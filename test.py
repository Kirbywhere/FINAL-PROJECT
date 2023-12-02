import os
import keyboard
import random
import time

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_line():
    # ANSI escape code to clear the entire line
    print("\033[K", end='', flush=True)

def type_text(text, delay=0.03, clear_line_after=True):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if clear_line_after:
        print('\r\033[K', end='', flush=True)  # carriage return and clear line
    else:
        print()

def print_board(player_pos, obstacles, enemy_pos, player_health, enemy_health):
    for row in range(10):
        for col in range(20):
            if (row, col) == player_pos:
                print("^", end=" ")
            elif (row, col) == enemy_pos:
                print("E", end=" ")
            elif (row, col) in obstacles:
                print("X", end=" ")
            else:
                print(".", end=" ")
        print()

    print("\nPlayer Health: [{}]  Enemy Health: [{}]".format("=" * player_health, "=" * enemy_health))

def select_attack(attacks):
    print("\nSelect an attack:")
    for i, attack in enumerate(attacks, start=1):
        print(f"{i}. {attack['name']} (Damage: {attack['damage']})")

    while True:
        try:
            choice = int(input("Enter the number of the attack: "))
            if 1 <= choice <= len(attacks):
                return attacks[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def attack_sequence(player_health, enemy_health, player_attack, enemy_attack):
    clear_line()  # Clear the previous line
    type_text("\nYou attack with {} (Damage: {})".format(player_attack['name'], player_attack['damage']))
    type_text("Enemy attacks with {} (Damage: {})".format(enemy_attack['name'], enemy_attack['damage']))

    # Ensure random damage is within the actual damage range
    player_damage = random.randint(max(1, player_attack['damage'] - 2), player_attack['damage'] + 2)
    enemy_damage = random.randint(max(1, enemy_attack['damage'] - 2), enemy_attack['damage'] + 2)

    player_health -= max(0, enemy_damage)
    enemy_health -= max(0, player_damage)

    type_text("You dealt {} damage!".format(player_damage))
    type_text("Enemy dealt {} damage!".format(enemy_damage))

    return player_health, enemy_health

def FOE_battle(player_pos, enemy_pos):
    type_text("angry FOE appeared!")
    player_health = 20
    enemy_health = 20

    attacks = [
        {"name": "Tackle", "damage": 5},
        {"name": "Scratch", "damage": 3},
        {"name": "Ember", "damage": 7},
    ]

    while True:
        print_board(player_pos, set(), enemy_pos, player_health, enemy_health)
        player_attack = select_attack(attacks)
        enemy_attack = random.choice(attacks)

        player_health, enemy_health = attack_sequence(player_health, enemy_health, player_attack, enemy_attack)

        if player_health <= 0:
            type_text("You fainted. Game Over!")
            return False
        elif enemy_health <= 0:
            type_text("You defeated the angry FOE!")
            return True

def encounter_scene():
    type_text("You encountered a angry FOE!")
    type_text("  ( )  ( )")
    type_text("   O    O")
    type_text("    \\  /")
    type_text("    (^)")
    type_text("Prepare for battle!")


def intro_story():
    clear_terminal()
    type_text("Welcome to the BAR!\n")
    type_text("In this game, you are in the middle of a brawl.")
    type_text("Your mission is to explore the world, fight angry FOEs, and gain their respect.")
    type_text("Prepare for an exciting adventure!")

def start_menu():
    clear_terminal()
    type_text("The BAR Adventure Game\n")
    type_text("1. Start", clear_line_after=False)
    type_text("2. Quit", clear_line_after=False)

    while True:
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            intro_story()
            return True
        elif choice == "2":
            return False
        else:
            type_text("Invalid choice. Please enter 1 or 2.", clear_line_after=True)

def move_player(player_pos, obstacles):
    clear_terminal()
    print_board(player_pos, obstacles, None, 20, 0)
    key = keyboard.read_event(suppress=True).name

    if key == "q":
        return "quit"
    elif key == "w" and player_pos[0] > 0:
        return "move", (player_pos[0] - 1, player_pos[1])
    elif key == "s" and player_pos[0] < 9:
        return "move", (player_pos[0] + 1, player_pos[1])
    elif key == "a" and player_pos[1] > 0:
        return "move", (player_pos[0], player_pos[1] - 1)
    elif key == "d" and player_pos[1] < 19:
        return "move", (player_pos[0], player_pos[1] + 1)
    else:
        return "invalid"

def main():
    if not start_menu():
        return

    player_pos = (5, 10)
    obstacles = {(2, 5), (3, 15), (7, 8)}
    enemy_pos = None

    type_text("Use arrow keys to move (^). Avoid obstacles (X). Press 'q' to quit.")

    while True:
        action, new_pos = move_player(player_pos, obstacles)

        if action == "quit":
            break
        elif action == "move":
            player_pos = new_pos

            if player_pos in obstacles:
                clear_terminal()
                print_board(player_pos, obstacles, None, 20, 0)
                type_text("Game Over!")
                break

            if random.random() < 0.1 and enemy_pos is None:
                enemy_pos = (random.randint(0, 9), random.randint(0, 19))
                encounter_scene()

                if not FOE_battle(player_pos, enemy_pos):
                    clear_terminal()
                    break

if __name__ == "__main__":
    main()
