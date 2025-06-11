from models import MonsterSpecies, Achievement, get_session
from items_data import seed_items

# Monster species data
MONSTER_SPECIES_DATA = [
    # Fire Type
    {"name": "Flamewyrm", "type": "Fire", "base_hp": 45, "base_attack": 52, "base_defense": 43, "base_speed": 65, "rarity": "Common", "description": "A fierce dragon with burning spirit"},
    {"name": "Blazeclaw", "type": "Fire", "base_hp": 58, "base_attack": 64, "base_defense": 58, "base_speed": 80, "rarity": "Uncommon", "description": "Sharp claws that burn everything they touch"},
    {"name": "Infernotail", "type": "Fire", "base_hp": 78, "base_attack": 84, "base_defense": 78, "base_speed": 100, "rarity": "Rare", "description": "Its tail burns with the heat of a thousand suns"},
    
    # Water Type
    {"name": "Aquafin", "type": "Water", "base_hp": 44, "base_attack": 48, "base_defense": 65, "base_speed": 43, "rarity": "Common", "description": "A graceful sea creature with healing powers"},
    {"name": "Tidalwave", "type": "Water", "base_hp": 60, "base_attack": 65, "base_defense": 80, "base_speed": 58, "rarity": "Uncommon", "description": "Controls ocean currents with its mind"},
    {"name": "Leviathan", "type": "Water", "base_hp": 95, "base_attack": 85, "base_defense": 100, "base_speed": 78, "rarity": "Epic", "description": "Ancient ruler of the deepest oceans"},
    
    # Grass Type
    {"name": "Vinewhip", "type": "Grass", "base_hp": 45, "base_attack": 49, "base_defense": 49, "base_speed": 45, "rarity": "Common", "description": "A nature spirit that controls plants"},
    {"name": "Thornbeast", "type": "Grass", "base_hp": 60, "base_attack": 62, "base_defense": 63, "base_speed": 60, "rarity": "Uncommon", "description": "Covered in poisonous thorns"},
    {"name": "Forestlord", "type": "Grass", "base_hp": 80, "base_attack": 82, "base_defense": 83, "base_speed": 80, "rarity": "Rare", "description": "Guardian of ancient forests"},
    
    # Electric Type
    {"name": "Sparkbolt", "type": "Electric", "base_hp": 35, "base_attack": 55, "base_defense": 40, "base_speed": 90, "rarity": "Common", "description": "Quick as lightning, strikes without warning"},
    {"name": "Thunderwing", "type": "Electric", "base_hp": 50, "base_attack": 70, "base_defense": 55, "base_speed": 105, "rarity": "Uncommon", "description": "Flies through storm clouds"},
    {"name": "Voltking", "type": "Electric", "base_hp": 70, "base_attack": 90, "base_defense": 75, "base_speed": 125, "rarity": "Epic", "description": "Master of all electrical energy"},
    
    # Rock Type
    {"name": "Rockgrinder", "type": "Rock", "base_hp": 80, "base_attack": 120, "base_defense": 130, "base_speed": 35, "rarity": "Common", "description": "Crushes boulders with its bare hands"},
    {"name": "Stoneguard", "type": "Rock", "base_hp": 95, "base_attack": 135, "base_defense": 145, "base_speed": 50, "rarity": "Uncommon", "description": "An impenetrable fortress of stone"},
    {"name": "Mountainking", "type": "Rock", "base_hp": 120, "base_attack": 150, "base_defense": 160, "base_speed": 65, "rarity": "Rare", "description": "Ancient as the mountains themselves"},
    
    # Air Type
    {"name": "Windrazor", "type": "Air", "base_hp": 40, "base_attack": 60, "base_defense": 40, "base_speed": 95, "rarity": "Common", "description": "Cuts through air with razor-sharp wings"},
    {"name": "Stormcaller", "type": "Air", "base_hp": 55, "base_attack": 75, "base_defense": 55, "base_speed": 110, "rarity": "Uncommon", "description": "Summons powerful windstorms"},
    {"name": "Skyemperor", "type": "Air", "base_hp": 75, "base_attack": 95, "base_defense": 75, "base_speed": 130, "rarity": "Epic", "description": "Rules the endless skies above"},
    
    # Legendary
    {"name": "Cosmicdragon", "type": "Cosmic", "base_hp": 106, "base_attack": 110, "base_defense": 90, "base_speed": 130, "rarity": "Legendary", "description": "Born from the stars themselves"},
    {"name": "Voidbeast", "type": "Dark", "base_hp": 150, "base_attack": 150, "base_defense": 150, "base_speed": 150, "rarity": "Legendary", "description": "Emerges from the darkest depths of space"},
]

# Achievement data
ACHIEVEMENT_DATA = [
    {"name": "First Catch", "description": "Catch your first monster", "requirement_type": "catch_count", "requirement_value": 1},
    {"name": "Monster Collector", "description": "Catch 10 different monsters", "requirement_type": "catch_count", "requirement_value": 10},
    {"name": "Master Collector", "description": "Catch 25 different monsters", "requirement_type": "catch_count", "requirement_value": 25},
    {"name": "First Victory", "description": "Win your first battle", "requirement_type": "battle_wins", "requirement_value": 1},
    {"name": "Battle Veteran", "description": "Win 10 battles", "requirement_type": "battle_wins", "requirement_value": 10},
    {"name": "Battle Master", "description": "Win 50 battles", "requirement_type": "battle_wins", "requirement_value": 50},
    {"name": "Rare Hunter", "description": "Catch a rare monster", "requirement_type": "rare_catch", "requirement_value": 1},
    {"name": "Legendary Hunter", "description": "Catch a legendary monster", "requirement_type": "legendary_catch", "requirement_value": 1},
]

# Type effectiveness chart
TYPE_EFFECTIVENESS = {
    "Fire": {"Grass": 2.0, "Water": 0.5, "Rock": 2.0, "Air": 1.0, "Electric": 1.0},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Rock": 2.0, "Air": 1.0, "Electric": 0.5},
    "Grass": {"Water": 2.0, "Fire": 0.5, "Rock": 2.0, "Air": 0.5, "Electric": 1.0},
    "Electric": {"Water": 2.0, "Air": 2.0, "Grass": 0.5, "Rock": 1.0, "Fire": 1.0},
    "Rock": {"Fire": 0.5, "Air": 2.0, "Electric": 1.0, "Water": 0.5, "Grass": 0.5},
    "Air": {"Grass": 2.0, "Electric": 0.5, "Rock": 0.5, "Fire": 1.0, "Water": 1.0},
    "Cosmic": {"Dark": 2.0},
    "Dark": {"Cosmic": 2.0},
}

def seed_database():
    """Populate the database with initial data"""
    session = get_session()
    
    # Check if data already exists
    if session.query(MonsterSpecies).count() > 0:
        session.close()
        return
    
    # Add monster species
    for species_data in MONSTER_SPECIES_DATA:
        species = MonsterSpecies(**species_data)
        session.add(species)
    
    # Add achievements
    for achievement_data in ACHIEVEMENT_DATA:
        achievement = Achievement(**achievement_data)
        session.add(achievement)
    
    session.commit()
    session.close()
    
    # Seed items
    seed_items()
    
    print("Database seeded successfully!")

def get_type_effectiveness(attacker_type, defender_type):
    """Get type effectiveness multiplier"""
    if attacker_type in TYPE_EFFECTIVENESS:
        return TYPE_EFFECTIVENESS[attacker_type].get(defender_type, 1.0)
    return 1.0
