import os
import random


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_field():
    return [['.'] * 7 for _ in range(7)]

def print_field(field):
    print("  A B C D E F G")
    for i, row in enumerate(field):
        print(f"{i + 1} " + " ".join(row))

def is_valid_placement(field, row, col, length, horizontal):
    for i in range(length):
        r = row + (0 if horizontal else i)
        c = col + (i if horizontal else 0)
        if not (0 <= r < 7 and 0 <= c < 7) or field[r][c] != '.':
            return False

    # Check for touching ships, even diagonally
    for i in range(-1, length + 1):
        for j in range(-1, 2):
            r = row + (0 if horizontal else i)
            c = col + (i if horizontal else 0)
            if 0 <= r < 7 and 0 <= c < 7 and field[r][c] == 'S':
                return False
    return True

def place_ship(field, length):
    while True:
        horizontal = random.choice([True, False])
        row = random.randint(0, 7 - (1 if horizontal else length))
        col = random.randint(0, 7 - (length if horizontal else 1))
        if is_valid_placement(field, row, col, length, horizontal):
            for i in range(length):
                r = row + (0 if horizontal else i)
                c = col + (i if horizontal else 0)
                field[r][c] = 'S'
            break

def place_ships(field):
    for length in [3, 2, 2, 1, 1, 1, 1]:
        place_ship(field, length)

def translate_coords(coords):
    try:
        col = ord(coords[0].upper()) - ord('A')
        row = int(coords[1:]) - 1
        return row, col
    except (IndexError, ValueError):
        return None, None

def is_game_over(field):
    return not any('S' in row for row in field)

def play_game():
    player_name = input("Enter your name: ")
    print(f"Welcome, {player_name}!\n")

    hidden_field = create_field()
    place_ships(hidden_field)
    visible_field = create_field()
    shots = 0
    shot_history = set()  # Keep track of all previously shot cells

    while True:
        clear_screen()
        print_field(visible_field)
        coords = input("Enter your shot (e.g., B5): ").strip()
        row, col = translate_coords(coords)

        if row is None or col is None or not (0 <= row < 7 and 0 <= col < 7):
            print("Invalid input. Try again.")
            continue

        if (row, col) in shot_history:
            print("Already shot here. Try again.")
            continue

        shots += 1
        shot_history.add((row, col))

        if hidden_field[row][col] == 'S':
            visible_field[row][col] = 'X'
            hidden_field[row][col] = '.'
            print("Hit!")
            if is_game_over(hidden_field):
                print(f"You sank all ships in {shots} shots!")
                break
        else:
            visible_field[row][col] = 'O'
            print("Miss!")

def main():
    leaderboard = []
    while True:
        play_game()
        name = input("Enter your name: ")
        shots = int(input("Enter the number of shots you took: "))
        leaderboard.append((name, shots))
        leaderboard.sort(key=lambda x: x[1])  # Sort by number of shots

        if input("Play again? (y/n): ").lower() != 'y':
            print("\nLeaderboard:")
            for rank, (name, score) in enumerate(leaderboard, 1):
                print(f"{rank}. {name} - {score} shots")
            break

if __name__ == "__main__":
    main()
