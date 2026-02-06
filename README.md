# project-DSA-python
Semester 2 Data Structure with Python Project


# Connect 4 Game (Python and Tkinter)

Connect 4 is a classic two-player strategy game in which players alternately drop discs into a vertical grid, with the objective of connecting four pieces horizontally, vertically, or diagonally.

This project implements the Connect 4 game using Python and the Tkinter library, providing an interactive graphical user interface along with enhanced gameplay features.

---

## Objectives

- Develop a fully functional GUI-based Connect 4 game  
- Implement game logic using two-dimensional Python lists  
- Include both Normal Mode and Battle Mania Mode (timed, best-of-three series)  
- Ensure a user-friendly interface with rule display, safe quit, and restart options  

---

## Tools and Technologies

- Python (Programming Language)  
- Tkinter (Graphical User Interface framework)  
- Two-dimensional Python lists (data structure for the game board)  
- Compatible with standard Python IDLE  

---

## System Design and Features

- The game board is a 6×7 grid displayed using a Tkinter canvas  
- Player names are entered through a single setup window  
- Column buttons are provided for disc placement  
- Turn indicators display the current player  
- A countdown timer is used in Battle Mania mode  
- Control buttons include Restart and Quit  
- The system checks for win or draw conditions after every move  
- Game rules can be accessed at any stage during gameplay  

---

## Battle Mania Mode

- Best-of-three game format  
- Fifteen-second time limit per move for each player  
- Automatic disc placement when the timer expires  
- Live scoreboard displaying current game wins  
- Overall winner announced after completion of three games  

---

## Key Features

- Interactive graphical user interface with visual disc placement  
- Real-time access to game rules  
- Timed gameplay with automatic move execution on timeout  
- Safe quit and restart options requiring consent from both players  
- Decorative welcome and exit screens with countdown functionality  

---

## How to Run

```bash
python connect4.py
