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
  
from matplotlib import pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import time
import copy
import sys

high_score = 0
q_max_vals_list = []
scores_list = []
episode_length_list = []
reward_list = []
args = sys.argv

model_folder = args[2]
def train_network(model,target_model,start):        
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.MSELoss()
    game = SpaceShooterGame()
    replay_memory = []
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[1] = 1
    game.perform_one_step(action)
    image_data = game.preprocess_screenshot(game.get_screenshot())
    #stacking 4 images
    state = torch.cat((image_data, image_data, image_data, image_data)).unsqueeze(0) 
    epsilon = model.initial_epsilon
    iteration = 0
    score_past = game.score
    high_score=0
    epsilon_decrements = np.linspace(model.initial_epsilon, model.final_epsilon,model.number_of_iterations)
    global q_max_vals_list
    global scores_list
    global episode_length_list
    global reward_list 
    count_episode_length = 0
    count_episode_reward = 0
    count_episode_q_max = 0
    while iteration < model.number_of_iterations:
        if game.game_over:
            print(q_max_vals_list,scores_list,episode_length_list,reward_list)
            q_max_vals_list.append(count_episode_q_max)
            scores_list.append(game.score)
            episode_length_list.append(count_episode_length)
            reward_list.append(count_episode_reward)
            count_episode_length = 0
            count_episode_reward = 0
            count_episode_q_max = 0
            if high_score < game.score:
                high_score = game.score
            game = SpaceShooterGame()
            score_past = 0

        # taking output from model
        output = model(state)[0]
        # print(action)
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
        # terminal
        terminal = game.game_over
        # reward
        reward = game.get_reward()
        # of score is same make reward 0
        if game.score == score_past:
            reward = 0
        if(terminal):
            reward = -100
        # print('reward =', reward)    
        # if game.score > score_past:
        #     reward = 1
        # if terminal:
        #     reward = -10
        reward = torch.from_numpy(np.array([reward], dtype=np.float32)).unsqueeze(0)
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
        output_1_target_model_batch = target_model(state_1_batch)
        output_1_model_batch = target_model(state_1_batch)
        # print('max index = ',torch.argmax(output_1_model_batch[0]))
        # print('vector = ',output_1_target_model_batch[0])
        # print('max vector = ',output_1_target_model_batch[0][torch.argmax(output_1_model_batch[0])])
        # form the actual labels, using the next state vals
        y_batch = torch.cat(tuple(reward_batch[i] if minibatch[i][4]
                                  else reward_batch[i] + model.gamma * 
                                  output_1_target_model_batch[i][torch.argmax(output_1_model_batch[i])]
                                  for i in range(len(minibatch))))
        # form the predicted vals using states
        q_value = torch.sum(model(state_batch) * action_batch, dim=1)
        optimizer.zero_grad()
        y_batch = y_batch.detach()
        # loss
        loss = criterion(q_value, y_batch)
        loss.backward()
        optimizer.step()
        # assign next state to state, change score
        state = state_1
        score_past = game.score
        # game.quit_game()

        if iteration % model.C==0:
            # print('model copied')
            # print('model = ',list(model.parameters()))
            # print('target model = ',list(target_model.parameters()))
            target_model = copy.deepcopy(model)
            # print('after model = ',list(model.parameters()))
            # print('after target model = ',list(target_model.parameters()))
        
        # save model , display result
        if iteration % 1000 == 0:
            print("iteration:", iteration, "score:", game.score, "past score:",score_past, "high_score:", high_score, "elapsed time:", time.time() - start, "epsilon:", epsilon, "action:",
                  action_index.cpu().detach().numpy(), "reward:", reward.numpy()[0][0], "Q max:",
                  np.max(output.cpu().detach().numpy()))
        
        count_episode_length+=1
        count_episode_q_max+=np.max(output.cpu().detach().numpy())
        count_episode_reward+=reward.numpy()[0][0]
        
        # if reward == -10:
        #     print('GAME OVER PUNISHMENT')
        # if reward == 1:
        #     print('REWARD FOR KILL')

        if iteration % 10000 == 0:
            torch.save(target_model, model_folder+"/current_model_" + str(iteration) + ".pth")

        iteration += 1


def test_network(model):  
    game = SpaceShooterGame()
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[1] = 1
    game.perform_one_step(action)
    image_data = game.preprocess_screenshot(game.get_screenshot())
    state = torch.cat((image_data, image_data, image_data, image_data)).unsqueeze(0) 
    while not game.game_over:
        # if game.game_over:
        #     if game.high_score < game.score:
        #         game.high_score = game.score
        #     game = SpaceShooterGame()
        #     score_past = 0
        # taking output from model
        output = model(state)[0]
        action = torch.zeros([model.number_of_actions], dtype=torch.float32) 
        # action
        action_index = torch.argmax(output)
        action[action_index] = 1
        game.perform_one_step(action)
        # state
        image_data_1 = game.preprocess_screenshot(game.get_screenshot())
        state_1 = torch.cat((state.squeeze(0)[1:, :, :], image_data_1)).unsqueeze(0)
        state = state_1
        # game.quit_game()
    return game.score
        
def init_weights(m):
    if type(m) == nn.Conv2d or type(m) == nn.Linear:
        torch.nn.init.uniform(m.weight, -0.01, 0.01)
        m.bias.data.fill_(0.01)



if not os.path.exists(model_folder+'/'):
    os.mkdir(model_folder+'/')


mode = args[1]

if mode=='train':
    model = NeuralNetwork()
    target_model = NeuralNetwork()
    model.apply(init_weights)
    target_model.apply(init_weights)
    # init_weights(model)
    start = time.time()
    train_network(model,target_model, start)
    print(q_max_vals_list)
    plt.plot(range(len(q_max_vals_list)),q_max_vals_list)
    plt.xlabel('episode')
    plt.ylabel('Q max Values')
    plt.legend('Plot for Episode and Q max values')
    plt.savefig(model_folder+'/q_val.png')
    plt.show()
    print(reward_list)
    plt.plot(range(len(reward_list)),reward_list)
    plt.xlabel('episode')
    plt.ylabel('rewards')
    plt.legend('Plot for Episode and Total Reward')
    plt.savefig(model_folder+'/reward.png')
    plt.show()
    print(scores_list)
    plt.plot(range(len(scores_list)),scores_list)
    plt.xlabel('episode')
    plt.ylabel('scores')
    plt.legend('Plot for Episode and score')
    plt.savefig(model_folder+'/score.png')
    plt.show()
    print(episode_length_list)
    plt.plot(range(len(episode_length_list)),episode_length_list)
    plt.xlabel('episode')
    plt.ylabel('episode length')
    plt.legend('Plot for Episode and episode length')
    plt.savefig(model_folder+'/length.png')
    plt.show()


# iterations = range(100000,200000,10000)
iterations = [150000,200000]
if mode=='test':
    for iter in iterations:
        final_score = 0
        max = 0
        for i in range(100):
            model = torch.load(model_folder+'/current_model_'+str(iter)+'.pth').eval()
            score = test_network(model)
            final_score+= score
            if score>max:
                max = score
        print('average score = ',final_score/100)
        print('high score = ',max)


# for i in range(2):
#     # no need for restart, just make object for the game class again and run it
#     game = SpaceShooterGame()
#     while game.get_game_over()==False:
#         actions = np.zeros((3))
#         actions[random.choice([0,1,2])]=1
#         # actions[2]=1
#         game.perform_one_step(actions)
#         input_image = game.get_screenshot()
#         game.preprocess_screenshot(input_image)
#         game.quit_game()
#     print('The end')
#         # pygame.display.update()
#     # game.restart_game()
