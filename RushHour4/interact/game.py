from ..setup.compose import Environment

class Game(Environment):

    def __init__(self, grid):
        super().__init__(grid)
    
    def initialize(self, agents):

        self._agent_location = agents
        for agent, idx in agents.items():
            X, Y = self.to_coordinate(idx)
            self._valid_state(X, Y)
            self._grid[X][Y] = agent
    
    def update(self, actions):

        for agent, action in actions:
            ind = self._agent_location[agent]
            nx_idx = self.next(action, ind, index=True)
            self._agent_location[agent] = nx_idx