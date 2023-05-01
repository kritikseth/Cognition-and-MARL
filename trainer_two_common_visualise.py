import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use('ggplot')

SIZE = 10
SIGHT = 5
EPISODES = 100
MOVE_PENALTY = 1
COLLISION_PENALTY = 100
CATCH_REWARD = 200

EPSILON = 0.0
EPS_DECAY = 0.9998
LEARNING_RATE = 0.1
DISCOUNT = 0.95

SHOW_EVERY = 10
SHOW = False

COP_N = 1  
THIEF_N = -1 
AGENT_COLORS = {1: (255, 175, 0), -1: (0, 0, 255)}

start_q_table = 'Models/two_common_qtable.pickle' # None or Filename

if start_q_table is None:
    # initialize the q-table#
    q_table = {}
    for i in range(- SIGHT, SIGHT+1):
        for ii in range(- SIGHT, SIGHT+1):
            for iii in range(- SIGHT, SIGHT+1):
                    for iiii in range(- SIGHT, SIGHT+1):
                        q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]

else:
    with open(start_q_table, 'rb') as f:
        q_table = pickle.load(f)

class cop_class:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def respawn(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def __str__(self):
        return f'{self.x}, {self.y}'

    def relative_position(self, other):
        x_val = 0
        if other.x > self.x:
            distance1 = other.x-self.x
            distance2 = self.x+SIZE - other.x
            if distance2<distance1:
                x_val = -distance2
            else:
                x_val = distance1
        elif other.x < self.x:
            distance1 = self.x - other.x
            distance2 = other.x+SIZE - self.x
            if distance2<distance1:
                x_val = distance2
            else:
                x_val = -distance1

        y_val = 0
        if other.y > self.y:
            distance1 = other.y-self.y
            distance2 = self.y+SIZE - other.y
            if distance2<distance1:
                y_val = -distance2
            else:
                y_val = distance1
        elif other.y < self.y:
            distance1 = self.y - other.y
            distance2 = other.y+SIZE - self.y
            if distance2<distance1:
                y_val = distance2
            else:
                y_val = -distance1

        return (x_val, y_val)

    def action(self):
        '''
        Gives us 4 total movement options. (0,1,2,3)
        '''
        if self.direction == 0:
            self.move(x=0, y=-1)
        elif self.direction == 1:
            self.move(x=0, y=1)
        elif self.direction == 2:
            self.move(x=-1, y=0)
        elif self.direction == 3:
            self.move(x=1, y=0)

    def move(self, x=0, y=0):
        self.x = (self.x + x) % SIZE
        self.y = (self.y + y) % SIZE
    
    def get_observation(self, c, t):
        c_obs = self.relative_position(c)
        t_obs = self.relative_position(t)
        self.new_obs = (c_obs, t_obs)
        return self.new_obs

    def perform_action(self):
        self.obs = self.new_obs
        if np.random.random() > EPSILON:
            self.direction = np.argmax(q_table[self.obs])
        else:
            self.direction = np.random.randint(0, 4)
        self.action()

    def update_table(self, reward, c, t):
        self.get_observation(c, t)
        max_future_q = np.max(q_table[self.new_obs])
        current_q = q_table[self.obs][self.direction]
        if reward == CATCH_REWARD*2:
            new_q = CATCH_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[self.obs][self.direction] = new_q


class thief_class:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def respawn(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)

    def __str__(self):
        return f'{self.x}, {self.y}'

    def relative_position(self, other):
        x_val = 0
        if other.x > self.x:
            distance1 = other.x-self.x
            distance2 = self.x+SIZE - other.x
            if distance2<distance1:
                x_val = -distance2
            else:
                x_val = distance1
        elif other.x < self.x:
            distance1 = self.x - other.x
            distance2 = other.x+SIZE - self.x
            if distance2<distance1:
                x_val = distance2
            else:
                x_val = -distance1

        y_val = 0
        if other.y > self.y:
            distance1 = other.y-self.y
            distance2 = self.y+SIZE - other.y
            if distance2<distance1:
                y_val = -distance2
            else:
                y_val = distance1
        elif other.y < self.y:
            distance1 = self.y - other.y
            distance2 = other.y+SIZE - self.y
            if distance2<distance1:
                y_val = distance2
            else:
                y_val = -distance1

        return (x_val, y_val)

    def action(self):
        '''
        Gives us 4 total movement options. (0,1,2,3)
        '''
        if self.direction == 0:
            self.move(x=0, y=-1)
        elif self.direction == 1:
            self.move(x=0, y=1)
        elif self.direction == 2:
            self.move(x=-1, y=0)
        elif self.direction == 3:
            self.move(x=1, y=0)

    def move(self, x=0, y=0):
        self.x = (self.x + x) % SIZE
        self.y = (self.y + y) % SIZE
    
    def get_observation(self, c1, c2):
        obs = [0,0,0,0]
        obs[0],obs[1] = self.relative_position(c1)
        obs[2],obs[3] = self.relative_position(c2)
        self.obs = obs

    def run(self):
        obs_values = list(map(abs, self.obs))
        lowest_index = obs_values.index(min(obs_values))
        if self.obs[lowest_index] < 0:
            if lowest_index in (0,2):
                self.direction = 3
            else:
                self.direction = 1
        else:
            if lowest_index in (0,2):
                self.direction = 2
            else:
                self.direction = 0
        self.action()

episode_rewards = []
cop1 = cop_class()
cop2 = cop_class()
thief = thief_class()
catch_count1 = 0
catch_count2 = 0

for episode in range(EPISODES):
    cop1.respawn()
    cop2.respawn()
    thief.respawn()

    episode_reward = 0
    cop1_caught = 0
    cop2_caught = 0
    cop1.get_observation(cop2, thief)
    cop2.get_observation(cop1, thief)
    for i in range(200):
        cop1.perform_action()
        cop2.perform_action()
        if cop1.x == thief.x and cop1.y == thief.y:
            reward = CATCH_REWARD
            cop1_caught = CATCH_REWARD
            catch_count1 += 1
            if cop2.x == thief.x and cop2.y == thief.y:
                cop2_caught = CATCH_REWARD
        elif cop2.x == thief.x and cop2.y == thief.y:
            reward = CATCH_REWARD
            cop2_caught = CATCH_REWARD
            catch_count2 += 1
        elif cop1.x == cop2.x and cop1.y == cop2.y:
            reward = -COLLISION_PENALTY
        else:
            reward = -MOVE_PENALTY

        if SHOW:
            env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
            env[thief.x][thief.y] = AGENT_COLORS[THIEF_N]
            env[cop1.x][cop1.y] = AGENT_COLORS[COP_N] 
            env[cop2.x][cop2.y] = AGENT_COLORS[COP_N] 
            img = Image.fromarray(env, 'RGB')
            img = img.resize((300, 300))
            cv2.imshow('image', np.array(img)) 
            if reward == CATCH_REWARD or reward == -COLLISION_PENALTY:
                if cv2.waitKey(500) & 0xFF == ord('q'):
                    break
            else:
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break

        thief.get_observation(cop1, cop2)
        thief.run()

        cop1.update_table(reward+cop1_caught , cop2, thief)
        cop2.update_table(reward+cop2_caught , cop1, thief)

        episode_reward += reward
        if reward == CATCH_REWARD or reward == -COLLISION_PENALTY:
            break

    print(episode + 1, ': STEPS :', 200 - episode_reward)
    episode_rewards.append(episode_reward)
    EPSILON *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f'Reward {SHOW_EVERY}ma')
plt.xlabel('episode #')
plt.show()

catch_count_total = (catch_count1 + catch_count2)
print('Catching Percentage : Cop 1 :', catch_count1 * 100 / catch_count_total)
print('Catching Percentage : Cop 2 :', catch_count2 * 100 / catch_count_total)
print('Catching Percentage : Total :', catch_count_total * 100 / EPISODES)
print('Average Steps To Catch      :', 200 - (sum(episode_rewards)/len(episode_rewards)))