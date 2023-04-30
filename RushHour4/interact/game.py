from ..setup.compose import Environment

class Game(Environment):

    def __init__(self, grid):
        super().__init__()

        if hasattr(grid, '_grid'):
            self.__dict__.update(grid.__dict__)
        else:
            self._grid = grid
            self._rows = len(grid)
            self._cols = len(grid[0])
            self._start = 0
            self._end = self._rows * self._cols - 1
    
    def initialize(self, agents):

        self._agent_location = agents
        for agent, idx in agents:
            self._valid_state(idx, index=True)
            X, Y = self.to_coordinate(idx):
            self._grid[X][Y] = agent
    
    def update(self, actions):

        for agent, action in actions:
            ind = self._agent_location[agent]
            nx_idx = self.next(action, ind, index=True)
            self._agent_location[agent] = nx_idx