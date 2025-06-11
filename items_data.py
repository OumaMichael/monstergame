from models import Item, PlayerInventory, ItemUsage, get_session

# Items data
ITEMS_DATA = [
    # Healing Potions
    {
        "name": "Health Potion",
        "description": "Restores 50 HP to a monster",
        "item_type": "potion",
        "effect_type": "heal",
        "effect_value": 50,
        "price": 200,
        "rarity": "Common"
    },
    {
        "name": "Super Potion",
        "description": "Restores 120 HP to a monster",
        "item_type": "potion",
        "effect_type": "heal",
        "effect_value": 120,
        "price": 500,
        "rarity": "Uncommon"
    },
    {
        "name": "Hyper Potion",
        "description": "Restores 200 HP to a monster",
        "item_type": "potion",
        "effect_type": "heal",
        "effect_value": 200,
        "price": 1000,
        "rarity": "Rare"
    },
    {
        "name": "Max Potion",
        "description": "Fully restores a monster's HP",
        "item_type": "potion",
        "effect_type": "full_heal",
        "effect_value": 0,
        "price": 2000,
        "rarity": "Epic"
    },
    {
        "name": "Revival Herb",
        "description": "Revives a fainted monster with half HP",
        "item_type": "potion",
        "effect_type": "revive",
        "effect_value": 50,
        "price": 1500,
        "rarity": "Rare"
    },
    
    # Pokeballs
    {
        "name": "Monster Ball",
        "description": "Standard ball for catching monsters",
        "item_type": "pokeball",
        "effect_type": "catch_boost",
        "effect_value": 0,
        "price": 100,
        "rarity": "Common"
    },
    {
        "name": "Great Ball",
        "description": "Better catch rate than Monster Ball",
        "item_type": "pokeball",
        "effect_type": "catch_boost",
        "effect_value": 15,
        "price": 300,
        "rarity": "Uncommon"
    },
    {
        "name": "Ultra Ball",
        "description": "High-performance ball with excellent catch rate",
        "item_type": "pokeball",
        "effect_type": "catch_boost",
        "effect_value": 30,
        "price": 800,
        "rarity": "Rare"
    },
    {
        "name": "Master Ball",
        "description": "Never fails to catch any monster",
        "item_type": "pokeball",
        "effect_type": "catch_boost",
        "effect_value": 100,
        "price": 10000,
        "rarity": "Legendary"
    },
    
    # Battle Items
    {
        "name": "Attack Boost",
        "description": "Temporarily increases a monster's attack by 50%",
        "item_type": "battle",
        "effect_type": "attack_boost",
        "effect_value": 50,
        "price": 400,
        "rarity": "Uncommon"
    },
    {
        "name": "Defense Boost",
        "description": "Temporarily increases a monster's defense by 50%",
        "item_type": "battle",
        "effect_type": "defense_boost",
        "effect_value": 50,
        "price": 400,
        "rarity": "Uncommon"
    },
    {
        "name": "Speed Boost",
        "description": "Temporarily increases a monster's speed by 50%",
        "item_type": "battle",
        "effect_type": "speed_boost",
        "effect_value": 50,
        "price": 400,
        "rarity": "Uncommon"
    },
    {
        "name": "Power Elixir",
        "description": "Doubles all stats for one battle",
        "item_type": "battle",
        "effect_type": "all_boost",
        "effect_value": 100,
        "price": 1200,
        "rarity": "Epic"
    },
    
    # Experience Items
    {
        "name": "EXP Candy S",
        "description": "Gives 25 experience points to a monster",
        "item_type": "misc",
        "effect_type": "exp_boost",
        "effect_value": 25,
        "price": 150,
        "rarity": "Common"
    },
    {
        "name": "EXP Candy M",
        "description": "Gives 50 experience points to a monster",
        "item_type": "misc",
        "effect_type": "exp_boost",
        "effect_value": 50,
        "price": 300,
        "rarity": "Uncommon"
    },
    {
        "name": "EXP Candy L",
        "description": "Gives 100 experience points to a monster",
        "item_type": "misc",
        "effect_type": "exp_boost",
        "effect_value": 100,
        "price": 600,
        "rarity": "Rare"
    },
    {
        "name": "Rare Candy",
        "description": "Instantly levels up a monster",
        "item_type": "misc",
        "effect_type": "level_up",
        "effect_value": 1,
        "price": 2500,
        "rarity": "Epic"
    },
    
    # Special Items
    {
        "name": "Lucky Charm",
        "description": "Increases money earned from battles by 50% for 5 battles",
        "item_type": "misc",
        "effect_type": "money_boost",
        "effect_value": 50,
        "price": 800,
        "rarity": "Rare"
    },
    {
        "name": "Shiny Stone",
        "description": "Increases chance of finding rare monsters for 10 encounters",
        "item_type": "misc",
        "effect_type": "rare_boost",
        "effect_value": 25,
        "price": 1500,
        "rarity": "Epic"
    },
    {
        "name": "Monster Treat",
        "description": "Increases friendship and catch rate for wild monsters",
        "item_type": "misc",
        "effect_type": "friendship_boost",
        "effect_value": 20,
        "price": 250,
        "rarity": "Common"
    }
]

