# Learning to be a Space Shooter Bot : Simulating a game using Deep Reinforcement Learning

In this work, a Deep Reinforcement Learning bot is trained to kill aliens in a custom Space Shooter game.  The objective of the bot is to kill aliens using bullets, which will serve as a positive reward for the bot. If the bot dies by collision with alien or if alien crosses the game over boundary, a negative reward will be assigned to the bot. The bot is tested by tuning parameters of the model as well as the game environment. The results obtained show significant improvement in behavior of the bot and it is observed to perform comparable to a human player.

### Code Description

<b>trained-model folders</b> : All the trained-model folders contain the Deep Q-Networks trained for this project.<br>
<b>original_game.py</b> : This file contains the game originally created to be played by a human player.<br>
<b>original_game_class.py</b> : Modified version of the game, which is used by the bot to play the game. Game parameters like speed of aliens, player and bullet, number of aliens, rewards, etc. can be tuned in this file.<br>
<b>model.py</b> : Deep Neural Network is defined. Model parameters like epsilon, gamma, batch size, C, etc. can be tuned in this file. <br>
<b>main_DQN_with_target.py</b> : DQN (Deep Q-Network) implementation using the current and target model.<br>
<b>main_DDQN_with_target.py</b> : DDQN (Double Deep-Q Network) implementation using the current and target model.<br>

### How to run the code : 
1. Clone the project using : ' git clone https://github.com/rishabhgargconnect/RL-Project.git ' <br>
2. Run 'git checkout master' from the terminal. (optional) <br>
3. Syntax of command to run python files : 'python filename arg1 arg2' <br>
where , <br>
<b>filename</b> = 'main_DQN_with_target.py' to run Deep Q-Network and  filename = 'main_DDQN_with_target.py'  to run Double Deep Q-Network.<br>
<b>arg1</b> = 'train' to train the models (after choosing the required parameters) and arg1 = 'test' to test the model. <br>
<b>arg2</b> refers to the model path. For eg: 'trained-model-ddqn-g0.99-b32-C100-e0.1_DONE' to train/test the DDQN model with gamma =0.99, batch size 32, C=100 and Epsilon = 0.1.<br>

Sample Command:<br>
<b> python main_DDQN_with_target.py test trained-model-ddqn-g0.99-b32-C100-e0.1_DONE</b>

### Useful links

Link to the presentation : https://docs.google.com/presentation/d/1D648ZiN4Xq99z6Nas_p9rVewA3zQmLMoBguTfKOmXXY/edit#slide=id.g845012c340_1_31

Link to the youtube video : https://www.youtube.com/watch?v=HvfSGqtO1VU

