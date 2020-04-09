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