from DS import *


class Environment:
    level, problem , max_char = int(), [], int()
    herbert, initial_location, targets, map = None, dict(), [], []

    def __init__(self, level):
        self.level = level
        self.read_problem(level)  # Read problem
        for index_row, line in enumerate(self.problem):
            map_row = []
            for index_col, char in enumerate(line):
                if char == 'u' or char == '.':
                    temp = Node(index_col, index_row, 0)
                    map_row.append(temp)
                    if char == 'u':
                        self.initial_location = temp
                elif char == 'o':
                    temp = Node(index_col, index_row, 1)
                    self.targets.append(temp)
                    map_row.append(temp)
                else:
                    temp = Node(index_col, index_row, 2)
                    map_row.append(temp)
            if len(map_row) == 25:
                self.map.append(map_row)

    def set_herbert(self, herbert):
        self.herbert = herbert

    def read_problem(self, level):
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
        while problem_file[len(problem_file) - 1][0] in 'pm ':
            if problem_file[len(problem_file) - 1][0] == 'm':
                x = problem_file[len(problem_file) - 1]
                maximum = int(x[8:])
            problem_file.pop()
        problem_text = map(lambda s: s.strip(), problem_file)
        self.problem, self.max_char = problem_text, maximum
