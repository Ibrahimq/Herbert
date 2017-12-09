# HERBERT SOLVING VIA ******** ALGORITHM#
class Herbert(object):
    face, position, targets, obstacles, answer = 'u', dict(), [], [], ''
    actions = {
        'left': {'up': 'left', 'left': 'down', 'down': 'right', 'right': 'up', 'action': 'l'},
        'right': {'up': 'right', 'left': 'up', 'down': 'left', 'right': 'down', 'action': 'r'},
        'step': {'up': {'x': 0, 'y': -1},
                 'down': {'x': 0, 'y':  1},
                 'left': {'x': -1, 'y':  0},
                 'right': {'x': 1, 'y':  0},
                 'action': 's',
                 }
    }

    def __init__(self, position, targets, obstacles):
        self.face = 'up'
        self.position = position
        self.targets, self.obstacles = targets, obstacles

    # Actions and Agent Logic will be implemented here
    def take_actions(self, act):
        self.answer += self.actions[act]['action']
        if act == 'left' or act == 'right':
            self.face = self.actions[act][self.face]
        elif act == 'step':
            self.position['x'] += self.actions[act][self.face]['x']
            self.position['y'] += self.actions[act][self.face]['y']


def read_problem(level):
    maximum = -1
    if type(level) is not int:
        print("Enter a valid level")
        return
    location = "Problems/level" + str(level) + ".txt"
    try:
        file_object = open(location, "r")
    except IOError as error:
        print("Error Loading File".format(error.errno, error.strerror))
        return
    problem_file = file_object.readlines()
    while problem_file[len(problem_file)-1][0] in 'pm ':
        if problem_file[len(problem_file)-1][0] == 'm':
            x = problem_file[len(problem_file)-1]
            maximum = int(x[8:])
        problem_file.pop()
    problem_text = map(lambda s: s.strip(), problem_file)
    problem_text = problem_text[0:-2]
    return [problem_text, maximum]


class Environment:
        level = int()                                        # Specify level  and save it to level
        problem, max_char = read_problem(20)                 # Read problem
        h_location, targets, obstacles = dict(), [], []
        for index_row, line in enumerate(problem):
            for index_col, char in enumerate(line):
                temp = dict()
                temp['y'], temp['x'] = index_col, index_row
                if char == 'o':
                    targets.append(temp)
                elif char == 'u':
                    h_location = temp
                elif char != '.':
                    obstacles.append(temp)
        herbert = Herbert(h_location, targets, obstacles)


if '__main__':
    environment = Environment()
