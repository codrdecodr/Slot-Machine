import random
from playsound import playsound

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbols and their properties
symbol_count = {"🍒": 2, "🍋": 4, "🍉": 6, "🍇": 8, "🎰": 3}
symbol_value = {"🍒": 5, "🍋": 4, "🍉": 3, "🍇": 2, "🎰": 0}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    # Iterate over each line
    for line in range(lines):
        symbol = columns[0][line]  # Get the symbol from the first column for comparison
        for column in columns:
            if column[line] != symbol:
                break
        else:
            # All symbols match on this line
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)

    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end="|")
            else:
                print(column[row], end="")
        print()


def check_jackpot(columns):
    for column in columns:
        if all(symbol == "🎰" for symbol in column):
            return True
    return False


def play_jackpot_sound():
    try:
        playsound("jackpot_sound.mp3")
    except Exception as e:
        print(f"Could not play jackpot sound: {e}")


def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a valid number.")


def get_number_of_lines():
    while True:
        lines = input(f"Enter number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a valid number.")


def get_bet():
    while True:
        amount = input(f"What would you like to bet on each line? (${MIN_BET}-${MAX_BET}): ")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")


def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    if check_jackpot(slots):
        print("""
        ****************************************************
        🎰🎰🎰 JACKPOT!!! 🎰🎰🎰
        ****************************************************
        """)
        play_jackpot_sound()
        return balance + 1000  # Award a bonus for hitting the jackpot

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    if winning_lines:
        print(f"You won on lines: {', '.join(map(str, winning_lines))}")
    else:
        print("No winnings this time.")

    return balance + winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is: ${balance}")
        answer = input("Press Enter to play (q to quit): ")
        if answer.lower() == "q":
            break
        balance = spin(balance)
    print(f"You left with ${balance}")


main()
