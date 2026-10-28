# Hangman Changes for Partner Review

Branch: `development`  
Code commit: [`02d8b63`](https://github.com/tatejones2/cscn345_lab8_ideas/commit/02d8b63)

## Changes to `hangman.py`

### 1. Keep playing after both players take a turn

Previously, the program ran two rounds and ended:

```python
take_turn(1)
take_turn(2)
```

Now, a `while True` loop keeps alternating between players until someone enters the quit command.

### 2. Keep a running scoreboard

The scoreboard is initialized once, before the main loop, so scores carry over between rounds:

```python
scoreboard = {1: 0, 2: 0}

while True:
    if take_turn(1):  # Player 2 guesses
        scoreboard[2] += 1

    show_scoreboard(scoreboard)

    if take_turn(2):  # Player 1 guesses
        scoreboard[1] += 1

    show_scoreboard(scoreboard)
```

`take_turn()` returns `True` when the guesser wins and `False` after six mistakes. A successful guesser earns one point. A loss awards no points. Scores reset when the program restarts.

The new `show_scoreboard()` function displays both totals after every completed round:

```python
def show_scoreboard(scoreboard):
    print("\nScoreboard:\n")
    print(f"Player 1: {scoreboard[1]} | Player 2: {scoreboard[2]}\n")
```

### 3. Add a quit command

The secret phrase prompt now tells the setter to enter `XXXX` to quit. After reading the phrase, `take_turn()` checks for that command:

```python
if phrase == "XXXX":
    print("\nThanks for playing!\n")
    exit()
```

The input is converted to uppercase, so `xxxx` also works. This command applies when entering the secret phrase.

## Implementation note

`take_turn()` also contains local `player1_score` and `player2_score` variables that reset each round. They do not control the displayed totals. The persistent `scoreboard` dictionary in the main loop controls those totals; the local counters are redundant and could be removed in a future cleanup.

## Related repository changes

The remote development branch already removed `graphics.py` and `hangman_gui (1).py` in separate commits. The current game uses the terminal interface in `hangman.py`.

## Verification

A scripted check simulated four successful rounds, alternating guessers. The displayed totals reached `Player 1: 2 | Player 2: 2`, confirming that scores persist across rounds. Entering `XXXX` then exited successfully and printed the goodbye message.
