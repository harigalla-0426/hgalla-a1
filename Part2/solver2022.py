#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: hgalla, rathlur, pfyffe
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
import numpy as np
import time
from queue import PriorityQueue

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    successor_list = []

    # slide rows
    successor_list += slide_row(state)

    transpose_board = np.transpose(np.copy(state))

    # slide columns
    successor_list += slide_row(transpose_board, True)

    # inner and outer rotations
    successor_list += rotate_board(state)

    return successor_list


def slide_row(original_board, is_col = False):
    slide_row_successors = []

    for row_start in range(0, 5, 1):
        row_indices = [ x for x in range(5*row_start, 5*row_start + 5, 1)]

        board = np.copy(original_board)
        board.flat[row_indices] = np.roll(board.flat[row_indices], 1)

        if is_col:
            slide_row_successors.append((np.transpose(board), 'D' + str(row_start+1)))
        else:
            slide_row_successors.append(( board, 'R' + str(row_start+1) ))

        board = np.copy(original_board)
        board.flat[row_indices] = np.roll(board.flat[row_indices], -1)

        if is_col:
            slide_row_successors.append(((np.transpose(board), 'U' + str(row_start+1))))
        else:
            slide_row_successors.append(( board, 'L' + str(row_start+1) ))
    
    return slide_row_successors

def rotate_board(original_board):
    outerInd= np.array([0, 1, 2,3,4,9,14,19,24,23,22,21,20,15,10,5])
    innerInd=np.array([6,7,8,13,18,17,16,11])
    rotate_board_successors = []
    
    board = np.copy(original_board)
    board.flat[outerInd]=np.roll(board.flat[outerInd], 1)
    rotate_board_successors.append(( board, 'Oc' ))
    
    board = np.copy(original_board)
    board.flat[outerInd]=np.roll(board.flat[outerInd], -1)
    rotate_board_successors.append(( board, 'Occ' ))
    
    board = np.copy(original_board)
    board.flat[innerInd]=np.roll(board.flat[innerInd], 1)
    rotate_board_successors.append(( board, 'Ic' ))
    
    board = np.copy(original_board)
    board.flat[innerInd]=np.roll(board.flat[innerInd], -1)
    rotate_board_successors.append(( board, 'Icc' ))

    return rotate_board_successors

# heuristic function: Manhattan distance for each board element all 4 possible directions taking the rotations also into consideration.
# See report for how it works / what it does.
def h(state, initialPositions):
    # Manhattan Distance: |desired_x - current_x| + |desired_y - current_y|

    distArr = []

    for i in range(ROWS):
        for j in range(COLS):
            (target_x, target_y) = initialPositions[state[i][j]]

            diff_array = [abs(target_x - i)  + abs(target_y - j), abs(5 - (target_x - i))+ abs(target_y - j), abs(target_x - i) + abs(5 - (target_y - j)), abs(5 - (target_x - i)) + abs(5 - (target_y - j))]

            distArr.append(min(diff_array))

    return np.sum(distArr) // 5



# check if we've reached the goal
def is_goal(state):
    goal_state = np.arange(25).reshape(5, 5) + 1

    if (state==goal_state).all():
        return True

    return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    initial_board_state = np.array(list(initial_board)).reshape((5,5))

    fringe = PriorityQueue()

    fringe.put((0, [], initial_board_state))

    initialPositions = {}

    initialBoard = np.arange(1,26).reshape(5, 5)

    for row in range(ROWS):
        for col in range(COLS):
            initialPositions[initialBoard[row][col]]=[row,col]

    while fringe:
        (heuristic_value, moves_array, current_board_state) =  fringe.get()

        if current_board_state.shape != (5,5):
            np.array(current_board_state).reshape((5,5))

        for ( successor, move ) in successors(current_board_state):
            if is_goal(successor):
                moves_array.append(move)
                return moves_array

            updated_moves = moves_array.copy()
            updated_moves.append(move)
            fringe.put((h(successor, initialPositions) + len(updated_moves), updated_moves, successor))
    else:
        print('No solution Found!')


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    start_time = time.time()
    route = solve(tuple(start_state))
    end_time = time.time()
    
    print('Time: ', (end_time - start_time))
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
    