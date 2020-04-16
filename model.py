"""
*define model layers(input can be an array of say 4 screenshots, or maybe we can increase input neurons count to 4 times)

*train model
1. choose action based on policy
2. call step function in while loop based on number of episodes needed 
3. feed input(state, reward?) and output(action) to  model for training
4. save model ater cetain iterations

*test model
1.calls model for taking actions
2.using this action, retrieve the next state
loop through 1 and 2 and keep track of high score as of now

*main method
- modes for train, test or play

*Tune:
1. layers count and neurons per layer count
2. dropout rate
3. batch size
4. epsilon
5. alpha

"""

import torch
import torch.nn as nn
import torch.optim as optim
import cv2
import numpy as np
import random
from original_game_class import SpaceShooterGame


class NeuralNetwork(nn.Module):
    
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.number_of_actions = 3
        self.gamma = 0.5
        self.final_epsilon = 0.0001
        self.initial_epsilon = 0.9
        self.number_of_iterations = 100001
        self.replay_memory_size = 10000
        self.minibatch_size = 32

        self.conv1 = nn.Conv2d(4, 32, 8, 4)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(32, 64, 4, 2)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv2d(64, 64, 3, 1)
        self.relu3 = nn.ReLU(inplace=True)
        self.fc4 = nn.Linear(3136, 512)
        self.relu4 = nn.ReLU(inplace=True)
        self.fc5 = nn.Linear(512 , self.number_of_actions)

    def forward(self, x):
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)
        out = self.relu3(out)
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = self.relu4(out)
        out = self.fc5(out)

        return out
