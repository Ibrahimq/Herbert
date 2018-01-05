import heapq
import copy
# no of rows and columns in grid
rows = 25
columns = 25


class Cell(object):
    x, y, reachable = int(), int(), bool()
    cost, heuristic, net_cost = int(), int(), int()

    def __init__(self, x, y, reachable):
        # setting some parameters for each cell
        self.x, self.y = x, y
        self.reachable, self.parent = reachable, None
        self.cost, self.heuristic, self.net_cost = 0, 0, 0      # net_cost=cost+heuristic


class AStar(object):
    open, cells, closed = list(), list(), None
    start, end = None, None

    def __init__(self, grid, start, end):
        self.open = []                          # list of unchecked neighbour cells
        heapq.heapify(self.open)                # keeps cells with lowest total_cost at top
        self.closed = set()                     # list of already checked cells
        self.cells = []                         # list of neighbour cells
        self.start, self.end = Cell, Cell
        self.init_grid(grid, start, end)

    def init_grid(self, grid, start, end):
        for i in range(rows):
            for j in range(columns):            # detecting the obstacles
                if grid[j][i].node_type == 2:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(i, j, reachable))
                if grid[j][i] == start:         # detecting the start and end
                    self.start = self.cell(i, j)
                elif grid[j][i] == end:
                    self.end = self.cell(i, j)

    def cell(self, x, y):                       # returns the location to identify each cell
        return self.cells[x*columns+y]

    def cell_heuristic(self, cell):             # returns the heuristic for A* algorithm
        return abs(cell.x-self.end.x)+abs(cell.y-self.end.y)

    def neighbour(self, cell):                  # returns a list of neighbors of a cell
        cells = []
        if cell.x < columns - 1:
            cells.append(self.cell(cell.x+1, cell.y))
        if cell.x > 0:
            cells.append(self.cell(cell.x-1, cell.y))
        if cell.y < rows-1:
            cells.append(self.cell(cell.x, cell.y+1))
        if cell.y > 0:
            cells.append(self.cell(cell.x, cell.y-1))
        return cells

    def update_cell(self, adj, cell):           # update the details about the selected neighbor cell
        adj.cost = cell.cost + 1
        adj.heuristic = self.cell_heuristic(adj)
        adj.parent = cell
        adj.net_cost = adj.cost + adj.heuristic

    def display_path(self):
        route_path, str_path = [], ''
        cell = self.end
        while cell.parent is not None:          # storing the parents in list from end to start
            route_path.append([cell.x, cell.y])
            cell = cell.parent
        route_path.reverse()                    # to get the path from start to end, as we went backward.
        temp = copy.copy(route_path[0])         # initiating temp with the start
        temp[0], temp[1] = self.start.x, self.start.y
        for i, node in enumerate(route_path):   # calculating movements for the path
            if temp[0] < node[0]:
                str_path += 'right,'
            elif temp[0] > node[0]:
                str_path += 'left,'
            elif temp[1] < node[1]:
                str_path += 'down,'
            elif temp[1] > node[1]:
                str_path += 'up,'
            temp = node
        return str_path

    def search(self):

        heapq.heappush(self.open,               # pushing the first element in open queue
                       (self.start.net_cost, self.start))
        str_path = ''
        while len(self.open):
            net_cost, cell = heapq.heappop(self.open)
            self.closed.add(cell)               # adding the checked cell to closed list
            if cell is self.end:                # store path movements
                str_path = self.display_path()
                break
            neighbours = self.neighbour(cell)   # getting the adjacent cells
            for path in neighbours:
                # if cell is not an obstacle and has not been already checked
                if path.reachable and path not in self.closed:
                    if (path.net_cost, path) in self.open:
                        if path.cost > cell.cost + 1:     # selecting the cell with least cost
                            self.update_cell(path, cell)
                    else:
                        self.update_cell(path, cell)
                        heapq.heappush(self.open, (path.net_cost, path))
        return str_path


def find(grid, start, end):
    solution = AStar(grid, start, end)
    str_path = solution.search()
    del solution
    return str_path
