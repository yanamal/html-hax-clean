#!/usr/bin/env python

# import libraries:
import logging, os
import json
import random

from google.appengine.api import users
from flask import Flask,request,render_template

# Import code from our own files:
from user import UserProfile
from puzzleSequenceLogic import userCompletedPuzzle

# make the flask app:
app = Flask(__name__)

# Set up debug/error logging, when not running "for real" on Google App Engine:
if not os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/'):
    app.debug = True  # with this setting on, the cause of Python errors is displayed in App Engine logs.

@app.route('/')
def hello():
    return render_template('hello.html', name=users.get_current_user().nickname())

# when the user navigates to an autopass puzzle, either display the puzzle,
# or (if they are submitting a correct solution) tell them that they are correct.
@app.route('/autopass/<puzzle>')
def render_autopass_puzzle(puzzle):
    # get current user's profile:
    profile = UserProfile.get_by_user(users.get_current_user())

    # get passphrase that was submitted with this request, if any:
    submitted = request.args.get('pass')
    # if they submitted the correct passphrase:
    if submitted and (submitted == profile.current_passphrase):
        # use the current puzzle's path to record the puzzle completion, and return the generated message:
        return userCompletedPuzzle(request.path)


    # The following will only happen when the previous "if" was false, and so we did not return "correct"
    # In other words, from here, we can assume that the correct password was NOT submitted.

    # generate a new passphrase:
    passphrase = 'default' # temporary default passphrase, just in case loading one from file fails.
    with app.open_resource('data/passphrases.json') as f:
        passphrases = json.load(f)
        passphrase = random.choice(passphrases)

    # store it in user's profile:
    profile.current_passphrase = passphrase
    profile.put()

    return render_template('autopass/'+puzzle, passphrase=passphrase)
