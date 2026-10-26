#!/usr/bin/env python3
# Two-player Hangman with a graphics.py window.
# Needs graphics.py (John Zelle) in the same folder as this file.
import os
import sys
import time
from graphics import GraphWin, Point, Line, Circle, Rectangle, Text, GraphicsError

WIDTH = 700
HEIGHT = 540
MAX_MISTAKES = 6
MAX_PHRASE_LENGTH = 24
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

BUTTON_SIZE = 44
BUTTON_GAP = 6
BUTTON_LEFT = 27
BUTTON_TOP = 430


# ---------- game logic (same as hangman.py) ----------

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

# builds the blank list; spaces are shown from the start
def make_revealed(phrase):
    revealed = ['_'] * len(phrase)
    for index, letter in enumerate(phrase):
        if letter == ' ':
            revealed[index] = ' '
    return revealed


# ---------- drawing helpers ----------

# draws a Text object and returns it so it can be updated later
def make_text(win, x, y, message, size=14, style="normal", face="helvetica", color="black"):
    text = Text(Point(x, y), message)
    text.setSize(size)
    text.setStyle(style)
    text.setFace(face)
    text.setTextColor(color)
    text.draw(win)
    return text

# removes everything in a list of drawn objects
def undraw_all(objects):
    for item in objects:
        item.undraw()
    objects.clear()

# shows the revealed parts of the phrase as "_ A _ _"
def format_revealed(revealed):
    return " ".join(revealed)

# waits until a key is pressed or the mouse is clicked
# returns ("key", keysym) or ("click", Point)
def wait_for_input(win):
    while True:
        key = win.checkKey()
        if key:
            return "key", key
        point = win.checkMouse()
        if point:
            return "click", point
        time.sleep(0.02)

# waits for any click or key press
def wait_to_continue(win):
    wait_for_input(win)


# ---------- scoreboard / header ----------

def draw_header(win, round_number, setter, guesser, scores):
    objects = []
    objects.append(make_text(win, WIDTH / 2, 25, f"Round {round_number}  |  Player {guesser} is guessing",
                             size=18, style="bold"))
    objects.append(make_text(win, WIDTH / 2, 52, f"Player 1: {scores[1]}     Player 2: {scores[2]}", size=12))
    return objects


# ---------- secret phrase entry ----------

# gets the secret phrase from the setter without showing it on screen
def get_phrase(win, setter, guesser):
    objects = []
    objects.append(make_text(win, WIDTH / 2, 150, f"Player {setter}, type a secret word or phrase",
                             size=20, style="bold"))
    objects.append(make_text(win, WIDTH / 2, 185, f"(Player {guesser}, look away!)", size=14, style="italic"))
    objects.append(make_text(win, WIDTH / 2, 215,
                             f"Letters and spaces only, up to {MAX_PHRASE_LENGTH} characters. Press Enter when done.",
                             size=11))

    box = Rectangle(Point(110, 250), Point(WIDTH - 110, 300))
    box.setFill("white")
    box.draw(win)
    objects.append(box)

    stars = make_text(win, WIDTH / 2, 275, "", size=20, face="courier")
    objects.append(stars)
    objects.append(make_text(win, WIDTH / 2, 365, "Typing not showing up? Click inside this window first.",
                             size=10, color="gray40"))
    warning = make_text(win, WIDTH / 2, 330, "", size=12, color="red")
    objects.append(warning)

    phrase = ""
    while True:
        kind, value = wait_for_input(win)
        if kind != "key":
            continue
        warning.setText("")

        if value == "Return":
            cleaned = " ".join(phrase.split())     # trims and collapses extra spaces
            if cleaned:
                undraw_all(objects)
                return cleaned
            warning.setText("Type at least one letter first.")
        elif value == "BackSpace":
            phrase = phrase[:-1]
        elif value == "space":
            if len(phrase) < MAX_PHRASE_LENGTH:
                phrase += " "
        elif len(value) == 1 and value.upper() in ALPHABET:
            if len(phrase) < MAX_PHRASE_LENGTH:
                phrase += value.upper()
            else:
                warning.setText("That's the maximum length.")

        # show a * for each letter so word lengths are clear without giving anything away
        stars.setText("".join("*" if letter != " " else " " for letter in phrase))


# ---------- gallows ----------

# draws the empty gallows and returns (frame pieces, body parts not yet drawn)
def draw_gallows(win):
    frame = [
        Line(Point(40, 350), Point(200, 350)),   # base
        Line(Point(80, 350), Point(80, 90)),     # post
        Line(Point(80, 90), Point(180, 90)),     # beam
        Line(Point(180, 90), Point(180, 120)),   # rope
    ]
    for piece in frame:
        piece.setWidth(4)
        piece.draw(win)

    body = [
        Circle(Point(180, 145), 25),               # head
        Line(Point(180, 170), Point(180, 255)),    # body
        Line(Point(180, 190), Point(145, 225)),    # left arm
        Line(Point(180, 190), Point(215, 225)),    # right arm
        Line(Point(180, 255), Point(150, 310)),    # left leg
        Line(Point(180, 255), Point(210, 310)),    # right leg
    ]
    for part in body:
        part.setWidth(3)
    return frame, body


# ---------- letter buttons ----------

def button_corners(index):
    row = index // 13
    col = index % 13
    x1 = BUTTON_LEFT + col * (BUTTON_SIZE + BUTTON_GAP)
    y1 = BUTTON_TOP + row * (BUTTON_SIZE + BUTTON_GAP)
    return x1, y1, x1 + BUTTON_SIZE, y1 + BUTTON_SIZE

