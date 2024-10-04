import pygame
import time
import json
import os

import BallSortBack
from binary_heap import BinaryHeap
from node import Node
import heuristics

HEURISTIC_PONDERATOR = 1
VISUALIZATION = True
MOVING_SPEED = 50

# Replace with the map to be tested
GAME_MAP = "map_5"

# Compute the map's absolute path
relative_map_path = os.path.join("maps", f"{GAME_MAP}.json")
current_path = os.path.dirname(os.path.realpath(__file__))
MAP_PATH = os.path.join(current_path, relative_map_path)

# Load the map's data
with open(MAP_PATH, 'r') as f:
    MAP_DATA = json.load(f)

class AStarSolver():

    '''
        This class models the solver for the game and performs the A* algorithm in order to find a solution for it.
    '''

    def __init__(self, heuristic = heuristics.no_heuristic, visualization = VISUALIZATION, map_info = MAP_DATA):

        '''
            Parameters:
                heuristic (function) : function used as heuristic for the search (should take a State as an input and output a number), no heuristic by default.
                visualization (bool) : whether to or not to display the solution after it's found.

        '''

        self.expansions = 0
        self.generated = 0
        self.f_states = []

        # Load the map's data
        self.game = BallSortBack.BallSortGame()
        self.game.load_map(map_info)
        self.initial_state = self.game.init_state
        
        self.heuristic = heuristic
        self.open = BinaryHeap()
        self.is_admisible = True

        if visualization:
            self.game.start_visualization(text = "Solving...")

    def search(self):

        '''
            Performs the A* search for a solution.
        '''
        self.start_time = time.time()
        self.generated = {}

        # We create the initial node and add it to the open list
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(initial_node.state)
        initial_node.key = initial_node.g + HEURISTIC_PONDERATOR * initial_node.h
        self.generated[repr(initial_node.state)] = initial_node
        self.open.insert(initial_node)

        # While there are still nodes to expand
        while not self.open.is_empty():
            # We get the node with the lowest f value
            parent_node = self.open.extract()
            self.f_states.append(parent_node.key)
            self.game.current_state = parent_node.state

            # If the node is a goal node, we return the solution
            if parent_node.state.is_final():
                self.end_time = time.time()
                return parent_node.trace(), self.expansions, self.end_time - self.start_time, self.open.size

            # We expand the node
            self.expansions += 1
            neighbors = self.game.get_valid_moves()
            for neighbor in neighbors:
                in_open = True
                child_node = self.generated.get(repr(neighbor[0]))
                # If the node doesnt exist, we create it
                if child_node is None:
                    child_node = Node(neighbor[0])
                    self.generated[repr(child_node.state)] = child_node
                    child_node.h = self.heuristic(child_node.state)
                    # If the node didn't exist it means it has never been in the open list
                    in_open = False
                # We check if the current path is better than the previous one
                if parent_node.g + neighbor[2] < child_node.g:
                    child_node.parent = parent_node
                    child_node.action = neighbor[1]
                    child_node.g = parent_node.g + neighbor[2]
                    child_node.key = child_node.g + HEURISTIC_PONDERATOR * child_node.h
                    # We check if heuristic is admissible
                    if child_node.h > parent_node.h + neighbor[2]:
                        self.is_admisible = False
                    # If node is not in open, we insert it
                    if not in_open:
                        self.open.insert(child_node)
                        
        self.end_time = time.time()
        return None, self.expansions, self.end_time - self.start_time, self.open.size
    
    def lazysearch(self):

        '''
            Performs the A* lazysearch for a solution.
        '''
        self.start_time = time.time()
        self.generated = {}

        # We create the initial node and add it to the open list
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(initial_node.state)
        initial_node.key = initial_node.g + HEURISTIC_PONDERATOR * initial_node.h
        self.open.insert(initial_node)

        # While there are still nodes to expand
        while not self.open.is_empty():
            # We get the node with the lowest f value
            parent_node = self.open.extract()
            self.game.current_state = parent_node.state

            # If the node is a goal node, we return the solution
            if parent_node.state.is_final():
                self.end_time = time.time()
                return parent_node.trace(), self.expansions, self.end_time - self.start_time, self.open.size

            # We expand the node
            self.expansions += 1
            neighbors = self.game.get_valid_moves()
            for neighbor in neighbors:
                # We create the node and set its values
                child_node = Node(neighbor[0])
                child_node.h = self.heuristic(child_node.state)
                child_node.parent = parent_node
                child_node.action = neighbor[1]
                child_node.g = parent_node.g + neighbor[2]
                child_node.key = child_node.g + HEURISTIC_PONDERATOR * child_node.h
                # We insert the node to the open
                self.open.insert(child_node)
                        
        self.end_time = time.time()
        return None, self.expansions, self.end_time - self.start_time, self.open.size
    
    def greedysearch(self):

        '''
            Performs the Greedy Best First Search for a solution.
        '''
        self.start_time = time.time()
        self.generated = {}

        # We create the initial node and add it to the open list
        initial_node = Node(self.initial_state)
        initial_node.h = self.heuristic(initial_node.state)
        initial_node.key = initial_node.h
        self.generated[repr(initial_node.state)] = initial_node
        self.open.insert(initial_node)

        # While there are still nodes to expand
        while not self.open.is_empty():
            # We get the node with the lowest f value
            parent_node = self.open.extract()
            self.game.current_state = parent_node.state

            # If the node is a goal node, we return the solution
            if parent_node.state.is_final():
                self.end_time = time.time()
                return parent_node.trace(), self.expansions, self.end_time - self.start_time, self.open.size

            # We expand the node
            self.expansions += 1
            neighbors = self.game.get_valid_moves()
            for neighbor in neighbors:
                in_open = True
                child_node = self.generated.get(repr(neighbor[0]))
                # If the node didn't exist it means it has never been in the open list
                in_open = False
                # If the node doesnt exist, we create it
                if child_node is None:
                    child_node = Node(neighbor[0])
                    self.generated[repr(child_node.state)] = child_node
                    child_node.h = self.heuristic(child_node.state)
                    child_node.parent = parent_node
                    child_node.action = neighbor[1]
                    child_node.key = child_node.h
                    # If node is not in open, we insert it
                    if not in_open:
                        self.open.insert(child_node)
                        
        self.end_time = time.time()
        return None, self.expansions, self.end_time - self.start_time, self.open.size
        
if __name__ == "__main__":
    # We create an instance for the solver and perform the search on the current map
    solver = AStarSolver(heuristic = heuristics.wagdy_heuristic, visualization = VISUALIZATION)
    sol = solver.greedysearch()

    # In case a solution was found, try it out
    if sol[0] is not None:
        solver.game.current_state = solver.game.init_state
        for step in sol[0][1]:
            solver.game.make_move(step[0], step[1], moving_speed = MOVING_SPEED)

        if VISUALIZATION:
            solver.game.front.draw(solver.game.current_state, text = ":)")
            pygame.time.wait(2000) 
            pygame.quit()

        print("The search was succesful at finding a solution.")
        print(f"The number of expansions: {solver.expansions}")
        print(f"The time it took to find a solution: {solver.end_time - solver.start_time}")
        print(f"Number of steps: {len(sol[0][1])}")
        print(f"Number of nodes in memory: {sol[3]}")
        # print(f"Is the heuristic admisible: {sol[4]}")
        # print(f"F states: {sol[5]}")