# CrossWord
#
# LIMITATION
# - Various files

import csv
from random import choice
from sys import exit
from os import stat

# CONSTANTS AND VARIABLES
# Define dictionary table + hints
CROSSWORD1_FILES = {
    "table": "1_CROSSWORD_TABLE.csv",
    "hints": "1_CROSSWORD_HINTS.csv"
}

CROSSWORD2_FILES = {
    "table": "2_CROSSWORD_TABLE.csv",
    "hints": "2_CROSSWORD_HINTS.csv"
}

CROSSWORD_SAVE_FILES = {
    "table": "0_CROSSWORD_SAVE.csv",
    "hints": "0_CROSSWORD_SAVE_HINT.csv",
    "answers": "0_CROSSWORD_SAVE_ANSWERS.csv"
}

# Define variable for randomized table files
selected_game = []

# Define variable for game_grid
game_grid = []

# Define variable for hints dictionary
hints = {}

# Define variable for answers list
answers = []


# FUNCTIONS
# Define function load_grid
def load_game_grid(file):
    # Define variable for loaded grid
    loaded_grid = []
    # Open and read selected table file
    table_open = open(file, "r")
    table_reader = csv.reader(table_open)
    # Iterate csv file and append to grid
    for row in table_reader:
        loaded_grid.append(row)
    # Close file
    table_open.close()

    return loaded_grid


# Define function print_game_grid
def print_game_grid(game_grid):
    for j in range(len(game_grid)):
        print(game_grid[j])


# Define function load_hints
def load_hints(file):
    # Define variable for loaded hints
    loaded_hints = []
    # Open and read selected hint file
    hint_open = open(file, "r")
    hint_reader = csv.DictReader(hint_open, delimiter="@")
    # Iterate csv file and create hint dictionary
    for row in hint_reader:
        loaded_hints = {k: v.split("%") for k, v in row.items()}
    # Close file
    hint_open.close()

    return loaded_hints


# Define function print_hints
def print_hints(loaded_hints):
    print("HINTS[Row,Column]")
    for j in loaded_hints.values():
        print(j[3])
    print()


# Define function load_answers
def load_answers(file, answer_list):
    # Open and read answers file
    answers_open = open(file, "r")
    answers_reader = csv.reader(answers_open)
    # Iterate csv file and create answers list
    for row in answers_reader:
        for item in row:
            answer_list.append(item)
            
    return answer_list


# Define function to populate game_grid
def place_word(word, hints, game_grid):
    # If input matches a key, then place it in proper place in matrix
    # If word orientation horizontal
    if hints[word][0] == "HORIZONTAL_TYPE":
        for k in range(len(word)):
            game_grid[int(hints[word][1])][k + int(hints[word][2])] = word[k]

    # If word orientation vertical
    elif hints[word][0] == "VERTICAL_TYPE":
        for k in range(len(word)):
            game_grid[k + int(hints[word][1])][int(hints[word][2])] = word[k]


# Define function to save game history
def save_game_grid(save_file_name):
    save_open = open(save_file_name, "w", newline="")
    save_writer = csv.writer(save_open)
    # Write game rows
    save_writer.writerows(game_grid)
    #Close file
    save_open.close()


# Define function to save hint file name
def save_hint_filename(chosen_file):   
    history_hint_open = open(CROSSWORD_SAVE_FILES["hints"], "w")
    history_hint_writer = csv.writer(history_hint_open)
    # Write hint file name
    history_hint_writer.writerow(chosen_file)
    # Close file
    history_hint_open.close()


# Save answers list
def save_answers(answer_list):  
    history_answers_open = open(CROSSWORD_SAVE_FILES["answers"], "w")
    history_hint_writer = csv.writer(history_answers_open)
    # Write answers in file
    history_hint_writer.writerow(answer_list)
    # Close file
    history_answers_open.close()


# Define function to pause game and save
def pause_game(answer_list):
    save_game_grid(CROSSWORD_SAVE_FILES["table"])
    save_answers(answer_list)
    input("Write 'c' to return to game\n")


# Define function to exit game
def exit_game(answer_list):
    save_game_grid(CROSSWORD_SAVE_FILES["table"])
    save_answers(answer_list)
    exit()


