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
import os
from model import NeuralNetwork

import torch
import torch.nn as nn
import torch.optim as optim
import time


mode = 'train'

if mode == 'train':
    if not os.path.exists('pretrained-model/'):
        os.mkdir('pretrained-model/')

    model = NeuralNetwork()

    model.apply(init_weights)
    start = time.time()

    train_network(model, start)




def init_weights(m):
    if type(m) == nn.Conv2d or type(m) == nn.Linear:
        torch.nn.init.uniform(m.weight, -0.01, 0.01)
        m.bias.data.fill_(0.01)

def train_network(model,start):        
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.MSELoss()
    game = SpaceShooterGame()
    replay_memory = []
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[0] = 1
    game.perform_one_step(action)
    image_data = game.preprocess_screenshot(game.get_screenshot())
    #stacking 4 images
    state = torch.cat((image_data, image_data, image_data, image_data)).unsqueeze(0) 
    epsilon = model.initial_epsilon
    iteration = 0
    score_past = game.score
    epsilon_decrements = np.linspace(model.initial_epsilon, model.final_epsilon,model.number_of_iterations)
    while iteration < model.number_of_iterations:
        if game.game_over:
            if game.high_score < game.score:
                game.high_score = game.score
            game = SpaceShooterGame()
        # taking output from model
        output = model(state)[0]
        action = torch.zeros([model.number_of_actions], dtype=torch.float32)
        # epsilon-greedy policy for actions 
        random_action = random.random() <= epsilon
        action_index = [torch.randint(model.number_of_actions, torch.Size([]), dtype=torch.int)
                        if random_action
                        else torch.argmax(output)][0]
        # action
        action[action_index] = 1
        game.perform_one_step(action)
        # state
        image_data_1 = game.preprocess_screenshot(game.get_screenshot())
        state_1 = torch.cat((state.squeeze(0)[1:, :, :], image_data_1)).unsqueeze(0)
        action = action.unsqueeze(0)
        # reward
        reward = 0
        if game.score > score_past:
            reward = 1
        score_past = game.score
        reward = torch.from_numpy(np.array([reward], dtype=np.float32)).unsqueeze(0)
        # terminal
        terminal = game.game_over
        replay_memory.append((state, action, reward, state_1, terminal))
        # check length of replay memory
        if len(replay_memory) > model.replay_memory_size:
            replay_memory.pop(0)
        # select batch from replay memory
        epsilon = epsilon_decrements[iteration]
        minibatch = random.sample(replay_memory, min(len(replay_memory), model.minibatch_size))
        state_batch = torch.cat(tuple(d[0] for d in minibatch))
        action_batch = torch.cat(tuple(d[1] for d in minibatch))
        reward_batch = torch.cat(tuple(d[2] for d in minibatch))
        state_1_batch = torch.cat(tuple(d[3] for d in minibatch))
        # take output for next state 
        output_1_batch = model(state_1_batch)
        # form the actual labels, using the next state vals
        y_batch = torch.cat(tuple(reward_batch[i] if minibatch[i][4]
                                  else reward_batch[i] + model.gamma * torch.max(output_1_batch[i])
                                  for i in range(len(minibatch))))
        # form the predicted vals using states
        q_value = torch.sum(model(state_batch) * action_batch, dim=1)
        optimizer.zero_grad()
        y_batch = y_batch.detach()
        # loss
        loss = criterion(q_value, y_batch)
        loss.backward()
        optimizer.step()
        # assign next state to state
        state = state_1
        # save model , display result
        if iteration % 1000 == 0:
            print("iteration:", iteration, "score:", game.score, "high_score:", high_score, "elapsed time:", time.time() - start, "epsilon:", epsilon, "action:",
                  action_index.cpu().detach().numpy(), "reward:", reward.numpy()[0][0], "Q max:",
                  np.max(output.cpu().detach().numpy()), "avg_score:", avg_score)

            generation_score = []

        if iteration % 100000 == 0:
            torch.save(model, "pretrained-model/current_model_" + str(iteration) + ".pth")

        iteration += 1

# def test_network(self):     



for i in range(2):
    # no need for restart, just make object for the game class again and run it
    game = SpaceShooterGame()
    while game.get_game_over()==False:
        actions = np.zeros((3))
        actions[random.choice([0,1,2])]=1
        # actions[2]=1
        game.perform_one_step(actions)
        input_image = game.get_screenshot()
        game.preprocess_screenshot(input_image)
        game.quit_game()
    print('The end')
        # pygame.display.update()
    # game.restart_game()
