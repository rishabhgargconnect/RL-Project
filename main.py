"""
processing for a single game state step

STEPS :
1. preprocess image screenshot
2. take screenshot
3. take state
4. take random action
5. get the reward (initially 0, check for collision to calculate reward value)
6. returns done true or false

"""

"""

building the game

FUNCTIONS -

STATES : 
crashed
playing
restart

ACTIONS : 
left
right
nothing

TUNING :
change in rewards (like give reward to stay alive)
bullet speed
number of aliens
player speed
speed of aliens
change in speed of aliens 

REST : 
score
high score
quit

OPTIONAL ADDITIONS :
random powers or bullet type in rewards (depending on scores/number of aliens killed)
segregate game into levels (depending on scores/number of aliens killed)
in case of manual firing - limit the bullets, collect bullet powers or refil in each level

"""

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


import pygame
import numpy as np
import random
from original_game_class import SpaceShooterGame

game = SpaceShooterGame()

while game.get_game_over()==False:
    actions = np.zeros((3))
    actions[random.choice([0,1,2])]=1
    # actions[2]=1

    game.perform_one_step(actions)
    game.quit_game()
    # pygame.display.update()
