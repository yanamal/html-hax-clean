import json

# Use the NDB database structure that's integrated into App Engine.
from google.appengine.ext import ndb

from flask import Flask

app = Flask(__name__)

# class representing User Profile data that's specific to this application:
class UserProfile(ndb.Model):
    user_email = ndb.StringProperty() # record the user's email, as specified by their Google log in.
    current_passphrase = ndb.StringProperty() # The randomly-assigned passphrase that the user is currently trying to guess
    current_puzzle = ndb.StringProperty() # the current puzzle that the user is working on
    solved_puzzles = ndb.StringProperty(repeated=True) # all the puzzles that the user has solved

    # retrieve (or automatically create) user profile for the given App Engine user object.
    @classmethod
    def get_by_user(cls, user):
        # cls is just a reference to the UserProfile class
        profile = cls.get_by_id(user.user_id())
        # automatically create blank profile if user doesn't already exist
        if not profile:
            with app.open_resource('data/puzzleSequence.json') as f:
                puzzles = json.load(f) # get the puzzle sequence from the data file puzzleSequence.json
                profile = UserProfile(user_email = user.email(),
                                      current_puzzle = puzzles[0], # for a new user, the first puzzle is the current puzzle
                                      solved_puzzles = [], # for a new user, the list of solved puzzles is empty.
                                      id=user.user_id() )
                # The special 'id' parameter sets the unique key for that entry in the NDB database.
                # We want one entry per user, so we use the user id as the unique key.
                # This is also why get_by_id above works: we know that the NDB id and the AppEngine User id are the same.
                profile.put()
        return profile
