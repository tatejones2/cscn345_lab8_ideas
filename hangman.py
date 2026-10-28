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
        print("\nEnter \"XXXX\" to quit game.")
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

# create scoreboard
def show_scoreboard(scoreboard):
    print("\nScoreboard:\n")
    print(f"Player 1: {scoreboard[1]} | Player 2: {scoreboard[2]}\n")

# shows the hangman graphic and list of wrong guesses
def show_hangman(mistakes, wrong_guesses):
    format_guesses = " ".join(wrong_guesses)
    clear_screen()


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


def take_turn(player):
    # sets guessing player
    if player == 1:
        guesser = 2
    else:
        guesser = 1

    # gets secret phrase from player
    phrase, revealed = get_phrase(player)

    # check for quit game command
    if phrase == "XXXX":
        print("\nThanks for playing!\n")
        exit()

    # initialize variables
    mistakes = 0
    wrong_guesses = []
    word_guessed = False

    # initialize scoreboard variables
    player1_score = 0
    player2_score = 0

    # game loop
    while mistakes < 6:

        show_hangman(mistakes, wrong_guesses)
        show_revealed(revealed)
        guess = get_guess(guesser)

        # adds to mistake count and wrong guesses list if wrong
        if not check_guess(phrase, guess, revealed): 

            mistakes += 1
            wrong_guesses.append(guess)

        # breaks out of loop if word is correct
        if check_word(phrase, revealed):

            show_hangman(mistakes, wrong_guesses)
            show_revealed(revealed)
            print(f"Great job, Player {guesser}!")

            # add score
            if guesser == 1:
                player1_score += 1
            else:
                player2_score += 1

            return True

    # only reaches here if guesser loses
    show_hangman(mistakes, wrong_guesses)
    print(f"\nGood try, Player {guesser}. The phrase was \"{phrase}\"\n")
    
    return False

    


# Game loop that alternates between players
scoreboard = {1: 0, 2: 0}

while True:
    if take_turn(1):  # Player 2 guesses
        scoreboard[2] += 1

    show_scoreboard(scoreboard)

    if take_turn(2):  # Player 1 guesses
        scoreboard[1] += 1

    show_scoreboard(scoreboard)
