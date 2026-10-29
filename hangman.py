#!/usr/bin/env python3
import os

# check if guess is contained in the secret phrase
def check_guess(phrase, guess, revealed):
    correct = False
    for index, letter in enumerate(phrase):
        if letter == guess:
            correct = True
            revealed[index] = letter
    return correct

# check if word has been guessed
def check_word(phrase, revealed):
    return list(phrase) == revealed

# gets the secret phrase from player
def get_phrase(player):
        print("\n---------------------------------------")
        print("Enter \"XXXX\" to quit game.")
        phrase = input(f"\nPlayer {player} | Enter secret word or phrase: ").upper()
        revealed = ['_'] * len(phrase)
        for index, letter in enumerate(phrase):
            if letter == ' ':
                revealed[index] = " "
        return phrase, revealed

# gets guess from guesser
def get_guess(guesser):
    try:
        guess = input(f"Player {guesser} | Enter guess: ")[0].upper()
    except:
        guess = " "
    return guess

# clears the screen
def clear_screen():
    os.system('clear')

# shows the revealed parts of the secret phrase
def show_revealed(revealed):
    print("\n", end="   ")
    for letter in revealed:
        print(letter, end=" ")
    print("\n")

def print_boxed(message):
    for i in range(len(message) + 4):
        print("-", end="")
    print(f"\n| {message} |")
    for i in range(len(message) + 4):
        print("-", end="")
    print()

# create scoreboard
def show_scoreboard(scoreboard):
    board = f"Player 1: {scoreboard[1]} | Player 2: {scoreboard[2]}"
    print_boxed(board)

# shows the hangman graphic and list of wrong guesses
def show_hangman(mistakes, wrong_guesses, scoreboard):
    format_guesses = " ".join(wrong_guesses)
    clear_screen()
    show_scoreboard(scoreboard)

    print(f"\n   +-----+ \t Mistakes: {format_guesses}")
    match mistakes:
        case 0:
            print("   |       ")
            print("   |       ")
            print("   |       ")              
        case 1:
            print("   |     O ")
            print("   |       ")
            print("   |       ")          
        case 2:
            print("   |     O ")
            print("   |     | ")
            print("   |       ")          
        case 3:
            print("   |     O ")
            print("   |    ~| ")
            print("   |       ")
        case 4:
            print("   |     O ")
            print("   |    ~|~")
            print("   |       ")
        case 5:
            print("   |     O ")
            print("   |    ~|~")
            print("   |    /  ")
        case _:
            print("   |     O ")
            print("   |    ~|~")
            print("   |    / \\")
    print("   |       ")


def take_turn(player, scoreboard):
    # sets guessing player
    if player == 1:
        guesser = 2
    else:
        guesser = 1

    # gets secret phrase from player
    phrase, revealed = get_phrase(player)

    # check for quit game command
    if phrase == "XXXX":
        clear_screen()
        if scoreboard[1] > scoreboard[2]:
            print_boxed(f"** Player 1 wins by {scoreboard[1] - scoreboard[2]} point! **")
        elif scoreboard[1] == scoreboard[2]:
            print_boxed("** It's a tie! **")
        else:
            print_boxed(f"** Player 2 wins by {scoreboard[2] - scoreboard[1]} point! **")
        print("\nThanks for playing!\n")
        exit()

    # initialize variables
    mistakes = 0
    wrong_guesses = []
    word_guessed = False

    # game loop
    while mistakes < 6:

        show_hangman(mistakes, wrong_guesses, scoreboard)
        show_revealed(revealed)
        guess = get_guess(guesser)

        # adds to mistake count and wrong guesses list if wrong
        if not check_guess(phrase, guess, revealed): 

            mistakes += 1
            wrong_guesses.append(guess)

        # breaks out of loop if word is correct
        if check_word(phrase, revealed):

            scoreboard[guesser] += 1
            show_hangman(mistakes, wrong_guesses, scoreboard)
            show_revealed(revealed)
            print(f"Great job, Player {guesser}!")
            return

    # only reaches here if guesser loses
    show_hangman(mistakes, wrong_guesses, scoreboard)
    print(f"\nGood try, Player {guesser}. The phrase was \"{phrase}\"")

clear_screen()
scoreboard = {1: 0, 2: 0}

# Game loop that alternates between players
while True:
    take_turn(1, scoreboard)  # Player 2 guesses
    take_turn(2, scoreboard)  # Player 1 guesses
    
