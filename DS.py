class Node(object):
    id, x, y, node_type = int(), int(), int(), int()
    visited = bool()
    parent, cost, heuristic, net_cost = None, int, int, int

    def __init__(self, x, y, node_type):
        self.x, self.y, self.node_type = x, y, node_type
        self.cost, self.heuristic, self.net_cost = 0, 0, 0          # net_cost=cost+heuristic
        self.visited = False
