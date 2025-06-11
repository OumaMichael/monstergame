# 🐾 Monster Collection CLI Game

A text-based monster collection game where players can catch, train, battle, and trade monsters. Think Pokémon meets CLI with persistent data storage using SQLAlchemy.

## 🎮 Features

### Core Gameplay
- **Monster Catching**: Encounter wild monsters and attempt to catch them
- **Monster Training**: Level up monsters through battles and training
- **Battle System**: Turn-based combat with type effectiveness
- **Collection Management**: View and organize your monster collection
- **Player Progression**: Level up your character and earn money

### Monster System
- **20 Unique Species**: From common Flamewyrms to legendary Cosmicdragon
- **Type System**: Fire, Water, Grass, Electric, Rock, Air, Cosmic, Dark
- **Rarity Levels**: Common, Uncommon, Rare, Epic, Legendary
- **Type Effectiveness**: Strategic combat with strengths and weaknesses

### Battle Features
- Turn-based combat system
- Attack, defend, and run options
- Type effectiveness multipliers
- Experience and money rewards
- Monster leveling and stat growth

## 🚀 Quick Start

### Installation

1. **Clone or download the game files**
2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. **Run setup** (optional):
   \`\`\`bash
   python setup.py
   \`\`\`
4. **Start the game**:
   \`\`\`bash
   python monster_game.py
   \`\`\`

### First Time Playing

1. **Create a new player** when prompted
2. **Choose your starter monster**:
   - Flamewyrm (Fire) - Balanced attacker
   - Aquafin (Water) - Defensive healer  
   - Vinewhip (Grass) - Nature controller
3. **Start exploring** to catch wild monsters!

## 🎯 How to Play

### Main Menu Options

1. **Explore & Catch Monsters**
   - Encounter random wild monsters
   - Attempt to catch them (success based on rarity and your level)
   - Build your collection

2. **Battle Wild Monsters**
   - Choose one of your monsters to battle
   - Turn-based combat with attack/defend options
   - Gain experience and money from victories

3. **View Collection**
   - See all your caught monsters
   - Check their stats, levels, and health
   - Monitor your collection progress

4. **Train Monsters**
   - Heal all monsters for $100
   - Train individual monsters to gain experience
   - Level up monsters to increase their stats

5. **Player Profile**
   - View your player statistics
   - See collection breakdown by rarity
   - Track your progress

### Battle System

**Type Effectiveness Chart:**
- Fire > Grass, Rock
- Water > Fire, Rock  
- Grass > Water, Rock
- Electric > Water, Air
- Rock > Fire, Air
- Air > Grass, Electric

**Combat Options:**
- **Attack**: Deal damage based on your monster's attack stat
- **Defend**: Reduce incoming damage by 50%
- **Run Away**: Escape from battle (no rewards)

### Monster Rarity & Catch Rates

| Rarity | Base Catch Rate | Examples |
|--------|----------------|----------|
| Common | 80% | Flamewyrm, Aquafin, Vinewhip |
| Uncommon | 60% | Blazeclaw, Tidalwave, Thornbeast |
| Rare | 40% | Infernotail, Forestlord, Mountainking |
| Epic | 20% | Leviathan, Voltking, Skyemperor |
| Legendary | 5% | Cosmicdragon, Voidbeast |

## 🗃️ Database Schema

The game uses SQLite with SQLAlchemy ORM:

- **Players**: User accounts and progression
- **Monster_Species**: Template data for monster types
- **Player_Monsters**: Individual monster instances
- **Battles**: Battle history and results
- **Trades**: Trading system (future feature)
- **Achievements**: Milestone tracking (future feature)

## 🛠️ Technical Details

### Requirements
- Python 3.7+
- SQLAlchemy 2.0+
- colorama (for colored terminal output)

### File Structure
\`\`\`
monster_game/
├── monster_game.py      # Main entry point
├── cli.py              # Command-line interface
├── game_engine.py      # Core game logic
├── models.py           # Database models
├── game_data.py        # Game data and seeding
├── setup.py            # Setup script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── monster_game.db     # SQLite database (created on first run)
\`\`\`

### Key Classes
- `GameEngine`: Core game logic and database operations
- `MonsterGameCLI`: Command-line interface and user interaction
- `Player`, `MonsterSpecies`, `PlayerMonster`: Database models

## 🎨 Game Features in Detail

### Monster Stats
Each monster has the following stats that grow with level:
- **HP**: Health points
- **Attack**: Damage dealing capability
- **Defense**: Damage resistance
- **Speed**: Turn order in battle (future feature)

### Leveling System
- Monsters gain experience from battles and training
- 100 experience points needed per level
- Each level increases all stats by +2
- Level up fully heals the monster

### Money System
- Earn money from winning battles
- Spend money on healing services
- Future: Buy items, pokeballs, etc.

## 🔮 Future Features

### Planned Additions
- **Trading System**: Trade monsters between players
- **Achievement System**: Unlock rewards for milestones
- **Gym Leaders**: Special boss battles
- **Monster Evolution**: Transform monsters at certain levels
- **Items & Inventory**: Potions, pokeballs, and equipment
- **Multiplayer Battles**: Challenge other players
- **Breeding System**: Create new monster combinations

### Technical Improvements
- Save/load game states
- Import/export collections
- Battle replay system
- Advanced AI opponents
- Tournament mode

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**Database errors:**
\`\`\`bash
rm monster_game.db
python setup.py
\`\`\`

**Permission errors on Linux/Mac:**
\`\`\`bash
chmod +x monster_game.py
\`\`\`

## 🤝 Contributing

This is a pair programming educational project. Key areas for contribution:
- Balance testing and adjustments
- Additional monster species
- New battle mechanics
- UI/UX improvements
- Bug fixes and optimizations

## 📝 License

Educational project - feel free to use and modify for learning purposes.

## 🎉 Credits

Created as a pair programming assignment to demonstrate:
- SQLAlchemy ORM usage
- CLI application design
- Game logic implementation
- Database relationship management
- Collaborative development practices

---

**Happy Monster Collecting! 🐾**
