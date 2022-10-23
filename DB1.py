import json
import math
from collections import deque
from copy import deepcopy
from timeit import default_timer

# Goal state of the puzzle
goal = [1, 2, 3, 4, 0, 0, 0, 0, 0]
str_goal = "".join(str(t) for t in goal)

# Calculates the possible moves of the blank tile.
def get_moves(puzzle, tile):
    pos = puzzle.index(tile)

    if pos == 0:
        possible_moves = [1, 3]
    elif pos == 1:
        possible_moves = [1, 3, -1]
    elif pos == 2:
        possible_moves = [3, -1]
    elif pos == 3:
        possible_moves = [-3, 1, 3]
    elif pos == 4:
        possible_moves = [-3, 1, 3, -1]
    elif pos == 5:
        possible_moves = [-3, 3, -1]
    elif pos == 6:
        possible_moves = [-3, 1]
    elif pos == 7:
        possible_moves = [-3, 1, -1]
    else:
        possible_moves = [-3, -1]

    return possible_moves

# Moves the blank tile in the puzzle.
def move(puzzle, direction, tile):
    # Creates a copy of the new_puzzle to change it.
    new_puzzle = deepcopy(puzzle)
    pos = puzzle.index(tile)
    # Position blank tile will move to.
    new_pos = pos + direction
    # Swap tiles.
    new_puzzle[pos], new_puzzle[new_pos] = new_puzzle[new_pos], new_puzzle[pos]

    return new_puzzle

# Creates the database.
def createDatabase():
    # Initializes a timer, starting state, queue and visited set.
    begin = default_timer()
    start = [1, 2, 3, 4, 0, 0, 0, 0, 0]
    queue = deque([[start, 0]])
    reached = {str_goal: 0}

    print("Generating database...")
    print("Collecting entries...")
    # BFS taking into account a state and the cost (number of moves) to reach it from the starting state.
    while queue:
        state_cost = queue.popleft()
        state = state_cost[0]
        cost = state_cost[1]

        for i in range(1,5):
            for m in get_moves(state,i):
                next_state = move(state, m,i)
                str_next_state = "".join(str(t) for t in next_state)
                next_state_cost = 0

                # Increases cost if blank tile swapped with number tile.
                pos = state.index(i)
                if next_state[pos] == 0:
                    next_state_cost = cost + 1

                    if not (next_state_cost==0):
                        if not reached.__contains__(str_next_state):
                            reached [str_next_state] = cost
                            queue.append([next_state, next_state_cost])


        # Exit loop when all permutations for the puzzle have been found.
        if len(reached) >= 362880:
            break


    print("Writing entries to database...")
    # Writes entries to the text file, sorted by cost in ascending order .
    with open("db1.json", "w") as f:
            json.dump(reached, f)
    
    
    end = default_timer()
    minutes = math.floor((end-begin)/60)
    seconds = math.floor((end-begin) % 60)
    return "Generated database in " + str(minutes) + " minute(s) and " + str(seconds) + " second(s)."

print(createDatabase())