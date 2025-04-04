import socket
import threading
import json
import random
import time
import atexit
from typing import Dict, List, Any, Tuple, Optional

# Server configuration
HOST: str = '0.0.0.0'
PORT: int = 5555
TICK_RATE: int = 60
PLAYER_SIZE: int = 40
WIDTH, HEIGHT = 800, 600

# Game state
players: Dict[int, Dict[str, Any]] = {}
bullets: List[Dict[str, Any]] = []
player_counter: int = 0
lock: threading.Lock = threading.Lock()

# Initialize server socket
server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def cleanup() -> None:
    """Clean up server socket on exit"""
    print("\nCleaning up server...")
    server.close()
    print("Server socket closed properly")

atexit.register(cleanup)

def handle_client(conn: socket.socket, addr: Tuple[str, int], pid: int) -> None:
    global players, bullets
    
    # Initialize new player
    with lock:
        players[pid] = {
            "x": random.randint(100, WIDTH-100),
            "y": random.randint(100, HEIGHT-100),
            "health": 100,
            "color": (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            ),
            "last_update": time.time()
        }
    
    try:
        # Send player their ID
        conn.send(json.dumps({"your_id": pid}).encode())
        
        while True:
            try:
                data: bytes = conn.recv(4096)
                if not data:
                    break
                    
                action: Dict[str, Any] = json.loads(data.decode('utf-8'))
                
                with lock:
                    # Process movement
                    if action["type"] == "move":
                        players[pid]["x"] = max(0, min(WIDTH-PLAYER_SIZE, players[pid]["x"] + action["dx"]))
                        players[pid]["y"] = max(0, min(HEIGHT-PLAYER_SIZE, players[pid]["y"] + action["dy"]))
                        players[pid]["last_update"] = time.time()
                    
                    # Process shooting
                    elif action["type"] == "shoot":
                        bullets.append({
                            "x": action["x"],
                            "y": action["y"],
                            "dx": action["dx"],
                            "dy": action["dy"],
                            "owner": pid,
                            "time": time.time()
                        })
                    
                    # Update game state
                    current_time: float = time.time()
                    
                    # Move bullets and check collisions
                    for bullet in bullets[:]:
                        bullet["x"] += bullet["dx"]
                        bullet["y"] += bullet["dy"]
                        
                        # Remove out-of-bounds bullets
                        if not (0 <= bullet["x"] <= WIDTH and 0 <= bullet["y"] <= HEIGHT):
                            bullets.remove(bullet)
                            continue
                            
                        # Check bullet-player collisions
                        for player_id, player in players.items():
                            if player_id != bullet["owner"]:
                                if (player["x"] < bullet["x"] < player["x"] + PLAYER_SIZE and
                                    player["y"] < bullet["y"] < player["y"] + PLAYER_SIZE):
                                    player["health"] -= 10
                                    if bullet in bullets:
                                        bullets.remove(bullet)
                                    break
                    
                    # Remove dead players
                    dead_players: List[int] = [pid for pid, p in players.items() if p["health"] <= 0]
                    for dead_pid in dead_players:
                        del players[dead_pid]
                    
                    # Send game state back to client
                    conn.send(json.dumps({
                        "players": players,
                        "bullets": [b for b in bullets if current_time - b["time"] < 3.0]  # 3 second lifetime
                    }).encode())
                    
            except json.JSONDecodeError:
                print(f"Invalid data from player {pid}")
            except Exception as e:
                print(f"Error with player {pid}: {e}")
                break
                
    finally:
        with lock:
            if pid in players:
                print(f"Player {pid} disconnected")
                del players[pid]
        conn.close()

def main() -> None:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    try:
        while True:
            conn: socket.socket
            addr: Tuple[str, int]
            conn, addr = server.accept()
            with lock:
                global player_counter
                player_counter += 1
                threading.Thread(
                    target=handle_client,
                    args=(conn, addr, player_counter),
                    daemon=True
                ).start()
                print(f"Player {player_counter} connected from {addr}")
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    main()