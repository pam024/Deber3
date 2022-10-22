from hashlib import new
import json
import math
from collections import deque
from copy import deepcopy
from queue import PriorityQueue
from timeit import default_timer

# Goal state of the puzzle
goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
str_goal = "".join(str(t) for t in goal)

# Calculates the possible moves of the blank tile.
def get_moves(puzzle):
    pos = puzzle.index(0)

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
def move(puzzle, direction):
    # Creates a copy of the new_puzzle to change it.
    new_puzzle = deepcopy(puzzle)
    pos = puzzle.index(0)
    # Position blank tile will move to.
    new_pos = pos + direction
    # Swap tiles.
    new_puzzle[pos], new_puzzle[new_pos] = new_puzzle[new_pos], new_puzzle[pos]

    return new_puzzle

def findMove(number):
    if(number==-1):
        move_tile = "Left"
    elif(number==1):
        move_tile = "Right"
    elif(number==3):
        move_tile = "Down"
    elif(number==-3):
        move_tile = "Up"

    return move_tile


# Creates the database.
def createDatabase():
    # Initializes a timer, starting state, queue and visited set.
    begin = default_timer()
    start = goal
    queue = deque([[start, 0]])
    entries = set()
    visited = set()
    entriesM = set()

    print("Generating database...")
    print("Collecting entries...")
    # BFS taking into account a state and the cost (number of moves) to reach it from the starting state.
    while queue:
        state_cost = queue.popleft()
        state = state_cost[0]
        cost = state_cost[1]

        for m in get_moves(state):
            next_state = move(state, m)

            # Increases cost if blank tile swapped with number tile.
            pos = state.index(0)
            if next_state[pos] > 0:
                next_state_cost = [next_state, cost+1]
            else:
                next_state_cost = [next_state, cost]

            if not "".join(str(t) for t in next_state) in visited:
                queue.append(next_state_cost)

            manhattanCost = sum(abs(b%3 - g%3) + abs(b//3 - g//3) for b, g in ((state.index(i), goal.index(i)) for i in range(1, 9)))

            
            entries.add(("".join(str(t) for t in state), cost))
            entriesM.add(("".join(str(t) for t in state), manhattanCost))
            
            visited.add("".join(str(t) for t in state))

        # Exit loop when all permutations for the puzzle have been found.
        if len(entries) >= 181440*2:
            break

    print("Writing entries to database...")
    # Writes entries to the text file, sorted by cost in ascending order .
    with open("database.txt", "w") as f:
        
        for entry in sorted(entries, key=lambda c: c[1]):
            json.dump(entry, f)
            f.write("\n")
    
    dic = {}
    with open("databaseM.json", "w") as f1:
        for entry in sorted(entriesM, key=lambda c: c[1]):
            dic[entry[0]]= entry[1]
    
        json.dump(dic, f1)
    

    end = default_timer()
    minutes = math.floor((end-begin)/60)
    seconds = math.floor((end-begin) % 60)
    return "Generated database in " + str(minutes) + " minute(s) and " + str(seconds) + " second(s)."


print(createDatabase())



def searchSolutionManhattan(puzzle):
    
    print("Complete board state", puzzle)

    #Read from archive 
    f2 = open('databaseM.json')
    js = json.load(f2)

    str_puzzle = "".join(str(t) for t in puzzle)
    start_cost = js[str_puzzle]
    node = puzzle
    frontier = PriorityQueue()
    frontier.put((start_cost,node))
    reached = {str_puzzle:start_cost}
    reached0 = {str_puzzle: 0}
    reached_path = {str_puzzle: "Start"}
    num_nodes = 0

    while not frontier.empty():
        node = frontier.get()[1]
        str_node = "".join(str(t) for t in node)
        nodeCost = reached0.get(str_node)
        
        if (node == goal):
            reached_path[str_goal] = reached_path[str_node] + ", End"
            print ("Number of nodes expanded: ", reached0.__len__(), "\nPath cost: ",reached.get(str_goal), "\nPath: ",reached_path[str_goal])
        
        for m in get_moves(node):
            child = move(node, m)
            str_child = "".join(str(t) for t in child)
            child_cost0 = nodeCost + 1
            child_cost = js[str_child] + child_cost0
            if not reached.__contains__(str_child) or child_cost < reached.get(str_child):
                num_nodes+=1
                reached[str_child] = child_cost
                reached0[str_child] = child_cost0
                reached_path[str_child] = reached_path[str_node] + ", " + findMove(m) 
                frontier.put((child_cost, child))


    return "\n"

print ("\nManhattan heuristic")
print (searchSolutionManhattan([2, 3, 5, 1, 4, 7, 0, 8, 6]))