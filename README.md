# Project name: "Draughts"
# Authors: Janicki Jakub, Kondracki Jakub, Twardowski Hubert

# 1. Project Idea
The project is aimed to present the basic communication between the server and client in the droughts game board.


# 2. Game Idea
Draughts is a classic board game played on an 8x8 grid with 64 squares, alternating in colors green and yellow.


Each player begins with 12 pieces, distinguished by color, placed on the red squares of three rows closest to them.
The goal is to capture all of the opponent's pieces or immobilize them so they cannot make a move.
Pieces move diagonally forward, one square at a time, onto empty adjacent squares.
When a player's piece reaches the opposite end of the board, it is "kinged" and gains the ability to move diagonally both forwards and backwards.
Captures are made by jumping over an opponent's piece onto an empty square immediately beyond it, removing the opponent's piece from the board.
Multiple captures can be made in a single turn if the opportunity arises, creating a strategic element of the game.

# 3. Technology selection
Programming language: Python
Application: Console
Libraries: signal, socket


# 4. Division of responsibilities
Hubert Twardowski- Implementation of initial client
Jakub Kondracki- Implementation of initial server
Jakub Janicki-  Implementation of initial communication between client and server game
