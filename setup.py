#!/usr/bin/env python3
"""
Setup script for Monster Collection Game
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_database():
    """Initialize the game database"""
    try:
        from game_data import seed_database
        seed_database()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to setup database: {e}")
        return False

def main():
    """Main setup function"""
    print("🐾 Setting up Monster Collection Game...")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    print("\n🎮 Setup complete! You can now run the game with:")
    print("   python monster_game.py")
    print("\nEnjoy catching monsters! 🐾")

if __name__ == "__main__":
    main()
