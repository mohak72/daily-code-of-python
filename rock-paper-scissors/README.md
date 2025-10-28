# Rock-Paper-Scissors Game

**Day 6 of 100 Days of Python**

## Description

Classic rock-paper-scissors game against the computer. Test your luck and strategy in this timeless game!

## Features

- Interactive command-line interface
- Play unlimited rounds
- Real-time score tracking
- Win/Loss/Draw statistics
- User-friendly prompts and feedback
- Input validation

## Installation

```bash
# Navigate to the project directory
cd rock-paper-scissors

# Install dependencies (for testing)
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

### How to Play

1. Run the game
2. Choose your weapon:
   - 1 for Rock
   - 2 for Paper
   - 3 for Scissors
3. See the result of each round
4. Keep playing or quit anytime
5. View your final score

### Game Rules

- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock

## Testing

```bash
pytest tests/ -v
```

## Requirements

- Python 3.8+

## Project Structure

```
rock-paper-scissors/
├── main.py              # Main application
├── tests/               # Unit tests
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Learning Outcomes

This project helped learn:
- Random number generation
- Control flow and conditionals
- Dictionary usage
- User input handling and validation
- Game logic implementation
- Score tracking
- Easy-level programming concepts

---

*Part of 100 Days of Code Challenge*
