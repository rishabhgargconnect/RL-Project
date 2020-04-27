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
# import torch
# import torch.nn as nn
# import torch.optim as optim
import cv2
from keras.layers import Dense
from keras.models import Sequential
from scipy.special import softmax
import numpy as np
from keras.optimizers import Adam
from keras.losses import huber_loss
import random
#Note: #32 states send to NN, each state has 4 images

class SpaceShooterDQN:

    def __init__(self, game):
        #Objects
        self.game = game
        self.actions_count = 3
        self.replay_memory_size = 10000
        self.replay_memory = []
        self.alpha = 0.2
        self.epsilon = 0.1
        self.gamma = 0.95
        self.batch_size = 64
        self.layers = [32]
        self.update_target_estimator_every = 100

        
        #TODO
        self.state_size = (84,84)
        self.model = self.build_model()
        self.target_model = self.build_model()


    def build_model(self):
        model = Sequential()
        model.add(Dense(4, input_shape=self.state_size, activation='relu'))

        
        for l in self.layers:
            model.add(Dense(l, activation='relu'))
        
        model.add(Dense(self.actions_count, activation='linear'))
        
        model.compile(loss=huber_loss,
                      optimizer=Adam(lr=self.alpha))
        return model


    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())  



    def get_epsilon_greedy_policy(self, state):
        
        print('length = ',len(state))
        act_vals = None
        rand_num = np.random.random_sample()

        if(rand_num<self.epsilon):
            act_vals = np.random.rand(self.actions_count)
        else:
            act_vals = self.model.predict(np.array(state))
            print('act_vals = ', act_vals)

        return softmax(act_vals)                



    def train_network(self):    

  
        state = [self.game.preprocess_screenshot(self.game.get_screenshot())[0]]*4
        is_done = False
        memory = []
        
        #TODO: Doubtful if C should be here or globally
        C=0
        

        while(is_done==False):
            action_to_take = self.get_epsilon_greedy_policy(state)
            actions = np.zeros((3))
            actions[np.argmax(action_to_take)] = 1
            next_state, reward, is_done = self.game.perform_one_step(actions)
            next_state_consecutive = state[1:]
            next_state_consecutive.append(next_state)
            memory.append((state,np.argmax(action_to_take),reward,next_state, is_done))



            memory_batch = random.choices(memory,k=self.batch_size)
            states_batch = [x[0] for x in memory_batch]
            actions_batch = [x[1] for x in memory_batch]
            rewards_batch = [x[2] for x in memory_batch]

            q_vals_batch = self.model.predict(np.array(states_batch), batch_size=32)

            for i in range(0, len(memory_batch)-1):
                reward = rewards_batch[i]
                very_next_state = np.array(states_batch[i+1])
                # print('very_next_state len = ', len(very_next_state))
                very_next_state_q_vals = self.target_model.predict(very_next_state)

                # print('very_next_state = ', very_next_state)
                # print( 'very_next_state_q_vals = ', very_next_state_q_vals[0])
                print('q_vals_batch[i] = ', q_vals_batch[i])
                print('actions_batch[i] = ' ,actions_batch[i])

                q_vals_batch[i][actions_batch[i]] = reward + self.gamma*max(very_next_state_q_vals[0])



            self.model.fit(np.array(states_batch[0][0]), np.array(q_vals_batch))     



            state = next_state_consecutive
            C+=1
            if(C == self.update_target_estimator_every):
                self.update_target_model()
                self.C=0            


    # def test_network(self):     




    # def init_weights(self):           





    # def reset_environment():
    #     #Code to restart game  