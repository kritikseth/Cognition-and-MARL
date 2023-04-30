from .base import BaseMap

class Map(BaseMap):

    def __init__(self, rows=10, cols=10):
        super().__init__(rows, cols)
    
    def obstruct(self, X, Y=None, index=False):
        if index:
            X, Y = self.to_coordinate(X)
            self._grid[X][Y] = 'x'
        else:
            self._grid[X][Y] = 'x'
    
    def save(self):
        return self._grid

class Environment(BaseMap):

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
    
    def _valid_state(self, X, Y, action=None):
        if self._grid[X][Y] != 'o':
            if action is not None:
                raise ValueError(f'Action: {action}, State: ({X}, {Y}) is invalid!')
            else:
                raise ValueError(f'Current State: ({X}, {Y}) is invalid!')
    
    def valid_actions(self, X, Y=None, index=False):
        if index:
            X, Y = self.to_coordinate(X)
        self._valid_state(X, Y)
        
        actions = {self._up: 'up', self._down: 'down', self._left: 'left', self._right: 'right'}
        coordinates = [action(X, Y) for action in actions.keys()]
        states = [self._grid[X][Y] for X, Y in coordinates]
        valid = [['up', 'down', 'left', 'right'][i] for i, s in enumerate(states) if s == 'o']
        return valid

    def _up(self, X, Y=None, index=False):
        if index:
            X, Y = self.to_coordinate(X)
        self._valid_state(X, Y)
        if X == 0: X = self._rows - 1
        else: X -= 1
        return (X, Y)

    def _down(self, X, Y=None, index=False):
        if index:
            X, Y = self.to_coordinate(X)
        self._valid_state(X, Y)
        if X == self._rows - 1: X = 0
        else: X += 1
        return (X, Y)
    
    def _left(self, X, Y=None, index=False):
        if index:
            X, Y = self.to_coordinate(X)
        self._valid_state(X, Y)
        if Y == 0: Y = self._cols - 1
        else: Y -= 1
        return (X, Y)

    def _right(self, X, Y=None, index=False):
        if index:
            X, Y = self.to_coordinate(X)
        self._valid_state(X, Y)
        if Y == self._cols - 1: Y = 0
        else: Y += 1
        return (X, Y)

    def up(self, X, Y=None, index=False):
        X, Y = self._up(X, Y, index)
        self._valid_state(X, Y, 'up')

        if index:
            return self.to_index(X, Y)
        else:
            return (X, Y)

    def down(self, X, Y=None, index=False):
        X, Y = self._down(X, Y, index)
        self._valid_state(X, Y, 'down')

        if index:
            return self.to_index(X, Y)
        else:
            return (X, Y)
    
    def left(self, X, Y=None, index=False):
        X, Y = self._left(X, Y, index)
        self._valid_state(X, Y, 'left')

        if index:
            return self.to_index(X, Y)
        else:
            return (X, Y)

    def right(self, X, Y=None, index=False):
        X, Y = self._right(X, Y, index)
        self._valid_state(X, Y, 'right')

        if index:
            return self.to_index(X, Y)
        else:
            return (X, Y)

    def next(self, action, X, Y=None, index=False):
        if action == 'up':
            return self.up(X, Y, index)
        if action == 'down':
            return self.down(X, Y, index)
        if action == 'left':
            return self.left(X, Y, index)
        if action == 'right':
            return self.right(X, Y, index)