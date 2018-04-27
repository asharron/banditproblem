#This file uses the incremental approach to calculating
# Q values AND also uses upper bound confidence to choose
# new actions based on uncertainty and degree of exploration

import numpy as np
import random
import math

randomint = random.randint(1,51) #How many actions we will have between 1 - 50
rewards = np.random.rand(1,randomint) #Rewards for each action set randomly
best_action = max(rewards[0]) #Find the best reward

print("Total choices are ", randomint, "!")

#Table for holding our progress so far, Col index is the action number
# Row 1: Total reward for each action
# Row 2: Total number of times called
# Row 3: Old Q value
table = np.zeros((3,randomint))

c = .5 #Degree of exploration
total_reward = 0 

#This is the equation for determining the value of an action
def q_equation(total_reward, total_called):
    return total_reward * total_called

#Equation for upper confidence bound slection
# c * sqrt(ln(t) / number_of_times_called)
def upper_selection(c, t, num_called):
    #Exception handling for 0 division
    # And log(0)
    try:
        uncertainty = math.log(t) / float(num_called)
    except:
        try:
            uncertainty = math.log(t)
        except:
            uncertainty = math.log(t+1)

    return (c * math.sqrt(uncertainty))

#Loop for any number of times to allow the agent to try and pick
for attempt in range(10000):

    #Equation is action = argmax(Qt(a))
    #Get the current action by greedily picking the max of the q_equation applied to
    # each reward and value in the table
    curr_action = max([(qvalue + upper_selection(c,attempt,table[1][index]) ,index) for index, qvalue in\
                        enumerate(table[2])])

    curr_reward = rewards[0][curr_action[1]] #Grab reward from rewards table 

    #Update the table
    table[0][curr_action[1]] = curr_reward #Just remember the nth reward
    table[1][curr_action[1]] += 1 #update number of times called
    #The new q value equation is:
    # Qn+1 = Qn + 1/n[Rn - Qn]
    # OR
    # Qn+1 = Qn + a[Rn - Qn]
    # ^ If using a fixed n timestep ratio
    old_q = table[2][curr_action[1]]  #Helper for indexing
    #First equation
    table[2][curr_action[1]] = old_q + (1/table[1][curr_action[1]]) * \
        (curr_reward - old_q) #Update the q value for this action
    #Second equation
    #table[2][curr_action[1]] = old_q + (1/table[1][curr_action[1]]) * \
        #(curr_reward - old_q) #Update the q value for this action

    #Update total reward
    total_reward += curr_reward

#Grab what the machine thinks is the best option overall
guess_best = max([(q_equation(tReward,tCalls),index) for index,\
                       (tReward,tCalls) in \
                       enumerate(zip(table[0],table[1]))])

print("Total reward was ", total_reward, "!")
print("Our AI thinks that the best choice is ", guess_best[1]+1, "!")

if rewards[0][guess_best[1]] == best_action:
    print("Our AI was correct!")
else:
    print("Dang, it was wrong...")
    