# draws A-Z buttons; returns {letter: (rectangle, label)}
def draw_buttons(win):
    buttons = {}
    for index, letter in enumerate(ALPHABET):
        x1, y1, x2, y2 = button_corners(index)
        rect = Rectangle(Point(x1, y1), Point(x2, y2))
        rect.setFill("lightblue")
        rect.draw(win)
        label = make_text(win, (x1 + x2) / 2, (y1 + y2) / 2, letter, size=16, style="bold")
        buttons[letter] = (rect, label)
    return buttons

# returns the letter whose button contains the point, or None
def letter_at(point):
    for index, letter in enumerate(ALPHABET):
        x1, y1, x2, y2 = button_corners(index)
        if x1 <= point.getX() <= x2 and y1 <= point.getY() <= y2:
            return letter
    return None

# grays out a used letter; red if wrong, green if right
def mark_button(buttons, letter, correct):
    rect, label = buttons[letter]
    rect.setFill("palegreen" if correct else "salmon")
    label.setTextColor("gray40")

# gets a guess from a button click or a key press, ignoring used letters
def get_guess(win, used):
    while True:
        kind, value = wait_for_input(win)
        if kind == "click":
            letter = letter_at(value)
        elif len(value) == 1:
            letter = value.upper()
        else:
            letter = None
        if letter is not None and letter in ALPHABET and letter not in used:
            return letter


# ---------- one round ----------

# runs one round with `setter` choosing the phrase; returns True if the guesser won
def take_turn(win, round_number, setter, scores):
    guesser = 2 if setter == 1 else 1

    header = draw_header(win, round_number, setter, guesser, scores)
    phrase = get_phrase(win, setter, guesser)
    revealed = make_revealed(phrase)

    # build the board
    board = []
    frame, body = draw_gallows(win)
    board.extend(frame)
    board.append(make_text(win, 450, 110, "Mistakes", size=16, style="bold"))
    mistakes_text = make_text(win, 450, 145, "", size=16, face="courier", color="red")
    remaining_text = make_text(win, 450, 185, f"{MAX_MISTAKES} guesses left", size=12)
    phrase_size = 26 if len(phrase) <= 14 else 18
    phrase_text = make_text(win, WIDTH / 2, 385, format_revealed(revealed), size=phrase_size, face="courier",
                            style="bold")
    message = make_text(win, 450, 250, "Click a letter or type it", size=12, style="italic")
    board.extend([mistakes_text, remaining_text, phrase_text, message])
    buttons = draw_buttons(win)
    for rect, label in buttons.values():
        board.extend([rect, label])

    # initialize variables
    mistakes = 0
    wrong_guesses = []
    used = set()

    # game loop
    while mistakes < MAX_MISTAKES and not check_word(phrase, revealed):
        guess = get_guess(win, used)
        used.add(guess)

        correct = check_guess(phrase, guess, revealed)
        mark_button(buttons, guess, correct)

        # adds to mistake count and draws the next body part if wrong
        if not correct:
            body[mistakes].draw(win)
            board.append(body[mistakes])
            mistakes += 1
            wrong_guesses.append(guess)
            mistakes_text.setText(" ".join(wrong_guesses))
            left = MAX_MISTAKES - mistakes
            remaining_text.setText(f"{left} guess left" if left == 1 else f"{left} guesses left")

        phrase_text.setText(format_revealed(revealed))

    won = check_word(phrase, revealed)
    if won:
        scores[guesser] += 1
        message.setText(f"Great job, Player {guesser}!")
        message.setTextColor("darkgreen")
    else:
        phrase_text.setText(format_revealed(list(phrase)))
        phrase_text.setTextColor("red")
        message.setText(f"Good try, Player {guesser}.")
        message.setTextColor("red")
    message.setStyle("bold")
    message.setSize(16)
    board.append(make_text(win, 450, 285, "Click or press any key to continue", size=11))

    wait_to_continue(win)
    undraw_all(board)
    undraw_all(header)
    return won


# ---------- final screen ----------

def show_final_score(win, scores):
    if scores[1] > scores[2]:
        result = "Player 1 wins!"
    elif scores[2] > scores[1]:
        result = "Player 2 wins!"
    else:
        result = "It's a tie!"
    make_text(win, WIDTH / 2, 190, "Game over", size=28, style="bold")
    make_text(win, WIDTH / 2, 250, f"Player 1: {scores[1]}     Player 2: {scores[2]}", size=18)
    make_text(win, WIDTH / 2, 300, result, size=22, style="bold", color="darkgreen")
    make_text(win, WIDTH / 2, 370, "Click or press any key to close", size=12)
    wait_to_continue(win)


# macOS often leaves keyboard focus in the terminal when Python opens a window,
# so key presses never reach the game. This brings the window to the front and
# gives it focus, and clicking anywhere in the window grabs focus again.
def take_focus(win):
    try:
        if sys.platform == "darwin":
            os.system("osascript -e 'tell application \"System Events\" to set frontmost of "
                      "the first process whose unix id is %d to true' >/dev/null 2>&1" % os.getpid())
        win.master.lift()
        win.master.focus_force()
        win.focus_set()
        win.bind("<Button-1>", lambda event: win.focus_set(), add="+")
    except Exception:
        pass    # focus is a nice-to-have; the game still runs without it


def main():
    win = GraphWin("Hangman (Head-to-Head)", WIDTH, HEIGHT)
    win.setBackground("whitesmoke")
    take_focus(win)
    scores = {1: 0, 2: 0}
    try:
        take_turn(win, 1, 1, scores)    # Player 1 sets, Player 2 guesses
        take_turn(win, 2, 2, scores)    # Player 2 sets, Player 1 guesses
        show_final_score(win, scores)
        win.close()
    except GraphicsError:
        pass    # the window was closed early


if __name__ == "__main__":
    main()
