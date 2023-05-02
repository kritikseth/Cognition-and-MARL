from ..core.compose import Environment
import random

class Game(Environment):

    def __init__(self, grid, block_size):

        super().__init__(grid)
        self._block_size = block_size
    
    def initialize(self):
        self._agent_location = {}
        self._grid = [['o']*self._cols for row in range(self._rows)]
        if self._obstruct_idx != []:
            for idx in self._obstruct_idx:
                self.obstruct(idx, index=True)

    def setup_agents(self, agents):

        self._agent_location.update(agents)
        for agent, idx in self._agent_location.items():
            X, Y = self.to_coordinate(idx)
            self._valid_state(X, Y)
            self._grid[X][Y] = agent
    
    def _valid_state(self, X, Y, action=None):

        if self._grid[X][Y] == '[]':
            if action is not None:
                raise ValueError(f'Action: {action}, State: ({X}, {Y}) is invalid!')
            else:
                raise ValueError(f'Current State: ({X}, {Y}) is invalid!')
    
    @property
    def valid_states(self, index=True):
        coordinate = []
        for row in range(self._rows):
            for col in range(self._cols):
                if self._grid[row][col] == 'o':
                    coordinate.append((row, col))
        
        if index:
            return [self.to_index(c) for c in coordinate]
        else:
            return coordinate
    
    def random_state(self):
        return random.choice(self.valid_states)
    
    def update(self, actions):

        for agent, action in actions.items():
            ind = self._agent_location[agent]
            X, Y = self.to_coordinate(ind)
            self._grid[X][Y] = 'o'
            
            nx_idx = self.next(action, ind, index=True)
            check = [p for a, p in self._agent_location.items() if 'x' != a]

            if nx_idx in check:
                raise ValueError(f'Action: {action}, State: ({X}, {Y}) is invalid for Agent: {agent}')
            
            X, Y = self.to_coordinate(nx_idx)

            if self._grid[X][Y] == 'o':
                self._grid[X][Y] = agent
                self._agent_location[agent] = nx_idx
            else:
                current_agent = self._grid[X][Y]
                if current_agent == 'x':
                    self._agent_location[current_agent] = 'end'
                    self._agent_location[agent] = 'end'
                    self._grid[X][Y] = agent
        
    def locate_agent(self, agent, index=True):

        for area in self._grid:
            if agent in area:
                if index:
                    return self.to_index((self._grid.index(area), area.index(agent)))
                else:
                    return (self._grid.index(area), area.index(agent))
        
    def increment(self, action, X, Y):

        if action == 'up':
            X, Y = self.up(X, Y)
        if action == 'down':
            X, Y = self.down(X, Y)
        if action == 'left':
            X, Y = self.left(X, Y)
        if action == 'right':
            X, Y = self.right(X, Y)
        
        return (X * self._block_size, Y * self._block_size)
    
    def relative_position(self, thief, cop):
        x_val = 0
        if cop[0] > thief[0]:
            distance1 = cop[0] - thief[0]
            distance2 = thief[0] + self._rows - cop[0]
            if distance2 < distance1:
                x_val = -distance2
            else:
                x_val = distance1
        elif cop[0] < thief[0]:
            distance1 = thief[0] - cop[0]
            distance2 = cop[0]+self._rows - thief[0]
            if distance2 < distance1:
                x_val = distance2
            else:
                x_val = -distance1
        
        y_val = 0
        if cop[1] > thief[1]:
            distance1 = cop[1] - thief[1]
            distance2 = thief[1]+self._rows - cop[1]
            if distance2 < distance1:
                y_val = - distance2
            else:
                y_val = distance1
        elif cop[1] < thief[1]:
            distance1 = thief[1] - cop[1]
            distance2 = cop[1] + self._rows - thief[1]
            if distance2 < distance1:
                y_val = distance2
            else:
                y_val = -distance1

        return (x_val, y_val)

    def get_away_direction(self, distance):
        directions = []
        if abs(distance[0]) < abs(distance[1]):
            if distance[0] < 0:
                directions.append('down')
            elif distance[0] > 0:
                directions.append('up')
            else:
                directions.append('down')
                directions.append('up')

            if distance[1] < 0:
                directions.append('right')
            elif distance[1] > 0:
                directions.append('left')
            else:
                directions.append('right')
                directions.append('left')
        
        else:
            if distance[1] < 0:
                directions.append('right')
            elif distance[1] > 0:
                directions.append('left')
            else:
                directions.append('right')
                directions.append('left')

            if distance[0] < 0:
                directions.append('down')
            elif distance[0] > 0:
                directions.append('up')
            else:
                directions.append('down')
                directions.append('up')

        return directions
    
    def thief_run(self):
        cop1_pos = self.locate_agent('1', index=False)
        cop2_pos = self.locate_agent('2', index=False)
        thief_pos = self.locate_agent('x', index=False)

        cop_1_rel = self.relative_position(thief_pos, cop1_pos)
        cop_2_rel = self.relative_position(thief_pos, cop2_pos)

        dir_away_frm_1 = self.get_away_direction(cop_1_rel)
        dir_away_frm_2 = self.get_away_direction(cop_2_rel)

        possible_escape = set(dir_away_frm_1).intersection(set(dir_away_frm_2))

        if len(possible_escape)==0:
            dis_frm_1 = abs(cop_1_rel[0])+abs(cop_1_rel[1])
            dis_frm_2 = abs(cop_2_rel[0])+abs(cop_2_rel[1])
            if dis_frm_1<=dis_frm_2:
                return dir_away_frm_1[0]
            else:
                return dir_away_frm_2[0]
        
        return list(possible_escape)[0]