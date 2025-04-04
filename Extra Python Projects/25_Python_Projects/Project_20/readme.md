# Online Multiplayer Top-Down Shooter 🎯🔥

A real-time multiplayer shooter game built with **Python**, **Pygame**, and **Sockets**. Play with friends over a local network (LAN) or the internet! 🚀

---

## 📌 Features
- ✔️ **Multiplayer**: Supports 2 or more players.
- ✔️ **Smooth Movement and Shooting**: Responsive controls for an engaging experience.
- ✔️ **Player Health System**: Track health and challenge opponents.
- ✔️ **Real-Time Updates**: Seamless communication between server and players using sockets.

---

## 🛠️ Installation

1. **Install Python (3.x)**  
   Download and install Python from [python.org](https://www.python.org/downloads/). Ensure `pip` is installed.

2. **Install Dependencies**  
   Use the following command to install the required libraries:
   ```bash
   pip install pygame
   ```

## 🚀 How to Run

### 1️⃣ Start the Server
**Run the server on one machine to host the game:**
```bash
python server.py
```
This will initialize the game server and wait for players to connect.

###  2️⃣ Run the Game Client
**Run the game client on each player's PC:**
```bash
python client.py
```
If playing over the internet, update the server_ip variable in client.py to point to the server's IP address.

### 🎮 Controls
**Key	Action**
**W, A, S, D	Move Up, Left, Down, Right**
**Left Click	Shoot**
**Esc	Exit Game**

### 🔧 Customization
**1- Player and Bullet Speed Modify movement speed or bullet speed in client.py.**

**2- Server Settings Change maximum players, server port, and related settings in server.py.**

### 💡 Future Improvements
🎨 Add Animations and Sounds: Enhance player and environment interaction with effects.
🔫 Implement Power-Ups and Weapons: Add variety to gameplay with upgrades and different weapons.
🏆 Leaderboard System: Track and display player rankings.

### 🎉 Enjoy the Game!
Jump into the battlefield and dominate the leaderboard. Happy shooting! 🕹️🎯



