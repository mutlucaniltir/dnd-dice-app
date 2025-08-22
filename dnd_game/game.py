
import random

class Entity:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

    def is_alive(self):
        return self.hp > 0

class Player(Entity):
    def __init__(self, name):
        super().__init__(name, 100, 10)
        self.x = 0
        self.y = 0
        self.inventory = []

class Monster(Entity):
    pass

class World:
    def __init__(self):
        self.rooms = {}

    def get_room(self, x, y):
        if (x, y) not in self.rooms:
            self.rooms[(x, y)] = self.generate_room()
        return self.rooms[(x, y)]

    def generate_room(self):
        room_type = random.choice(["normal", "treasure", "fountain", "trap"])
        
        room = {
            "description": "",
            "monster": None,
            "item": None,
            "room_type": room_type,
        }

        if room_type == "normal":
            room["description"] = random.choice([
                "You are in a dark, damp cave.",
                "You've entered a chamber filled with the bones of past adventurers.",
                "A long, narrow hallway stretches before you.",
                "You are in a vast cavern. You can hear the dripping of water.",
            ])
            monster_data = {
                "goblin": {"hp": 30, "attack": 5},
                "giant spider": {"hp": 50, "attack": 8},
                "skeleton": {"hp": 40, "attack": 6},
            }
            monster_name = random.choice(list(monster_data.keys()) + [None])
            if monster_name:
                stats = monster_data[monster_name]
                room["monster"] = Monster(monster_name, stats["hp"], stats["attack"])
            
            room["item"] = random.choice([None, "a rusty sword", "a mysterious amulet"])

        elif room_type == "treasure":
            room["description"] = "You find yourself in a brightly lit room with a large, ornate treasure chest."
            room["item"] = random.choice(["a gleaming sword", "a suit of armor", "a magical staff"])

        elif room_type == "fountain":
            room["description"] = "You've discovered a room with a beautiful fountain in the center. The water glows with a soft, inviting light."

        elif room_type == "trap":
            room["description"] = "You enter a room and hear a 'click' under your feet. It's a trap!"

        return room

def print_room(room):
    print(room["description"])
    if room["monster"]:
        print(f"You see a {room['monster'].name} here.")
    if room["item"]:
        print(f"You see {room['item']} on the ground.")

def combat(player, monster):
    print(f"You have encountered a {monster.name}!")
    while player.is_alive() and monster.is_alive():
        player_damage = random.randint(0, player.attack_power)
        monster.hp -= player_damage
        print(f"You attack the {monster.name} for {player_damage} damage. The {monster.name} has {monster.hp} HP left.")
        if not monster.is_alive():
            print(f"You have defeated the {monster.name}!")
            return

        monster_damage = random.randint(0, monster.attack_power)
        player.hp -= monster_damage
        print(f"The {monster.name} attacks you for {monster_damage} damage. You have {player.hp} HP left.")
        if not player.is_alive():
            print("You have been defeated.")
            return

def get_player_action(room):
    actions = {
        "1": "go north",
        "2": "go south",
        "3": "go east",
        "4": "go west",
        "5": "inventory",
        "6": "quit",
    }

    print("\nWhat do you want to do?")
    print("1. Go North")
    print("2. Go South")
    print("3. Go East")
    print("4. Go West")

    action_num = 5
    if room.get("monster"):
        actions[str(action_num)] = "attack"
        print(f"{action_num}. Attack the {room['monster'].name}")
        action_num += 1

    if room.get("item"):
        actions[str(action_num)] = f"get {room['item']}"
        print(f"{action_num}. Get the {room['item']}")
        action_num += 1

    if room["room_type"] == "fountain":
        actions[str(action_num)] = "drink"
        print(f"{action_num}. Drink from the fountain")
        action_num += 1

    print(f"{action_num}. View Inventory")
    actions[str(action_num)] = "inventory"
    action_num += 1
    print(f"{action_num}. Quit")
    actions[str(action_num)] = "quit"

    while True:
        choice = input("> ")
        if choice in actions:
            return actions[choice]
        else:
            print("Invalid choice. Please try again.")

def main():
    player_name = input("Enter your name, adventurer: ")
    player = Player(player_name)
    world = World()

    print(f"Welcome, {player.name}!")

    while player.is_alive():
        room = world.get_room(player.x, player.y)
        print_room(room)

        if room["room_type"] == "trap":
            damage = random.randint(5, 15)
            player.hp -= damage
            print(f"You sprung a trap and took {damage} damage! You have {player.hp} HP left.")
            room["room_type"] = "normal"
            if not player.is_alive():
                print("You have been defeated.")
                break

        command = get_player_action(room)

        if command == "quit":
            print("You have fled the dungeon.")
            break
        elif command.startswith("go "):
            direction = command.split(" ")[1]
            if direction == "north":
                player.y += 1
            elif direction == "south":
                player.y -= 1
            elif direction == "east":
                player.x += 1
            elif direction == "west":
                player.x -= 1
        elif command == "attack":
            monster = room.get("monster")
            if monster:
                combat(player, monster)
                if not monster.is_alive():
                    room["monster"] = None
        elif command.startswith("get "):
            item_to_get = command.split(" ", 1)[1]
            if room["item"] and item_to_get in room["item"]:
                print(f"You pick up the {room['item']}.")
                player.inventory.append(room["item"])
                room["item"] = None
        elif command == "inventory":
            if player.inventory:
                print("You are carrying:")
                for item in player.inventory:
                    print(f"- {item}")
            else:
                print("Your inventory is empty.")
        elif command == "drink":
            if room["room_type"] == "fountain":
                healing = random.randint(10, 30)
                player.hp = min(100, player.hp + healing)
                print(f"You drink from the fountain and restore {healing} HP. You now have {player.hp} HP.")
                room["description"] = "The fountain has been used and is now dry."
                room["room_type"] = "normal"

if __name__ == "__main__":
    main()
