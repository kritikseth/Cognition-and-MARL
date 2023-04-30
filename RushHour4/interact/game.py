from ..core.compose import Environment

class Game(Environment):

    def __init__(self, grid, block_size):
        super().__init__(grid)
        self._block_size = block_size
    
    def initialize(self, agents):

        self._agent_location = agents
        for agent, idx in agents.items():
            X, Y = self.to_coordinate(idx)
            self._valid_state(X, Y)
            self._grid[X][Y] = agent
    
    def _valid_state(self, X, Y, action=None):
        if self._grid[X][Y] == '[]':
            if action is not None:
                raise ValueError(f'Action: {action}, State: ({X}, {Y}) is invalid!')
            else:
                raise ValueError(f'Current State: ({X}, {Y}) is invalid!')
    
    def update(self, actions):

        for agent, action in actions.items():
            ind = self._agent_location[agent]
            X, Y = self.to_coordinate(ind)
            self._grid[X][Y] = 'o'
            
            nx_idx = self.next(action, ind, index=True)
            X, Y = self.to_coordinate(nx_idx)
            self._grid[X][Y] = agent
            self._agent_location[agent] = nx_idx
        
    def locate_agent(self, agent):

        for area in self._grid:
            if agent in area:
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