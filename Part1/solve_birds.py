#!/usr/local/bin/python3
# solve_birds.py : Bird puzzle solver
#
# Code by: hgalla, rathlur, pfyffe
#
# Based on skeleton code by D. Crandall & B551 course staff, Fall 2022
#
# N birds stand in a row on a wire, each wearing a t-shirt with a number.
# In a single step, two adjacent birds can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys

N=5

#####
# THE ABSTRACTION:
#
# Initial state:
# Birds sitting on the power line in random order

# Goal state:
# given a state, returns True or False to indicate if it is the goal state: birds aligned in sequential order
def is_goal(state):
    return state == list(range(1, N+1))

# Successor function:
# given a state, return a list of successor states
def successors(state):
    return [ state[0:n] + [state[n+1],] + [state[n],] + state[n+2:] for n in range(0, N-1) ]

# Heuristic function:
# given a state, return an estimate of the number of steps to a goal from that state
def h(state):
    # computes the sum of distances of the birds from their goal positions
    h_value = 0

    for i in range(0, len(state)):
        if state[i] == i+1:
            continue
        h_value += abs(state[i] - i+1)

    return h_value

#########
#
# THE ALGORITHM:
#
# This is a generic solver using BFS. 
#
def solve(initial_state):
    fringe = []

    fringe += [(initial_state, [], 0),]
    while len(fringe) > 0:
        (state, path, h_value) = fringe.pop(0)
        
        if is_goal(state):
            return path+[state,]

        successor_array = successors(state)
        for s in successor_array:
            # appending f(s) = g(s) + h(s) into the fringe where:
            # g(s) - the total cost from initial state to the state 's'
            # h(s) - the heuristic function which calculates how far the state 's' is from the goal
            g = path+[state,]
            fringe.append((s, g, h(s) + len(g)))

        # sorting the queue based on priority
        fringe.sort(key=lambda node: node[2])

    return []

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

    

