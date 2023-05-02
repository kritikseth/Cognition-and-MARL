import numpy as np

def get_cop_states(cop1_pos, cop2_pos, cop3_pos, thief_pos):
    cop1_state = [cop1_pos, cop2_pos, cop3_pos, thief_pos]
    cop2_state = [cop2_pos, cop3_pos, cop1_pos, thief_pos]
    cop3_state = [cop3_pos, cop1_pos, cop2_pos, thief_pos]
    return cop1_state, cop2_state, cop3_state

def perform_action(observations, q_table, epsilon):
    if np.random.random() > epsilon:
        direction = np.argmax(q_table[observations[0]][observations[1]][observations[2]][observations[3]])
    else:
        direction = np.random.randint(0, 4)
    return direction

def update_table(reward, old_state, new_state, direction, q_table, catch_reward, learning_rate, discount):
    max_future_q = np.max(q_table[new_state[0]][new_state[1]][new_state[2]][new_state[3]])
    current_q = q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]][direction]
    
    if reward == catch_reward*2:
        new_q = catch_reward
    else:
        new_q = (1 - learning_rate) * current_q + learning_rate * (reward + discount * max_future_q)
    q_table[old_state[0]][old_state[1]][old_state[2]][old_state[3]][direction] = new_q