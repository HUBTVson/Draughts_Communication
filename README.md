# Draughts Game Console - Solution Documentation

# Table of Contents
1. [Introduction](https://github.com/HUBTVson/Draughts_Communication/blob/main/README.md#1-introduction)
2. [Game Idea](https://github.com/HUBTVson/Draughts_Communication/blob/main/README.md#2-game-idea)
3. [System Architecture](https://github.com/HUBTVson/Draughts_Communication/blob/main/README.md#3-system-architecture)
4. [Communication Protocol](https://github.com/HUBTVson/Draughts_Communication/blob/main/README.md#4-communication-protocol)
5. [Implementation](https://github.com/HUBTVson/Draughts_Communication/blob/main/README.md#5-implementation)
6. [Example Session](https://github.com/HUBTVson/Draughts_Communication/blob/main/README.md#6-example-session)

# 1. Introduction
Documents provides a detailed overwiev of a console-based Draughts game that is played between two clients connected to the server. The game is implemented in Python language and enable the real-time communication between players.

# 2. Game Idea
Draughts is a classic board game played on an 8x8 grid with 64 squares, alternating in colors green and red.

Each player begins with 12 pieces, distinguished by color, placed on the grey squares of three rows closest to them.
The goal is to capture all of the opponent's pieces or immobilize them so they cannot make a move.
Pieces move diagonally forward, one square at a time, onto empty adjacent squares.
When a player's piece reaches the opposite end of the board, it is "kinged" and gains the ability to move diagonally both forwards and backwards.
Captures are made by jumping over an opponent's piece onto an empty square immediately beyond it, removing the opponent's piece from the board.
Multiple captures can be made in a single turn if the opportunity arises, creating a strategic element of the game.

# 3. System Architecture
## The system consists of 3 main components:
### • Server:
Handles the game state and communication between clients.
### • Client A (Player 0):
Connects to the server to send and receive game moves.
### • Client B (Player 1):
Connects to the server to send and receive game moves.
## Diagrams !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 4. Communication Protocol
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 5. Implementation
## Main Components:
### 1. Server Implementation
#### • Server Initialization:
Sets up yhe server socket and listens for ingoing connections.
#### • Client Handler:
Sets up yhe server socket and listens for ingoing connections.
### 2. Client Implementation
#### • Client Initialization:
Sets up the client socket and connects to the server.
##### • Message Handling:
Sends player moves to the server and processes game state updates from the server.
### 3. Game Logic
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 6. Example Session
### uuuuaaaaa te kolory pionków fajnie by było dopasować 
## Server Output:
![image](https://github.com/HUBTVson/Draughts_Communication/assets/120310542/b161b091-c369-4314-8406-bd1efc0b6f3b)

![image](https://github.com/HUBTVson/Draughts_Communication/assets/120310542/ae30d62c-339d-4240-a879-8a0707658ddf)

## Client A Output:
![image](https://github.com/HUBTVson/Draughts_Communication/assets/120310542/bdbe14eb-761d-4f86-b462-86d5fc275f91)

## Client B Output:
![image](https://github.com/HUBTVson/Draughts_Communication/assets/120310542/a8f9df71-bb2c-4009-b2b6-19f3a2986419)


# Authors: Janicki Jakub, Kondracki Jakub, Twardowski Hubert





