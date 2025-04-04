import pygame
import socket
import threading
import json
import random
import time
import sys
from typing import Dict, List, Any, Optional, Union

# Initialize pygame
pygame.init()
pygame.font.init()

# Game settings
WIDTH, HEIGHT = 800, 600
screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Shooter")
clock: pygame.time.Clock = pygame.time.Clock()
font: pygame.font.Font = pygame.font.SysFont('Arial', 24)

# Player settings
player_id: Optional[int] = None
player_size: int = 40
player_color: tuple[int, int, int] = (
    random.randint(50, 255),
    random.randint(50, 255),
    random.randint(50, 255)
)
player_speed: int = 5

# Networking
client_socket: Union[socket.socket, None] = None
connection_active: bool = False
reconnect_attempts: int = 0
MAX_RECONNECT_ATTEMPTS: int = 3
RECONNECT_DELAY: float = 2.0

# Game state
players: Dict[int, Dict[str, Any]] = {}
bullets: List[Dict[str, Any]] = []
last_shot: int = 0
shot_cooldown: int = 500  # ms

def establish_connection() -> bool:
    global client_socket, connection_active, reconnect_attempts
    
    while reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
        try:
            # Clean up previous socket if exists
            if client_socket:
                client_socket.close()
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5.0)
            client_socket.connect(("127.0.0.1", 5555))  # Change to server IP if needed
            connection_active = True
            reconnect_attempts = 0
            print("Successfully connected to server!")
            return True
        except socket.error as e:
            print(f"Connection failed (attempt {reconnect_attempts + 1}/{MAX_RECONNECT_ATTEMPTS}): {e}")
            reconnect_attempts += 1
            time.sleep(RECONNECT_DELAY)
        except Exception as e:
            print(f"Unexpected connection error: {e}")
            reconnect_attempts += 1
            time.sleep(RECONNECT_DELAY)
    
    print("Max connection attempts reached. Exiting...")
    return False

def receive_data() -> None:
    global players, bullets, player_id, connection_active
    
    while connection_active and client_socket:
        try:
            data: bytes = client_socket.recv(8192)
            if not data:
                print("Server closed connection")
                connection_active = False
                break
                
            game_state: Dict[str, Any] = json.loads(data.decode('utf-8'))
            
            if "your_id" in game_state:
                player_id = game_state["your_id"]
                print(f"Assigned player ID: {player_id}")
                continue
                
            with threading.Lock():
                players = game_state.get("players", {})
                bullets = game_state.get("bullets", [])
                
        except json.JSONDecodeError:
            print("Received invalid game data")
        except ConnectionResetError:
            print("Server disconnected unexpectedly")
            connection_active = False
            break
        except Exception as e:
            print(f"Network error: {e}")
            connection_active = False
            break

def send_data(data: dict) -> bool:
    if not connection_active or not client_socket:
        return False
        
    try:
        client_socket.send(json.dumps(data).encode())
        return True
    except Exception as e:
        print(f"Failed to send data: {e}")
        connection_active = False
        return False

def main() -> None:
    global connection_active, last_shot, reconnect_attempts
    
    if not establish_connection():
        pygame.quit()
        sys.exit(1)

    # Start data receiver thread
    threading.Thread(target=receive_data, daemon=True).start()

    running: bool = True
    while running:
        current_time: int = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Reconnect logic
        if not connection_active:
            if reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
                if establish_connection():
                    threading.Thread(target=receive_data, daemon=True).start()
            else:
                running = False
            continue

        # Shooting logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and current_time - last_shot > shot_cooldown:
            if player_id is not None and player_id in players:
                if send_data({
                    "type": "shoot",
                    "x": players[player_id]["x"],
                    "y": players[player_id]["y"],
                    "dx": 0,
                    "dy": -10
                }):
                    last_shot = current_time

        # Movement logic
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= player_speed
        if keys[pygame.K_s]: dy += player_speed
        if keys[pygame.K_a]: dx -= player_speed
        if keys[pygame.K_d]: dx += player_speed

        if dx != 0 or dy != 0:
            send_data({
                "type": "move",
                "dx": dx,
                "dy": dy
            })

        # Rendering
        screen.fill((0, 0, 0))
        
        # Draw players
        for pid, p in players.items():
            color: tuple[int, int, int] = p.get("color", player_color)
            pygame.draw.rect(screen, color, (p["x"], p["y"], player_size, player_size))
            
            # Health bar
            health: int = p.get("health", 100)
            pygame.draw.rect(screen, (255, 0, 0), (p["x"], p["y"] - 15, player_size, 5))
            pygame.draw.rect(screen, (0, 255, 0), (p["x"], p["y"] - 15, player_size * (health / 100), 5))
            
            # Highlight local player
            if pid == player_id:
                pygame.draw.rect(screen, (255, 255, 255), (p["x"], p["y"], player_size, player_size), 2)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, (255, 215, 0), (int(bullet["x"]), int(bullet["y"])), 5)

        # Display info
        if player_id in players:
            health_text: str = f"Health: {players[player_id].get('health', 100)}"
            screen.blit(font.render(health_text, True, (255, 255, 255)), (10, 10))

        # Connection status
        if not connection_active:
            status_text: str = "RECONNECTING..." if reconnect_attempts < MAX_RECONNECT_ATTEMPTS else "CONNECTION LOST"
            screen.blit(font.render(status_text, True, (255, 0, 0)), (WIDTH//2 - 80, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

    # Clean shutdown
    if connection_active and client_socket:
        send_data({"type": "disconnect"})
        client_socket.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()