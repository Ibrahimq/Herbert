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
            print '\nCalculating Paths...'
        for i, target in enumerate(targets):        # calculating shortest path for each start point.
            targets_copy = list(targets)            # Copying the target list
            del targets_copy[i]                     # delete current node from list
            solutions.append(self.find_path(target, # get path for a start point $target
            targets_copy, []))
        if fl == 0:
            print('Paths Calculated\n')
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
        full_path += find(self.map, position, path[0], path)
        full_path = full_path[:-1]
        answer = self.apply_path(full_path)
        reduced_answer = self.answer_reduction(answer)
        print(answer)
        print(reduced_answer)
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
        Strs = []
        Functions = [['a(N):sa(N-1)', False], ['b(N):rb(N-1)', False], ['c(N):lc(N-1)', False], ['x:sr', False],
                     ['y:sl', False]]
        Reduced_answer, Patterns, StrTemp = "", "", ""
        chTemp = ''
        i = 0
        # Divide string into substrings
        for ch in answer:
            i += 1
            if chTemp == ch or chTemp == '':
                chTemp = ch
                StrTemp += chTemp
                if len(answer) == i:
                    Strs.append(StrTemp)
            elif chTemp != ch:
                if len(StrTemp) > 1:
                    Strs.append(StrTemp)
                    chTemp = ch
                    Strs.append(chTemp)
                    chTemp = ''
                    StrTemp = ""
                else:
                    Strs.append(chTemp)
                    StrTemp = ''
                    chTemp = ch
                    StrTemp += chTemp
        # Find repeated characters and replace with pattern
        for s in Strs:
            if len(s) > 1 and s[0] == 's':
                Patterns += ("a(" + str(len(s)) + ")")
                Functions[0][1] = True
            elif len(s) > 2 and s[0] == 'r':
                Patterns += ("b(" + str(len(s)) + ")")
                Functions[1][1] = True
            elif len(s) > 2 and s[0] == 'l':
                Patterns += ("c(" + str(len(s)) + ")")
                Functions[2][1] = True
            else:
                Patterns += (s)
        # Replace patterns
        Patterns = Patterns.replace("sr", "x")
        Patterns = Patterns.replace("sl", "y")
        if Patterns.find("x") != -1:
            Functions[3][1] = True
        if Patterns.find("y") != -1:
            Functions[4][1] = True
        endlines_count = 0
        for F in Functions:
            if F[1] == True:
                Reduced_answer += F[0] + "\n"
                endlines_count += 1
        Reduced_answer += Patterns
        count = 0
        for char in Reduced_answer:
            if not (char == ':' or char == '(' or char == ')'):
                count += 1
        count -= 2*endlines_count
        if len(answer) < count:
            Reduced_answer = answer
        return Reduced_answer
    def solve(self):
        routes = self.get_routes(self.targets, 0)
        solutions, reduced_solutions = [], []
        print('Calculating actions...')
        for route in routes:
            reduced_solution, solution = self.find_path_movements(route)
            solutions.append(solution)
            reduced_solutions.append(reduced_solution)
        print('Actions Calculated\n')
        best_solution = ''
        best_solution_len = 1000000
        print(str(len(routes))+' Solutions found:')
        for solution, reduced_solution in zip(solutions, reduced_solutions):
            if len(reduced_solution) < best_solution_len:
                best_solution_len = len(reduced_solution)
                best_solution = reduced_solution
            print reduced_solution
        print('\nThe best Solution of them is: ')
        print(best_solution)
        print('with length of: '+str(best_solution_len))
if '__main__':
    flag = True
    while(flag):
        try:
            level = raw_input("Please enter the level you want to solve: ")
            if not level or not level.isdigit():
                raise ValueError('Empty string')
        except ValueError as error:
            print(str(error) +", please enter a valid number level.")
            continue
        flag = False
    environment = Environment(int(level))
    herbert = Herbert(environment.initial_location, environment.map, environment.max_char, environment.targets)
    environment.set_herbert(herbert)
    herbert.solve()
    del herbert, environment
