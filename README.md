# Python Playground

This repository contains various Python projects and games, created to explore different aspects of Python programming, game development, and AI interactions.

## Projects

### Pomodoro.py
- A simple command line based pomodoro timer by Claude
- To run: python pomodoro.py --work 25 --short 5 --long 15 --sessions 4 --auto
Where:

--work: Work session duration in minutes (default: 25)
--short: Short break duration in minutes (default: 5)
--long: Long break duration in minutes (default: 15)
--sessions: Number of work sessions before a long break (default: 4)
--auto: Auto-start each session without prompting

### Bouncing Balls
- A simulation created to test collision detection and Pygame capabilities
- Features a bouncing yellow ball within a rotating square
- Implements proper physics and collision handling
- Often used to detect coding skills in new models

### Hangman Game
- Classic text-based Hangman implementation
- Features:
  - Word guessing with limited attempts
  - ASCII art display
  - Score tracking system
  - Persistent high scores saved to JSON file

### Tetris
- Pygame implementation of the classic Tetris game
- Features:
  - Complete piece rotation and movement
  - Score tracking
  - Next piece preview
  - Game over detection and restart capability

## Setup

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requi