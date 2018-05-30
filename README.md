# html-hax
This will be a web-based game where players learn about HTML by "hacking" web pages to solve puzzles.

This is an [App Engine](https://cloud.google.com/appengine/) app, using the [Flask](http://flask.pocoo.org/) library.

## Changes since release 0.2

### Auto-passphrase style puzzle
This commit adds the main type of puzzle that html-hax will use: the puzzle asks the player to figure out the current passphrase, but the passphrase is automatically randomly chosen from a list every time the user loads a puzzle.

This way, it's much harder to just guess, and the user will have to figure out what the passphrase is by examining the HTML source of the puzzle itself. The very first puzzle simply lists the passphrase in a comment right at the top of its own source. So the user just needs to be able to open the browser's development tools and look at the HTML source.

The passphrases are generated and checked on the server side, in `main.py`, and stored in the user's profile. The autopass structure assumes that the password guess will always be submitted as the parameter `pass` in a request to the given puzzle's page.

The current "correct" passphrase that the user is trying to guess is stored in the user's profile.
