# HERBERT SOLVING VIA ******** ALGORITHM#
import math, datetime, copy
from Environment import Environment
from DS import *
from searching import *


class Herbert(object):
    face, position, map, targets = None, dict(), [], []
    action_LR = {
        'left': {'up': 'left', 'left': 'down', 'down': 'right', 'right': 'up', 'action': 'l'},
        'right': {'up': 'right', 'left': 'up', 'down': 'left', 'right': 'down', 'action': 'r'},
    }
    action_step = {
        'up': {'x': 0, 'y': -1},
        'down': {'x': 0, 'y': 1},
        'left': {'x': -1, 'y': 0},
        'right': {'x': 1, 'y': 0},
        'action': 's',
    }
    adjacent = {
        'up': ['left','right'],
        'down': ['left','right'],
        'left':['up','down'],
        'right':['up','down'],
    }
    def __init__(self, position, env_map, max_c, targets):
        self.face, self.position, self.map = 'up', position, env_map
        self.targets = targets

    # Actions and Agent Logic will be implemented here
    def take_actions(self, face, act, position):
        if act == 'left' or act == 'right':
            face = self.action_LR[act][face]
            return str(self.action_LR[act]['action']), face, position
        elif act == 'step':
            position.x += self.action_step[face]['x']
            position.y += self.action_step[face]['y']
            return str(self.action_step['action']), face, position

    def get_routes(self, targets, fl):              #find multible paths
        solutions = list()
        if fl == 0:
            print 'Calculating Paths...'
        for i, target in enumerate(targets):        # calculating shortest path for each start point.
            targets_copy = list(targets)            # Copying the target list
            del targets_copy[i]                     # delete current node from list
            solutions.append(self.find_path(target, # get path for a start point $target
            targets_copy, []))
        if fl == 0:
            print('Paths Calculated')
        return solutions

    def find_path(self, start, targets, path):      # find individual path
        if len(targets) == 0:                       # base case - All appended
            path.append(start)
            return path
        path.append(start)
        glo_distance = 100
        glo_index = -1
        for i, target in enumerate(targets):        # detecting nearest point
            loc_distance = abs(target.x - start.x) + abs(target.y - start.y)
            if loc_distance < glo_distance:
                glo_distance = loc_distance
                glo_index = i
        temp = targets[glo_index]
        del targets[glo_index]
        path = self.find_path(temp ,targets, path)
        return path

    def find_path_movements(self, path):            # converting nodes order to a set ot Movements
        position = self.position                    # made by (left, right, up, down) actions to make it
        full_path = ''                              # easier for A* get the shortest path.
        for node in path:
            full_path += find(self.map, position, node)
            position = node
        full_path = full_path[:-1]
        answer = self.apply_path(full_path)
        reduced_answer = self.answer_reduction(answer)

        return reduced_answer, answer

    def apply_path(self, path_in_movements):        # maping the movements of (left, right, up, down) to
        movements = path_in_movements.split(",")    # herbert language constructed by (s, l, r)
        face = copy.copy(self.face)
        position = copy.copy(self.position)
        path_in_actions = ''
        for movement in movements:                  # convert each movement to corresponding action
            action_in_path = ''
            if (face == movement):
                action_in_path, face, position = self.take_actions(face, 'step', position)
            else:
                sub_action_in_path=''
                if movement in self.adjacent[face]:
                    if self.take_actions(face, 'right', position)[1] == movement:
                        sub_action_in_path, face, position = self.take_actions(face, 'right', position)
                        action_in_path += sub_action_in_path
                        sub_action_in_path, face, position = self.take_actions(face, 'step', position)
                        action_in_path += sub_action_in_path
                    elif self.take_actions(face, 'left', position)[1] == movement:
                        sub_action_in_path, face, position = self.take_actions(face, 'left', position)
                        action_in_path += sub_action_in_path
                        sub_action_in_path, face, position = self.take_actions(face, 'step', position)
                        action_in_path += sub_action_in_path
                else:
                    if len(path_in_actions) > 1 and path_in_actions[len(path_in_actions)-1] == 'l':
                        sub_action_in_path, face, position = self.take_actions(face, 'left', position)
                        action_in_path += sub_action_in_path
                        sub_action_in_path, face, position = self.take_actions(face, 'left', position)
                        action_in_path += sub_action_in_path
                    else:
                        sub_action_in_path, face, position = self.take_actions(face, 'right', position)
                        action_in_path += sub_action_in_path
                        sub_action_in_path, face, position = self.take_actions(face, 'right', position)
                        action_in_path += sub_action_in_path
                    sub_action_in_path, face, position = self.take_actions(face, 'step', position)
                    action_in_path += sub_action_in_path
            path_in_actions += action_in_path
        return path_in_actions

    def answer_reduction(self, answer):
        reduced_answer = ''
        Strs, ch, Str, i = [], '', "", 0
        for char in answer:
            i += 1
            if ch == char or ch == '':
                ch = char
                Str += ch
                if len(answer) == i:
                    Strs.append(Str)
            elif ch != char:
                if len(Str) > 1:
                    Strs.append(Str)
                    ch = char
                    Strs.append(ch)
                    ch = ''
                    Str = ""
                else:
                    Strs.append(ch)
                    Str = ''
                    ch = char
                    Str += ch
        for s in Strs:
            if len(s) > 1 and s[0] == 's':
                reduced_answer += "S(" + str(len(s)) + ")"
            elif len(s) > 1 and s[0] == 'r':
                reduced_answer += "R(" + str(len(s)) + ")"
            elif len(s) > 1 and s[0] == 'l':
                reduced_answer += "L(" + str(len(s)) + ")"
            else:
                reduced_answer += s
        return reduced_answer

    def solve(self):
        routes = self.get_routes(self.targets, 0)
        solutions, reduced_solutions = [], []
        for route in routes:
            solution, reduced_solution = self.find_path_movements(route)
            solutions.append(solution)
            reduced_solutions.append(reduced_solution)
        for solution, reduced_solution in zip(solutions, reduced_solutions):
            print (solution, reduced_solution)

if '__main__':
    environment = Environment(5)
    herbert = Herbert(environment.initial_location, environment.map, environment.max_char, environment.targets)
    environment.set_herbert(herbert)
    herbert.solve()