import random
from models import Player, MonsterSpecies, PlayerMonster, Battle, get_session, Item
from game_data import get_type_effectiveness
from datetime import datetime
from items_data import ItemManager

class GameEngine:
    def __init__(self):
        self.session = get_session()
    
    def create_player(self, username):
        """Create a new player"""
        existing_player = self.session.query(Player).filter_by(username=username).first()
        if existing_player:
            return None, "Username already exists!"
        
        player = Player(username=username)
        self.session.add(player)
        self.session.commit()
        return player, "Player created successfully!"
    
    def get_player(self, username):
        """Get player by username"""
        return self.session.query(Player).filter_by(username=username).first()
    
    def get_starter_monsters(self):
        """Get the three starter monsters"""
        starters = ["Flamewyrm", "Aquafin", "Vinewhip"]
        return self.session.query(MonsterSpecies).filter(MonsterSpecies.name.in_(starters)).all()
    
    def give_starter_monster(self, player_id, species_id):
        """Give a starter monster to a new player"""
        species = self.session.query(MonsterSpecies).get(species_id)
        if not species:
            return None
        
        monster = self.create_monster_instance(player_id, species)
        self.session.add(monster)
        self.session.commit()
        return monster
    
    def create_monster_instance(self, player_id, species, level=1):
        """Create a monster instance from species template"""
        # Calculate stats based on level
        hp = species.base_hp + (level - 1) * 2
        attack = species.base_attack + (level - 1) * 2
        defense = species.base_defense + (level - 1) * 2
        speed = species.base_speed + (level - 1) * 2
        
        monster = PlayerMonster(
            player_id=player_id,
            species_id=species.id,
            level=level,
            hp=hp,
            max_hp=hp,
            attack=attack,
            defense=defense,
            speed=speed
        )
        return monster
    
    def encounter_wild_monster(self):
        """Generate a random wild monster encounter"""
        all_species = self.session.query(MonsterSpecies).all()
        
        # Weighted random selection based on rarity
        rarity_weights = {
            "Common": 50,
            "Uncommon": 25,
            "Rare": 15,
            "Epic": 8,
            "Legendary": 2
        }
        
        weighted_species = []
        for species in all_species:
            weight = rarity_weights.get(species.rarity, 1)
            weighted_species.extend([species] * weight)
        
        chosen_species = random.choice(weighted_species)
        level = random.randint(1, 10)
        
        return self.create_monster_instance(None, chosen_species, level)
    
    def calculate_catch_rate(self, species_rarity, player_level):
        """Calculate the probability of catching a monster"""
        base_rates = {
            "Common": 0.8,
            "Uncommon": 0.6,
            "Rare": 0.4,
            "Epic": 0.2,
            "Legendary": 0.05
        }
        
        base_rate = base_rates.get(species_rarity, 0.5)
        level_bonus = min(player_level * 0.01, 0.2)  # Max 20% bonus
        
        return min(base_rate + level_bonus, 0.95)  # Max 95% catch rate
    
    def attempt_catch(self, player_id, wild_monster):
        """Attempt to catch a wild monster"""
        player = self.session.query(Player).get(player_id)
        species = self.session.query(MonsterSpecies).get(wild_monster.species_id)
        
        catch_rate = self.calculate_catch_rate(species.rarity, player.level)
        
        if random.random() < catch_rate:
            # Successful catch
            wild_monster.player_id = player_id
            self.session.add(wild_monster)
            self.session.commit()
            return True, f"Successfully caught {species.name}!"
        else:
            return False, f"{species.name} broke free!"

    def attempt_catch_with_ball(self, player_id, wild_monster, pokeball_item_id=None):
        """Attempt to catch a wild monster with a specific pokeball"""
        player = self.session.query(Player).get(player_id)
        species = self.session.query(MonsterSpecies).get(wild_monster.species_id)
        
        base_catch_rate = self.calculate_catch_rate(species.rarity, player.level)
        
        # Apply pokeball bonus
        if pokeball_item_id:
            item_manager = ItemManager()
            item = self.session.query(Item).get(pokeball_item_id)
            if item and item.item_type == "pokeball":
                if item.name == "Master Ball":
                    # Master Ball never fails
                    wild_monster.player_id = player_id
                    self.session.add(wild_monster)
                    self.session.commit()
                    item_manager.close()
                    return True, f"Master Ball never fails! Successfully caught {species.name}!"
                else:
                    bonus = item_manager.get_pokeball_catch_bonus(item.name)
                    base_catch_rate = min(0.95, base_catch_rate + bonus)
        
        
            item_manager.close()
    
        if random.random() < base_catch_rate:
            # Successful catch
            wild_monster.player_id = player_id
            self.session.add(wild_monster)
            self.session.commit()
            return True, f"Successfully caught {species.name}!"
        else:
            return False, f"{species.name} broke free!"
    
    def get_player_collection(self, player_id):
        """Get all monsters owned by a player"""
        return self.session.query(PlayerMonster).filter_by(player_id=player_id).all()
    
    def level_up_monster(self, monster_id):
        """Level up a monster"""
        monster = self.session.query(PlayerMonster).get(monster_id)
        if not monster:
            return None
        
        monster.level += 1
        monster.experience = 0
        
        # Increase stats
        monster.max_hp += 2
        monster.hp = monster.max_hp  # Full heal on level up
        monster.attack += 2
        monster.defense += 2
        monster.speed += 2
        
        self.session.commit()
        return monster
    
    def calculate_damage(self, attacker, defender, move_power=50):
        """Calculate battle damage"""
        # Get type effectiveness
        attacker_species = self.session.query(MonsterSpecies).get(attacker.species_id)
        defender_species = self.session.query(MonsterSpecies).get(defender.species_id)
        
        effectiveness = get_type_effectiveness(attacker_species.type, defender_species.type)
        
        # Basic damage calculation
        level_factor = attacker.level / 50.0
        attack_factor = attacker.attack / defender.defense
        random_factor = random.uniform(0.85, 1.0)
        
        damage = int(move_power * level_factor * attack_factor * effectiveness * random_factor)
        return max(damage, 1), effectiveness
    
    def create_battle(self, player1_id, player2_id=None, battle_type="wild"):
        """Create a new battle"""
        battle = Battle(
            player1_id=player1_id,
            player2_id=player2_id,
            battle_type=battle_type
        )
        self.session.add(battle)
        self.session.commit()
        return battle
    
    def execute_battle_turn(self, attacker, defender, move_name="Tackle"):
        """Execute a single battle turn"""
        damage, effectiveness = self.calculate_damage(attacker, defender)
        defender.hp = max(0, defender.hp - damage)
        
        # Determine effectiveness message
        if effectiveness > 1.5:
            effect_msg = "It's super effective!"
        elif effectiveness < 0.75:
            effect_msg = "It's not very effective..."
        else:
            effect_msg = ""
        
        return {
            "damage": damage,
            "effectiveness": effectiveness,
            "effect_message": effect_msg,
            "defender_hp": defender.hp,
            "defender_fainted": defender.hp <= 0
        }
    
    def heal_monster(self, monster_id):
        """Fully heal a monster"""
        monster = self.session.query(PlayerMonster).get(monster_id)
        if monster:
            monster.hp = monster.max_hp
            self.session.commit()
            return True
        return False
    
    def close(self):
        """Close the database session"""
        self.session.close()
