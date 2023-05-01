from ..core.compose import Environment
import random

class Game(Environment):

    def __init__(self, grid, block_size):

        super().__init__(grid)
        self._block_size = block_size
    
    def initialize(self):
         self._agent_location = {}

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