def seed_items():
    """Populate the database with items"""
    session = get_session()
    
    # Check if items already exist
    if session.query(Item).count() > 0:
        session.close()
        return
    
    # Add items
    for item_data in ITEMS_DATA:
        item = Item(**item_data)
        session.add(item)
    
    session.commit()
    session.close()
    print("Items seeded successfully!")

class ItemManager:
    def __init__(self):
        self.session = get_session()
    
    def get_all_items(self):
        """Get all available items"""
        return self.session.query(Item).all()
    
    def get_items_by_type(self, item_type):
        """Get items by type"""
        return self.session.query(Item).filter_by(item_type=item_type).all()
    
    def get_player_inventory(self, player_id):
        """Get player's inventory"""
        return self.session.query(PlayerInventory).filter_by(player_id=player_id).all()
    
    def add_item_to_inventory(self, player_id, item_id, quantity=1):
        """Add item to player's inventory"""
        existing = self.session.query(PlayerInventory).filter_by(
            player_id=player_id, item_id=item_id
        ).first()
        
        if existing:
            existing.quantity += quantity
        else:
            inventory_item = PlayerInventory(
                player_id=player_id,
                item_id=item_id,
                quantity=quantity
            )
            self.session.add(inventory_item)
        
        self.session.commit()
        return True
    
    def remove_item_from_inventory(self, player_id, item_id, quantity=1):
        """Remove item from player's inventory"""
        inventory_item = self.session.query(PlayerInventory).filter_by(
            player_id=player_id, item_id=item_id
        ).first()
        
        if not inventory_item or inventory_item.quantity < quantity:
            return False
        
        inventory_item.quantity -= quantity
        if inventory_item.quantity <= 0:
            self.session.delete(inventory_item)
        
        self.session.commit()
        return True
    
    def use_item(self, player_id, item_id, monster_id=None):
        """Use an item"""
        # Check if player has the item
        inventory_item = self.session.query(PlayerInventory).filter_by(
            player_id=player_id, item_id=item_id
        ).first()
        
        if not inventory_item or inventory_item.quantity <= 0:
            return False, "You don't have this item!"
        
        item = self.session.query(Item).get(item_id)
        if not item:
            return False, "Item not found!"
        
        # Apply item effect
        success, message = self.apply_item_effect(player_id, item, monster_id)
        
        if success:
            # Remove item from inventory
            self.remove_item_from_inventory(player_id, item_id, 1)
            
            # Record usage
            usage = ItemUsage(
                player_id=player_id,
                item_id=item_id,
                monster_id=monster_id,
                success=True
            )
            self.session.add(usage)
            self.session.commit()
        
        return success, message
    
    def apply_item_effect(self, player_id, item, monster_id=None):
        """Apply the effect of an item"""
        from models import Player, PlayerMonster
        
        if item.effect_type == "heal":
            if not monster_id:
                return False, "This item requires a monster to use on!"
            
            monster = self.session.query(PlayerMonster).get(monster_id)
            if not monster or monster.player_id != player_id:
                return False, "Monster not found or not owned by you!"
            
            if monster.hp >= monster.max_hp:
                return False, "Monster is already at full health!"
            
            old_hp = monster.hp
            monster.hp = min(monster.max_hp, monster.hp + item.effect_value)
            healed = monster.hp - old_hp
            self.session.commit()
            
            return True, f"Monster healed for {healed} HP!"
        
        elif item.effect_type == "full_heal":
            if not monster_id:
                return False, "This item requires a monster to use on!"
            
            monster = self.session.query(PlayerMonster).get(monster_id)
            if not monster or monster.player_id != player_id:
                return False, "Monster not found or not owned by you!"
            
            if monster.hp >= monster.max_hp:
                return False, "Monster is already at full health!"
            
            monster.hp = monster.max_hp
            self.session.commit()
            
            return True, "Monster fully healed!"
        
        elif item.effect_type == "revive":
            if not monster_id:
                return False, "This item requires a monster to use on!"
            
            monster = self.session.query(PlayerMonster).get(monster_id)
            if not monster or monster.player_id != player_id:
                return False, "Monster not found or not owned by you!"
            
            if monster.hp > 0:
                return False, "Monster is not fainted!"
            
            monster.hp = monster.max_hp * item.effect_value // 100
            self.session.commit()
            
            return True, f"Monster revived with {monster.hp} HP!"
        
        elif item.effect_type == "exp_boost":
            if not monster_id:
                return False, "This item requires a monster to use on!"
            
            monster = self.session.query(PlayerMonster).get(monster_id)
            if not monster or monster.player_id != player_id:
                return False, "Monster not found or not owned by you!"
            
            monster.experience += item.effect_value
            
            # Check for level up
            leveled_up = False
            while monster.experience >= 100:
                monster.experience -= 100
                monster.level += 1
                monster.max_hp += 2
                monster.hp = monster.max_hp  # Full heal on level up
                monster.attack += 2
                monster.defense += 2
                monster.speed += 2
                leveled_up = True
            
            self.session.commit()
            
            if leveled_up:
                return True, f"Monster gained {item.effect_value} EXP and leveled up to level {monster.level}!"
            else:
                return True, f"Monster gained {item.effect_value} EXP!"
        
        elif item.effect_type == "level_up":
            if not monster_id:
                return False, "This item requires a monster to use on!"
            
            monster = self.session.query(PlayerMonster).get(monster_id)
            if not monster or monster.player_id != player_id:
                return False, "Monster not found or not owned by you!"
            
            old_level = monster.level
            monster.level += item.effect_value
            monster.experience = 0
            monster.max_hp += 2 * item.effect_value
            monster.hp = monster.max_hp  # Full heal on level up
            monster.attack += 2 * item.effect_value
            monster.defense += 2 * item.effect_value
            monster.speed += 2 * item.effect_value
            
            self.session.commit()
            
            return True, f"Monster leveled up from {old_level} to {monster.level}!"
        
        else:
            return False, "Item effect not implemented yet!"
    
    def buy_item(self, player_id, item_id, quantity=1):
        """Buy an item from the shop"""
        from models import Player
        
        player = self.session.query(Player).get(player_id)
        item = self.session.query(Item).get(item_id)
        
        if not player or not item:
            return False, "Player or item not found!"
        
        total_cost = item.price * quantity
        if player.money < total_cost:
            return False, f"Not enough money! Need ${total_cost}, have ${player.money}"
        
        player.money -= total_cost
        self.add_item_to_inventory(player_id, item_id, quantity)
        
        return True, f"Bought {quantity}x {item.name} for ${total_cost}!"
    
    def get_pokeball_catch_bonus(self, item_name):
        """Get catch rate bonus for pokeballs"""
        bonuses = {
            "Monster Ball": 0,
            "Great Ball": 0.15,
            "Ultra Ball": 0.30,
            "Master Ball": 1.0  # Guaranteed catch
        }
        return bonuses.get(item_name, 0)
    
    def close(self):
        """Close the database session"""
        self.session.close()
