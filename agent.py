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


class DinoAgent:
    def __init__(self,game):
        self.dinoGame = game; 
        self.jump(); 
    def is_running(self):
        return self.dinoGame.get_playing()
    def is_crashed(self):
        return self.dinoGame.get_crashed()
    def jump(self):
        self.dinoGame.press_up()
    def duck(self):
        self.dinoGame.press_down()
    def DoNothing(self):
        self.dinoGame.press_right()

"""

class GameAgent:
    def __init__(self,game_object):
        self.spaceGame = game_object
        self.noMovement()
    def is_alive(self):
        return self.spaceGame.get_alive()
    def is_dead(self):
        
    