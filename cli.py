from colorama import init, Fore
from game_engine import GameEngine
from game_data import seed_database
from models import Item
from items_data import ItemManager

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class MonsterGameCLI:
    def __init__(self):
        self.engine = GameEngine()
        self.current_player = None
        
    def print_header(self, text):
        """Print a styled header"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}{text.center(50)}")
        print(f"{Fore.CYAN}{'='*50}")
    
    def print_monster_ascii(self, monster_type):
        """Print ASCII art for monsters"""
        ascii_art = {
            "Fire": """
        🔥 FIRE MONSTER 🔥
           /\\_/\\  
          ( o.o ) 
           > ^ <  
            """,
            "Water": """
        🌊 WATER MONSTER 🌊
           ~~~~
          ( ^.^ )
           ~~~~
            """,
            "Grass": """
        🌿 GRASS MONSTER 🌿
           /\\_/\\
          ( -.-)
           > v <
            """,
            "Electric": """
        ⚡ ELECTRIC MONSTER ⚡
           /\\_/\\
          ( @.@)
           > ⚡ <
            """,
        }
        print(Fore.MAGENTA + ascii_art.get(monster_type, "🐾 MONSTER 🐾"))
    
    def main_menu(self):
        """Display the main menu"""
        while True:
            self.print_header("MONSTER COLLECTION GAME")
            print(f"{Fore.GREEN}1. {Fore.WHITE}Login/Create Player")
            print(f"{Fore.GREEN}2. {Fore.WHITE}Start New Game")
            print(f"{Fore.GREEN}3. {Fore.WHITE}Exit")
            
            choice = input(f"\n{Fore.YELLOW}Choose an option: {Fore.WHITE}")
            
            if choice == "1":
                self.login_menu()
            elif choice == "2":
                self.new_game_menu()
            elif choice == "3":
                print(f"{Fore.CYAN}Thanks for playing!")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.")
    
    def login_menu(self):
        """Handle player login/creation"""
        username = input(f"{Fore.YELLOW}Enter username: {Fore.WHITE}")
        
        player = self.engine.get_player(username)
        if player:
            self.current_player = player
            print(f"{Fore.GREEN}Welcome back, {username}!")
            self.game_menu()
        else:
            create = input(f"{Fore.YELLOW}Player not found. Create new player? (y/n): {Fore.WHITE}")
            if create.lower() == 'y':
                player, message = self.engine.create_player(username)
                if player:
                    self.current_player = player
                    print(f"{Fore.GREEN}{message}")
                    self.choose_starter()
                else:
                    print(f"{Fore.RED}{message}")
    
    def new_game_menu(self):
        """Start a completely new game"""
        username = input(f"{Fore.YELLOW}Enter new username: {Fore.WHITE}")
        player, message = self.engine.create_player(username)
        
        if player:
            self.current_player = player
            print(f"{Fore.GREEN}{message}")
            self.choose_starter()
        else:
            print(f"{Fore.RED}{message}")
    
    def choose_starter(self):
        """Let player choose their starter monster"""
        self.print_header("CHOOSE YOUR STARTER MONSTER")
        
        starters = self.engine.get_starter_monsters()
        
        for i, starter in enumerate(starters, 1):
            print(f"{Fore.GREEN}{i}. {Fore.CYAN}{starter.name} {Fore.YELLOW}({starter.type})")
            print(f"   {Fore.WHITE}{starter.description}")
            print(f"   HP: {starter.base_hp} | ATK: {starter.base_attack} | DEF: {starter.base_defense} | SPD: {starter.base_speed}")
            self.print_monster_ascii(starter.type)
        
        while True:
            try:
                choice = int(input(f"\n{Fore.YELLOW}Choose your starter (1-3): {Fore.WHITE}"))
                if 1 <= choice <= len(starters):
                    chosen_starter = starters[choice - 1]
                    monster = self.engine.give_starter_monster(self.current_player.id, chosen_starter.id)
                    print(f"\n{Fore.GREEN}Congratulations! You chose {chosen_starter.name}!")
                    self.engine.give_starter_monster(self.current_player.id, chosen_starter.id)
                    print(f"\n{Fore.GREEN}Congratulations! You chose {chosen_starter.name}!")
                    self.print_monster_ascii(chosen_starter.type)
                    self.game_menu()
                    break
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
    
    def game_menu(self):
        """Main game menu after login"""
        while True:
            self.print_header(f"WELCOME, {self.current_player.username.upper()}")
            print(f"{Fore.CYAN}Level: {self.current_player.level} | Money: ${self.current_player.money}")
            
            print(f"\n{Fore.GREEN}1. {Fore.WHITE}Explore & Catch Monsters")
            print(f"{Fore.GREEN}2. {Fore.WHITE}Battle Wild Monsters")
            print(f"{Fore.GREEN}3. {Fore.WHITE}View Collection")
            print(f"{Fore.GREEN}4. {Fore.WHITE}Train Monsters")
            print(f"{Fore.GREEN}5. {Fore.WHITE}Player Profile")
            print(f"{Fore.GREEN}6. {Fore.WHITE}Item Shop")
            print(f"{Fore.GREEN}7. {Fore.WHITE}Inventory")
            print(f"{Fore.GREEN}8. {Fore.WHITE}Player Profile")
            print(f"{Fore.GREEN}9. {Fore.WHITE}Logout")
            
            choice = input(f"\n{Fore.YELLOW}Choose an option: {Fore.WHITE}")
            
            if choice == "1":
                self.explore_menu()
            elif choice == "2":
                self.battle_menu()
            elif choice == "3":
                self.collection_menu()
            elif choice == "4":
                self.training_menu()
            elif choice == "5":
                self.profile_menu()
            elif choice == "6":
                self.shop_menu()
            elif choice == "7":
                self.inventory_menu()
            elif choice == "8":
                self.profile_menu()
            elif choice == "9":
                self.current_player = None
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.")
    
    def explore_menu(self):
        """Explore and encounter wild monsters"""
        self.print_header("EXPLORING THE WILD")
        
        print(f"{Fore.CYAN}You venture into the wilderness...")
        input(f"{Fore.YELLOW}Press Enter to continue...")
        
        wild_monster = self.engine.encounter_wild_monster()
        
        # Get the species info
        from models import MonsterSpecies
        species = self.engine.session.query(MonsterSpecies).get(wild_monster.species_id)
        
        print(f"\n{Fore.MAGENTA}A wild {species.name} appears!")
        print(f"{Fore.YELLOW}Type: {species.type} | Level: {wild_monster.level} | Rarity: {species.rarity}")
        self.print_monster_ascii(species.type)
        
        while True:
            print(f"\n{Fore.GREEN}1. {Fore.WHITE}Use Pokeball")
            print(f"{Fore.GREEN}2. {Fore.WHITE}Battle First")
            print(f"{Fore.GREEN}3. {Fore.WHITE}Run away")
            
            choice = input(f"\n{Fore.YELLOW}What do you want to do? {Fore.WHITE}")
            
            if choice == "1":
                success = self.use_pokeball_interface(wild_monster, species)
                if success:
                    break
            elif choice == "2":
                # Start battle first, then allow catching if monster survives
                player_monsters = self.engine.get_player_collection(self.current_player.id)
                if not player_monsters:
                    print(f"{Fore.RED}You have no monsters to battle with!")
                    continue
                
                # Choose monster for battle
                print(f"\n{Fore.CYAN}Choose your monster:")
                for i, monster in enumerate(player_monsters, 1):
                    monster_species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
                    if monster.hp > 0:
                        print(f"{Fore.GREEN}{i}. {monster_species.name} (Lv.{monster.level}) HP: {monster.hp}/{monster.max_hp}")
                
                try:
                    battle_choice = int(input(f"\n{Fore.YELLOW}Choose monster: {Fore.WHITE}")) - 1
                    if 0 <= battle_choice < len(player_monsters) and player_monsters[battle_choice].hp > 0:
                        battle_result = self.wild_battle_for_catch(player_monsters[battle_choice], wild_monster)
                        if battle_result == "wild_fainted":
                            print(f"{Fore.RED}The wild {species.name} fainted! You can't catch it now.")
                            break
                        elif battle_result == "player_fainted":
                            print(f"{Fore.RED}Your monster fainted! The wild {species.name} escaped!")
                            break
                        elif battle_result == "weakened":
                            print(f"{Fore.YELLOW}The wild {species.name} is weakened! Catch rate increased!")
                            # Continue to allow catching
                    else:
                        print(f"{Fore.RED}Invalid choice or monster is fainted!")
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number!")
                    
            elif choice == "3":
                print(f"\n{Fore.CYAN}You ran away safely.")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")
    
    def collection_menu(self):
        """View player's monster collection"""
        self.print_header("YOUR MONSTER COLLECTION")
        
        monsters = self.engine.get_player_collection(self.current_player.id)
        
        if not monsters:
            print(f"{Fore.RED}Your collection is empty! Go catch some monsters!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        
        for i, monster in enumerate(monsters, 1):
            species = self.engine.session.query(self.engine.session.query(monster.__class__).get(monster.species_id).__class__).get(monster.species_id)
            # Get species info
            from models import MonsterSpecies
            species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
            
            print(f"\n{Fore.CYAN}{i}. {species.name} {Fore.YELLOW}(Level {monster.level})")
            print(f"   Type: {species.type} | Rarity: {species.rarity}")
            print(f"   HP: {monster.hp}/{monster.max_hp} | ATK: {monster.attack} | DEF: {monster.defense} | SPD: {monster.speed}")
            print(f"   Experience: {monster.experience}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")
    
    def battle_menu(self):
        """Battle wild monsters"""
        self.print_header("BATTLE ARENA")
        
        # Get player's monsters
        player_monsters = self.engine.get_player_collection(self.current_player.id)
        
        if not player_monsters:
            print(f"{Fore.RED}You need monsters to battle! Go catch some first!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        
        # Choose player monster
        print(f"{Fore.CYAN}Choose your monster for battle:")
        for i, monster in enumerate(player_monsters, 1):
            from models import MonsterSpecies
            species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
            print(f"{Fore.GREEN}{i}. {species.name} {Fore.YELLOW}(Lv.{monster.level}) HP: {monster.hp}/{monster.max_hp}")
        
        try:
            choice = int(input(f"\n{Fore.YELLOW}Choose your monster: {Fore.WHITE}")) - 1
            if 0 <= choice < len(player_monsters):
                player_monster = player_monsters[choice]
                
                if player_monster.hp <= 0:
                    print(f"{Fore.RED}This monster has fainted! Heal it first!")
                    input(f"\n{Fore.YELLOW}Press Enter to continue...")
                    return
                
                self.start_battle(player_monster)
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")
    
    def start_battle(self, player_monster):
        """Start a battle between player monster and wild monster"""
        # Generate wild opponent
        wild_monster = self.engine.encounter_wild_monster()
        
        from models import MonsterSpecies
        player_species = self.engine.session.query(MonsterSpecies).get(player_monster.species_id)
        wild_species = self.engine.session.query(MonsterSpecies).get(wild_monster.species_id)
        
        self.print_header("BATTLE BEGINS!")
        print(f"{Fore.CYAN}{player_species.name} vs {wild_species.name}")
        print(f"{Fore.GREEN}Your {player_species.name}: HP {player_monster.hp}/{player_monster.max_hp}")
        print(f"{Fore.RED}Wild {wild_species.name}: HP {wild_monster.hp}/{wild_monster.max_hp}")
        
        # Battle loop
        turn = 1
        while player_monster.hp > 0 and wild_monster.hp > 0:
            print(f"\n{Fore.YELLOW}--- Turn {turn} ---")
            
            # Player turn
            print(f"\n{Fore.CYAN}What will {player_species.name} do?")
            print(f"{Fore.GREEN}1. {Fore.WHITE}Attack")
            print(f"{Fore.GREEN}2. {Fore.WHITE}Defend")
            print(f"{Fore.GREEN}3. {Fore.WHITE}Run Away")
            
            action = input(f"\n{Fore.YELLOW}Choose action: {Fore.WHITE}")
            
            if action == "1":
                # Player attacks
                result = self.engine.execute_battle_turn(player_monster, wild_monster)
                print(f"\n{Fore.GREEN}{player_species.name} attacks!")
                print(f"{Fore.WHITE}Deals {result['damage']} damage! {result['effect_message']}")
                print(f"{Fore.RED}Wild {wild_species.name} HP: {result['defender_hp']}/{wild_monster.max_hp}")
                
                if result['defender_fainted']:
                    print(f"\n{Fore.GREEN}Wild {wild_species.name} fainted! You win!")
                    # Give experience and money
                    player_monster.experience += 50
                    self.current_player.money += 100
                    self.engine.session.commit()
                    
                    if player_monster.experience >= 100:
                        self.engine.level_up_monster(player_monster.id)
                        print(f"{Fore.YELLOW}{player_species.name} leveled up!")
                    break
                
                # Wild monster attacks back
                result = self.engine.execute_battle_turn(wild_monster, player_monster)
                print(f"\n{Fore.RED}Wild {wild_species.name} attacks!")
                print(f"{Fore.WHITE}Deals {result['damage']} damage! {result['effect_message']}")
                print(f"{Fore.GREEN}Your {player_species.name} HP: {result['defender_hp']}/{player_monster.max_hp}")
                
                if result['defender_fainted']:
                    print(f"\n{Fore.RED}Your {player_species.name} fainted! You lose!")
                    break
                    
            elif action == "2":
                print(f"\n{Fore.CYAN}{player_species.name} defends!")
                # Reduce incoming damage by half
                result = self.engine.execute_battle_turn(wild_monster, player_monster)
                damage = result['damage'] // 2
                player_monster.hp = max(0, player_monster.hp - damage + result['damage'])  # Restore half damage
                print(f"{Fore.WHITE}Reduced damage to {damage}!")
                print(f"{Fore.GREEN}Your {player_species.name} HP: {player_monster.hp}/{player_monster.max_hp}")
                
            elif action == "3":
                print(f"\n{Fore.YELLOW}You ran away from battle!")
                break
            
            turn += 1
        
        # Update monster HP in database
        self.engine.session.commit()
    
    def training_menu(self):
        """Train and heal monsters"""
        self.print_header("TRAINING CENTER")
        
        monsters = self.engine.get_player_collection(self.current_player.id)
        
        if not monsters:
            print(f"{Fore.RED}You have no monsters to train!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        
        print(f"{Fore.GREEN}1. {Fore.WHITE}Heal All Monsters ($100)")
        print(f"{Fore.GREEN}2. {Fore.WHITE}Train Monster (Gain Experience)")
        print(f"{Fore.GREEN}3. {Fore.WHITE}Back")
        
        choice = input(f"\n{Fore.YELLOW}Choose option: {Fore.WHITE}")
        
        if choice == "1":
            if self.current_player.money >= 100:
                for monster in monsters:
                    self.engine.heal_monster(monster.id)
                self.current_player.money -= 100
                self.engine.session.commit()
                print(f"{Fore.GREEN}All monsters healed!")
            else:
                print(f"{Fore.RED}Not enough money! You need $100.")
        
        elif choice == "2":
            print(f"\n{Fore.CYAN}Choose monster to train:")
            for i, monster in enumerate(monsters, 1):
                from models import MonsterSpecies
                species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
                print(f"{Fore.GREEN}{i}. {species.name} {Fore.YELLOW}(Lv.{monster.level}) Exp: {monster.experience}/100")
            
            try:
                choice = int(input(f"\n{Fore.YELLOW}Choose monster: {Fore.WHITE}")) - 1
                if 0 <= choice < len(monsters):
                    monster = monsters[choice]
                    monster.experience += 25
                    
                    if monster.experience >= 100:
                        self.engine.level_up_monster(monster.id)
                        from models import MonsterSpecies
                        species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
                        print(f"{Fore.YELLOW}{species.name} leveled up to level {monster.level}!")
                    else:
                        self.engine.session.commit()
                        print(f"{Fore.GREEN}Training complete! Gained 25 experience.")
                else:
                    print(f"{Fore.RED}Invalid choice!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")
    
    def profile_menu(self):
        """Display player profile and statistics"""
        self.print_header(f"{self.current_player.username.upper()}'S PROFILE")
        
        monsters = self.engine.get_player_collection(self.current_player.id)
        
        print(f"{Fore.CYAN}Player Level: {Fore.WHITE}{self.current_player.level}")
        print(f"{Fore.CYAN}Experience: {Fore.WHITE}{self.current_player.experience}")
        print(f"{Fore.CYAN}Money: {Fore.WHITE}${self.current_player.money}")
        print(f"{Fore.CYAN}Monsters Caught: {Fore.WHITE}{len(monsters)}")
        print(f"{Fore.CYAN}Member Since: {Fore.WHITE}{self.current_player.created_at.strftime('%Y-%m-%d')}")
        
        # Show rarity breakdown
        rarity_count = {}
        for monster in monsters:
            from models import MonsterSpecies
            species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
            rarity_count[species.rarity] = rarity_count.get(species.rarity, 0) + 1
        
        if rarity_count:
            print(f"\n{Fore.YELLOW}Collection by Rarity:")
            for rarity, count in rarity_count.items():
                print(f"  {rarity}: {count}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")
    
    def shop_menu(self):
        """Item shop interface"""
        self.print_header("🏪 MONSTER MART")
        
        item_manager = ItemManager()
        
        while True:
            print(f"{Fore.CYAN}Your Money: ${self.current_player.money}")
            print(f"\n{Fore.GREEN}1. {Fore.WHITE}Potions & Healing")
            print(f"{Fore.GREEN}2. {Fore.WHITE}Pokeballs")
            print(f"{Fore.GREEN}3. {Fore.WHITE}Battle Items")
            print(f"{Fore.GREEN}4. {Fore.WHITE}Special Items")
            print(f"{Fore.GREEN}5. {Fore.WHITE}Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}Choose category: {Fore.WHITE}")
            
            if choice == "1":
                self.show_shop_category(item_manager, "potion")
            elif choice == "2":
                self.show_shop_category(item_manager, "pokeball")
            elif choice == "3":
                self.show_shop_category(item_manager, "battle")
            elif choice == "4":
                self.show_shop_category(item_manager, "misc")
            elif choice == "5":
                break
            else:
                print(f"{Fore.RED}Invalid choice!")
        
        item_manager.close()

    def show_shop_category(self, item_manager, category):
        """Show items in a specific category"""
        items = item_manager.get_items_by_type(category)
        
        if not items:
            print(f"{Fore.RED}No items in this category!")
            return
        
        category_names = {
            "potion": "🧪 POTIONS & HEALING",
            "pokeball": "⚾ POKEBALLS",
            "battle": "⚔️ BATTLE ITEMS",
            "misc": "✨ SPECIAL ITEMS"
        }
        
        self.print_header(category_names.get(category, "ITEMS"))
        
        for i, item in enumerate(items, 1):
            rarity_colors = {
                "Common": Fore.WHITE,
                "Uncommon": Fore.GREEN,
                "Rare": Fore.BLUE,
                "Epic": Fore.MAGENTA,
                "Legendary": Fore.YELLOW
            }
            color = rarity_colors.get(item.rarity, Fore.WHITE)
            
            print(f"{Fore.GREEN}{i}. {color}{item.name} {Fore.CYAN}(${item.price})")
            print(f"   {Fore.WHITE}{item.description}")
            print(f"   Rarity: {color}{item.rarity}")
        
        print(f"{Fore.GREEN}0. {Fore.WHITE}Back")
        
        try:
            choice = int(input(f"\n{Fore.YELLOW}Choose item to buy: {Fore.WHITE}"))
            if choice == 0:
                return
            elif 1 <= choice <= len(items):
                item = items[choice - 1]
                quantity = int(input(f"{Fore.YELLOW}How many? {Fore.WHITE}"))
                
                if quantity > 0:
                    success, message = item_manager.buy_item(self.current_player.id, item.id, quantity)
                    if success:
                        print(f"{Fore.GREEN}{message}")
                        # Update player money in current session
                        self.engine.session.refresh(self.current_player)
                    else:
                        print(f"{Fore.RED}{message}")
                else:
                    print(f"{Fore.RED}Invalid quantity!")
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

    def inventory_menu(self):
        """Player inventory interface"""
        self.print_header("🎒 YOUR INVENTORY")
        
        item_manager = ItemManager()
        inventory = item_manager.get_player_inventory(self.current_player.id)
        
        if not inventory:
            print(f"{Fore.RED}Your inventory is empty! Visit the shop to buy items.")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            item_manager.close()
            return
        
        # Group items by type
        items_by_type = {}
        for inv_item in inventory:
            item = self.engine.session.query(Item).get(inv_item.item_id)
            if item.item_type not in items_by_type:
                items_by_type[item.item_type] = []
            items_by_type[item.item_type].append((inv_item, item))
        
        # Display inventory
        all_items = []
        for item_type, items in items_by_type.items():
            type_names = {
                "potion": "🧪 Potions",
                "pokeball": "⚾ Pokeballs", 
                "battle": "⚔️ Battle Items",
                "misc": "✨ Special Items"
            }
            print(f"\n{Fore.CYAN}{type_names.get(item_type, item_type.title())}:")
            
            for inv_item, item in items:
                all_items.append((inv_item, item))
                rarity_colors = {
                    "Common": Fore.WHITE,
                    "Uncommon": Fore.GREEN,
                    "Rare": Fore.BLUE,
                    "Epic": Fore.MAGENTA,
                    "Legendary": Fore.YELLOW
                }
                color = rarity_colors.get(item.rarity, Fore.WHITE)
                
                print(f"  {len(all_items)}. {color}{item.name} {Fore.WHITE}x{inv_item.quantity}")
                print(f"     {item.description}")
        
        print(f"\n{Fore.GREEN}Enter item number to use, or 0 to go back")
        
        try:
            choice = int(input(f"\n{Fore.YELLOW}Choose item: {Fore.WHITE}"))
            if choice == 0:
                item_manager.close()
                return
            elif 1 <= choice <= len(all_items):
                inv_item, item = all_items[choice - 1]
                self.use_item_interface(item_manager, item, inv_item)
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")
        item_manager.close()

    def use_item_interface(self, item_manager, item, inv_item):
        """Interface for using an item"""
    def use_item_interface(self, item_manager, item, _):
        """Interface for using an item"""
        if item.item_type == "pokeball":
            print(f"{Fore.YELLOW}Pokeballs can only be used during monster encounters!")
            return
        
        monster_id = None
        
        # Check if item requires a monster
        if item.effect_type in ["heal", "full_heal", "revive", "exp_boost", "level_up"]:
            monsters = self.engine.get_player_collection(self.current_player.id)
            
            if not monsters:
                print(f"{Fore.RED}You have no monsters to use this item on!")
                return
            
            print(f"\n{Fore.CYAN}Choose monster to use {item.name} on:")
            
            valid_monsters = []
            for monster in monsters:
                from models import MonsterSpecies
                species = self.engine.session.query(MonsterSpecies).get(monster.species_id)
                
                # Filter based on item type
                if item.effect_type == "revive" and monster.hp > 0:
                    continue  # Can't revive non-fainted monsters
                elif item.effect_type in ["heal", "full_heal"] and monster.hp >= monster.max_hp:
                    continue  # Can't heal full-health monsters
                
                valid_monsters.append(monster)
                print(f"{len(valid_monsters)}. {species.name} (Lv.{monster.level}) HP: {monster.hp}/{monster.max_hp}")
            
            if not valid_monsters:
                if item.effect_type == "revive":
                    print(f"{Fore.RED}No fainted monsters to revive!")
                elif item.effect_type in ["heal", "full_heal"]:
                    print(f"{Fore.RED}All monsters are at full health!")
                else:
                    print(f"{Fore.RED}No valid monsters for this item!")
                return
            
            try:
                choice = int(input(f"\n{Fore.YELLOW}Choose monster: {Fore.WHITE}")) - 1
                if 0 <= choice < len(valid_monsters):
                    monster_id = valid_monsters[choice].id
                else:
                    print(f"{Fore.RED}Invalid choice!")
                    return
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
                return
        
        # Use the item
        success, message = item_manager.use_item(self.current_player.id, item.id, monster_id)
        
        if success:
            print(f"{Fore.GREEN}{message}")
        else:
            print(f"{Fore.RED}{message}")
        """Interface for using pokeballs to catch monsters"""
    def use_pokeball_interface(self, wild_monster, species):
        """Interface for using pokeballs to catch monsters"""
        item_manager = ItemManager()
        
        # Get player's pokeballs
        inventory = item_manager.get_player_inventory(self.current_player.id)
        pokeballs = []
        
        for inv_item in inventory:
            item = self.engine.session.query(Item).get(inv_item.item_id)
            if item.item_type == "pokeball":
                pokeballs.append((inv_item, item))
        
        if not pokeballs:
            print(f"{Fore.RED}You don't have any pokeballs! Visit the shop to buy some.")
            item_manager.close()
            return False
        
        print(f"\n{Fore.CYAN}Choose a pokeball:")
        for i, (inv_item, item) in enumerate(pokeballs, 1):
            rarity_colors = {
                "Common": Fore.WHITE,
                "Uncommon": Fore.GREEN,
                "Rare": Fore.BLUE,
                "Epic": Fore.MAGENTA,
                "Legendary": Fore.YELLOW
            }
            color = rarity_colors.get(item.rarity, Fore.WHITE)
            print(f"{Fore.GREEN}{i}. {color}{item.name} {Fore.WHITE}x{inv_item.quantity}")
            print(f"   {item.description}")
        
        print(f"{Fore.GREEN}0. {Fore.WHITE}Back")
        
        try:
            choice = int(input(f"\n{Fore.YELLOW}Choose pokeball: {Fore.WHITE}"))
            if choice == 0:
                item_manager.close()
                return False
            elif 1 <= choice <= len(pokeballs):
                inv_item, pokeball = pokeballs[choice - 1]
                
                # Use the pokeball
                success, message = self.engine.attempt_catch_with_ball(
                    self.current_player.id, wild_monster, pokeball.id
                )
                
                # Remove pokeball from inventory
                item_manager.remove_item_from_inventory(
                    self.current_player.id, pokeball.id, 1
                )
                
                print(f"\n{Fore.CYAN}You threw a {pokeball.name}!")
                
                if success:
                    print(f"{Fore.GREEN}{message}")
                    print(f"{Fore.CYAN}{species.name} was added to your collection!")
                    item_manager.close()
                    return True
                else:
                    print(f"{Fore.RED}{message}")
                    print(f"{Fore.YELLOW}The {pokeball.name} was lost...")
                    item_manager.close()
                    return False
            else:
                print(f"{Fore.RED}Invalid choice!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
        
        item_manager.close()
        return False
        """Simplified battle for weakening wild monsters before catching"""
        from models import MonsterSpecies
        
        player_species = self.engine.session.query(MonsterSpecies).get(player_monster.species_id)
        wild_species = self.engine.session.query(MonsterSpecies).get(wild_monster.species_id)
        
        print(f"\n{Fore.CYAN}Battle: {player_species.name} vs Wild {wild_species.name}")
        
        # Simple battle - just a few turns to weaken
        for turn in range(3):  # Max 3 turns
            # Player attacks
            result = self.engine.execute_battle_turn(player_monster, wild_monster)
            print(f"\n{Fore.GREEN}{player_species.name} attacks for {result['damage']} damage!")
            
            if result['defender_fainted']:
                return "wild_fainted"
            
            # Wild monster attacks back
            result = self.engine.execute_battle_turn(wild_monster, player_monster)
            print(f"{Fore.RED}Wild {wild_species.name} attacks for {result['damage']} damage!")
            
            if result['defender_fainted']:
                return "player_fainted"
            
            # Check if wild monster is weakened (below 50% HP)
            if wild_monster.hp < wild_monster.max_hp * 0.5:
                return "weakened"
        
        return "continue"
    
    def run(self):
        """Start the game"""
        # Initialize database
        seed_database()
        
        print(f"{Fore.MAGENTA}")
        print("🐾" * 20)
        print("  WELCOME TO MONSTER COLLECTION GAME!")
        print("     Now with Items & Inventory!")
        print("🐾" * 20)
        print(f"{Fore.RESET}")
        
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Game interrupted. Thanks for playing!")
        finally:
            self.engine.close()

if __name__ == "__main__":
    game = MonsterGameCLI()
    game.run()
