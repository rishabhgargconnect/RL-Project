"""
building the agent

FUNCTIONS -

STATES : 
is crashed (current episode ends)
is playing (continue with train/test)
will restart (start next episode)

ACTIONS : 
go left
go right
do nothing

OPTIONAL ADDITIONS :
fire bullets
if bullet wasted, negative rewards

"""

class GameAgent:

    # initialize the class
    def __init__(self,game_object):
        self.spaceGame = game_object
        self.no_movement()

    # define functions to check the state of agent
    def is_alive(self):
        return self.spaceGame.get_alive()
    def is_dead(self):
        return self.spaceGame.get_dead()

    # define functions to perform actions using spaceGame object
    def go_left(self):
        self.spaceGame.press_left()
    def go_right(self):
        self.spaceGame.press_right()
    def no_movement(self):
        self.spaceGame.no_action()
    