# Define function to compute score
def compute_score(played_word, hints):
    score = 0
    # If word in answers list
    for word in played_word:
        if word in hints:
            score += 1
        else:
            score -= 1
    return score


# Define function to erase game saves
def erase_saves(table_save_file, hint_save_file, answers_save_file):
    # Open files
    history_open = open(table_save_file, "w")
    history_hint_open = open(hint_save_file, "w")
    history_answers_open = open(answers_save_file, "w")
    # Erase files
    history_open.truncate()
    history_hint_open.truncate()
    history_answers_open.truncate()
    # Close files
    history_open.close()
    history_hint_open.close()
    history_answers_open.close()


def process_user_word(word, answer_list):
    # If word already in game_grid or not in dictionary, print 'Try Again'
    if word in answer_list or word not in hints:
        print("Try Again!")
    # Proceed with game
    else:
        place_word(word, hints, game_grid)
        print_game_grid(game_grid)
        print_hints(hints)

    # Append to answers list
    answer_list.append(word)
    # Print answers list
    print("Played words:", answer_list)
    print()

    # Get Score
    score = compute_score(answers, hints)
    print("(+1 point/correct word; -1 point/incorrect word)\nScore: \n", score)


# Define function to end game if no words left
def has_won_game(game_grid):
    return all(" " not in row for row in game_grid)


# Define game_loop
def game_loop(answer_list):
    # Define variable to keep game running
    running = True

    # Start game loop
    while running:
        # Ask user input and inform how to pause or exit game
        user_input = input(
            "--> Please write a solution to a hint (Write 'p|P' or 'e|E' to pause or exit the game):\n").upper()

        # Pause game or exit chance 
        if user_input == "P":
            pause_game(answer_list)
        elif user_input == "E":
            exit_game(answer_list)
        # Continue game
        else:
            process_user_word(user_input, answer_list)
            if has_won_game(game_grid):
                # Print victory
                print("You win!")
                # Erase and close history files
                erase_saves(CROSSWORD_SAVE_FILES["table"], CROSSWORD_SAVE_FILES["answers"], CROSSWORD_SAVE_FILES["hints"])

                # End loop to finish game
                running = False


# Define function for game process
def start_game(crosswords_file, dictionary_file, answer_list):
    # Load game_grid
    global game_grid
    game_grid = load_game_grid(crosswords_file)
    # Print game_grid
    print_game_grid(game_grid)
    # Load game hints
    global hints
    hints = load_hints(dictionary_file)
    # Print hints
    print_hints(hints)
    # Print answers
    print("Played words:", answer_list)
    # Set Score
    compute_score(answer_list, hints)
    # Game loop
    game_loop(answer_list)


# Define function for new game
def new_game():
    # Select table
    global selected_game
    selected_game = choice([CROSSWORD1_FILES, CROSSWORD2_FILES])
    # Save hint file name
    save_hint_filename(selected_game["hints"])
    # Start game
    start_game(selected_game["table"], selected_game["hints"], answers)


# Define function to confirm if save exists
def has_save_game():
    return stat(CROSSWORD_SAVE_FILES["table"]).st_size > 0


# Define function to continue game
def continue_game():
    # Get hints file name
    hint_filename_open = open(CROSSWORD_SAVE_FILES["hints"], "r")
    hint_filename = next(csv.reader(hint_filename_open))
    hint_filename_str = ""
    for char in hint_filename:
        hint_filename_str += char
    # Close file
    hint_filename_open.close()
    # Load answers
    global answers
    answers = load_answers(CROSSWORD_SAVE_FILES["answers"], answers)

    # Start game
    start_game(CROSSWORD_SAVE_FILES["table"], hint_filename_str, answers)



# GAME PROCESS
# If there is no save file
if not has_save_game():
    new_game()
# If there is a save file
else:
    # Ask user if they want to continue saved game
    input_loop = True
    user_input = ""
    while input_loop:
        user_input = input("Do you want to continue saved game? (Yes/No): ").upper()
        if user_input in ["YES", "NO"]:
            input_loop = False
    # If NO
    if user_input == "NO":
        new_game()

    # If YES
    if user_input == "YES":
        continue_game()
