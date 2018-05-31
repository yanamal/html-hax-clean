# html-hax
This is a web-based game where players learn about HTML by "hacking" web pages to solve puzzles.

It is an [App Engine](https://cloud.google.com/appengine/) app, using the [Flask](http://flask.pocoo.org/) library.

## Changes since release 0.2

### Auto-passphrase style puzzle
[This commit](https://github.com/yanamal/html-hax-clean/commit/96c5d4e59e79ae99a6d161bd90d5ee687da8b240) adds the main type of puzzle that html-hax will use: the puzzle asks the player to figure out the current passphrase, but the passphrase is automatically randomly chosen from a list every time the user loads a puzzle.

This way, it's much harder to just guess, and the user will have to figure out what the passphrase is by examining the HTML source of the puzzle itself. The very first puzzle simply lists the passphrase in a comment right at the top of its own source. So the user just needs to be able to open the browser's development tools and look at the HTML source.

The passphrases are generated and checked on the server side, in `main.py`, and stored in the user's profile. The autopass structure assumes that the password guess will always be submitted as the parameter `pass` in a request to the given puzzle's page.

The current "correct" passphrase that the user is trying to guess is stored in the user's profile.

### Puzzle Sequencing
[This commit](https://github.com/yanamal/html-hax-clean/commit/f9914184c0b97ff7b6c0005e837f29dc1a56b908) adds the logic and structure for defining the sequence of puzzles the user is meant to go through:

`data/puzzleSequence.json` is a simple json data structure with a sequence of puzzle URLs.

each time a user solves a puzzle in that sequence, the code in `puzzleSequenceLogic.py` look at that data file, and returns the next puzzle in the sequence.

The logic for each type of puzzle (which is just the auto-passphrase type, for now) is responsible for calling the `userCompletedPuzzle` function in `puzzleSequenceLogic.py` when the user completes the puzzle, and then passing the generated completion message on to the user.

### Puzzle content
There are now 5 puzzles that should introduce the user to the basics of HTML structure, and to the practice of using their browser to examine and manipulate HTML.

[This](https://github.com/yanamal/html-hax-clean/commit/56fb7cced0d7ee2dabf0bae43edd938ddca30dd2) is a commit which just adds one puzzle, so it is a good example to look at to understand what you need to do to add a puzzle.
