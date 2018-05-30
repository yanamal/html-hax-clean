import json, logging
from google.appengine.api import users
from flask import Flask

from user import UserProfile

app = Flask(__name__)

# given the name of a puzzle the user has just completed,
# generate a completion message for the user (as a short HTML snippet).
# The message includes a link to the next puzzle they should do, if any.
def userCompletedPuzzle(puzzle):
    message = 'correct! ' # start composing the message displayed to the user.
    nextPuzzle = getNextPuzzle(puzzle) # use the current puzzle's path to get the puzzle that should be next.
    if nextPuzzle:
        # if there is a next puzzle, then link to it
        message += '<a href='+nextPuzzle+'>Next puzzle!</a>'
    else:
        # if there is not a next puzzle, tell the user they are all done
        message += 'All done!'
    return message

# given the name of the current puzzle,
# decide what the next puzzle should be.
def getNextPuzzle(curr):
    with app.open_resource('data/puzzleSequence.json') as f:
        puzzles = json.load(f)
        nextp = puzzles[0] # default value: if we can't figure out the proper next puzzle, we'll just return the first one.
        if curr and (curr in puzzles):
            i = puzzles.index(curr) # This isn't very efficient, but anything nicer would require a more complex puzzleSequence data structure.
            if (i+1) >= len(puzzles):
                return None # if this was the last puzzle, you're done!
            nextp = puzzles[i+1]
        return nextp
