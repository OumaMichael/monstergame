#!/usr/bin/env python3
"""
Monster Collection CLI Game
A text-based monster collection game where players can catch, train, battle, and trade monsters.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import MonsterGameCLI

def main():
    """Main entry point for the Monster Collection Game"""
    try:
        game = MonsterGameCLI()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your installation and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
