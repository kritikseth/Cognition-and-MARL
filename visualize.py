import sys
import random
import time
from tqdm import trange

import pygame
import matplotlib.pyplot as plt

import numpy as np

from RushHour4.core import Map, Environment
from RushHour4.interact import FourAgentGame, visualize, load_image_objects
from RushHour4.utils import *

import pickle

ROWS, COLS = 8, 8
EPISODES = 10000
MOVE_PENALTY = 1
COLLISION_PENALTY = 100
CATCH_REWARD = 400
STEPS = 400

EPSILON = 0.0
EPS_DECAY = 0.9999965
LEARNING_RATE = 0.1
DISCOUNT = 0.95

SHOW = False
SHOW_EVERY = 1
blockSize = 100

model_type = 'common'
# model_type = 'separate'
if len(sys.argv) == 2:
    model_type = sys.argv[1]
if len(sys.argv) == 3:
    if sys.argv[2] == 'show':
        SHOW = True
        EPISODES = 10

if SHOW:
    global screen, CLOCK
    agent, action = None, None
    pygame.init()
    screen = pygame.display.set_mode((blockSize * COLS, blockSize * ROWS))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    pyimage_objects = load_image_objects()

mymap = Map(ROWS, COLS)
game = FourAgentGame(mymap, blockSize)


if model_type == 'common':
    start_q_table1 = 'Models/qtable_common.pickle' # None or Filename
    with open(start_q_table1, 'rb') as f:
        q_table1 = pickle.load(f)
        q_table2 = q_table1
        q_table3 = q_table1
elif model_type == 'separate':
    start_q_table1 = 'Models/qtable_1.pickle' # None or Filename
    start_q_table2 = 'Models/qtable_2.pickle' # None or Filename
    start_q_table3 = 'Models/qtable_3.pickle' # None or Filename
    with open(start_q_table1, 'rb') as f:
        q_table1 = pickle.load(f)
    with open(start_q_table2, 'rb') as f:
        q_table2 = pickle.load(f)
    with open(start_q_table3, 'rb') as f:
        q_table3 = pickle.load(f)
         
action_direction = ['up', 'down', 'left', 'right']


episode_rewards = []
catch_count1 = 0
catch_count2 = 0
catch_count3 = 0

progress = trange(EPISODES)
for episode in progress:

    game.initialize()
    game.setup_agents({'1': game.random_state()})
    game.setup_agents({'2': game.random_state()})
    game.setup_agents({'3': game.random_state()})
    game.setup_agents({'x': game.random_state()})

    episode_reward = 0
    cop1_caught = 0
    cop2_caught = 0
    cop3_caught = 0

    cop1_pos = game.locate_agent('1')
    cop2_pos = game.locate_agent('2')
    cop3_pos = game.locate_agent('3')
    thief_pos = game.locate_agent('x')
    cop1_state, cop2_state, cop3_state = get_cop_states(cop1_pos, cop2_pos, cop3_pos, thief_pos)

    for i in range(STEPS):
        cop1_direction = perform_action(cop1_state, q_table1, EPSILON)
        cop2_direction = perform_action(cop2_state, q_table2, EPSILON)
        cop3_direction = perform_action(cop3_state, q_table3, EPSILON)
        if action_direction[cop1_direction] in game.valid_actions(cop1_pos, index=True):
            game.update({'1': action_direction[cop1_direction]})
        
        if action_direction[cop2_direction] in game.valid_actions(cop2_pos, index=True):
            game.update({'2': action_direction[cop2_direction]})

        if action_direction[cop3_direction] in game.valid_actions(cop3_pos, index=True):
            game.update({'3': action_direction[cop3_direction]})

        if game._agent_location['1'] == game._agent_location['x']:
            reward = CATCH_REWARD
            cop1_caught = CATCH_REWARD
            catch_count1 += 1
        elif game._agent_location['2'] == game._agent_location['x']:
            reward = CATCH_REWARD
            cop2_caught = CATCH_REWARD
            catch_count2 += 1
        elif game._agent_location['3'] == game._agent_location['x']:
            reward = CATCH_REWARD
            cop3_caught = CATCH_REWARD
            catch_count3 += 1
        else:
            reward = -MOVE_PENALTY
        
        if SHOW:
            visualize(screen, game.grid, pyimage_objects, ROWS, COLS, blockSize)
            pygame.display.update()
            time.sleep(1)
            if game._agent_location['x'] == 'end':
                time.sleep(2)

        cop1_pos = game.locate_agent('1')
        cop2_pos = game.locate_agent('2')
        cop3_pos = game.locate_agent('3')
        
        if reward != CATCH_REWARD:
            thief_run_direction = game.thief_run()
            if thief_run_direction in game.valid_actions(thief_pos, index=True):
                game.update({'x': thief_run_direction})

        thief_pos = game.locate_agent('x')
        cop1_state_new, cop2_state_new, cop3_state_new = get_cop_states(cop1_pos, cop2_pos, cop3_pos, thief_pos)

        cop1_state, cop2_state, cop3_state = cop1_state_new, cop2_state_new, cop3_state_new

        episode_reward += reward
        if reward == CATCH_REWARD:
            break
    
    progress.set_description(f'Total Steps: {STEPS - episode_reward}')
    episode_rewards.append(episode_reward)
    EPSILON *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f'Reward {SHOW_EVERY}ma')
plt.xlabel('episode #')
plt.savefig('Graphs/visualize.png')
plt.show()

catch_count_total = (catch_count1 + catch_count2 + catch_count3)
print('Catching Percentage : Cop 1 :', catch_count1 * 100 / catch_count_total)
print('Catching Percentage : Cop 2 :', catch_count2 * 100 / catch_count_total)
print('Catching Percentage : Cop 3 :', catch_count3 * 100 / catch_count_total)
print('Catching Percentage : Total :', catch_count_total * 100 / EPISODES)
print('Average Steps To Catch      :', STEPS - (sum(episode_rewards)/len(episode_rewards)))