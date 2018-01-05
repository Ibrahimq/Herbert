class Node(object):
    id, x, y, node_type = int(), int(), int(), int()
    visited = bool()
    parent, cost, heuristic, net_cost = None, int, int, int

    def __init__(self, x, y, node_type):
        self.x, self.y, self.node_type = x, y, node_type
        self.cost, self.heuristic, self.net_cost = 0, 0, 0          # net_cost=cost+heuristic
        self.visited = False


class Cell(object):
    x, y, reachable = int(), int(), bool()
    cost, heuristic, net_cost = int(), int(), int()
    is_target = bool()

    def __init__(self, x, y, reachable):
        # setting some parameters for each cell
        self.x, self.y = x, y
        self.reachable, self.parent = reachable, None
        self.cost, self.heuristic, self.net_cost = 0, 0, 0      # net_cost=cost+heuristic
        self.is_target = False

    def set_target(self, is_target):
        self.is_target = is_target
