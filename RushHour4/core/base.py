from tabulate import tabulate
from IPython.display import display, Markdown, Latex, HTML

class BaseMap:

    def __init__(self, rows=10, cols=10):

        self._rows = rows
        self._cols = cols
        self._start = 0
        self._end = rows * cols - 1
        self._grid = [['o']*cols for row in range(rows)]
    
    def to_coordinate(self, idx):
        return (idx // self._cols, idx % self._cols)
    
    def to_index(self, XY):
        return XY[0] * self._cols + XY[1]
    
    def __str__(self):
        table = [' '.join(row) for row in self._grid]
        table = '\n'.join(table)
        return table

    def _display(self, table):
        display(HTML(tabulate(table, tablefmt='html')))

    @property    
    def index(self):
        table, previous = [], 0
        for row in range(self._rows):
            table.append(list(range(0 + previous, self._cols + previous)))
            previous += self._cols
        self._display(table)
    
    @property
    def coordinate(self):
        table = []
        for row in range(self._rows):
            row_index = []
            for col in range(self._cols):
                row_index.append(f'({row:3.0f}, {col:3.0f} )')
            table.append(row_index)
        self._display(table)
    
    @property
    def grid(self):
        return self._grid
    
    def view(self):
        self._display(self._grid)