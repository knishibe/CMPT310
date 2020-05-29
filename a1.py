# a1.py

from search import *
import time

def make_rand_8puzzle():
    #create a random eight puzzle
	state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	puzzle = EightPuzzle(state)

    #do 100 moves
	for i in range(100):

		validAction = False

		while(validAction == False):
            #continue until random move is valid
			y = random.randint(0, 3)
			actions = puzzle.actions(state)

			if y == 0:
				action = "UP"
			elif y == 1:
				action = "DOWN"
			elif y == 2:
				action = "LEFT"
			elif y == 3:
				action = "RIGHT"

			if(action in actions):
				validAction = True

		state = puzzle.result(state, action)

	return EightPuzzle(state)

def display(state):
	#display an eight puzzle from a given state
	for i in range(9):

		if state[i] == 0:
			print('*', end = ' ')
		else:
			print(state[i], end = ' ')

		if (i+1) % 3 == 0:
			print('\n', end = '')

def display_duck(state):
    #display a duck puzzle from a given state
	for i in range(9):

		if state[i] == 0:
			print('*', end = ' ')
		else:
			print(state[i], end = ' ')

		if i == 1:
			print('\n', end = '')
		elif i == 5:
			print('\n  ', end = '')

def astar_search(problem, h=None, display=False):
    #taken from search.py
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def best_first_graph_search(problem, f, display=False):
    #taken from search.py and added a counter
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    global counter
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            counter = len(explored) + 1
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def h(node):
    #Missing Tile Heuristic Function 
    #taken from EightPuzzle in search.py
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    sum = 0
    for i in range(0,9):
        if node.state[i] != 0 and node.state[i] != goal[i]:
            sum += 1
    return sum

def h2(node):
    # Manhattan Heuristic Function

    sum = 0
    v = 0
    h = 0

    for i in range(0,9):
        if node.state[i] == 0:
            continue
        else:
            v = abs(((node.state[i] - 1) // 3) - (i//3))
            h = abs(((node.state[i] - 1) % 3) - (i%3))

        sum += v
        sum += h
    return sum

def h3(node):
    # Heuristic Function Max of Manhattan and Missing Tile
	return max(h2(node), h(node))

def solve_puzzle(puzzleNum, puzzle):
    #helper function to solve puzzle and print results
	global counter
	counter = 0
	t1 = time.time()
	if puzzleNum == 1:
		node = astar_search(puzzle, h=h, display = False)
	elif puzzleNum == 2:
		node = astar_search(puzzle, h=h2, display = False)
	elif puzzleNum == 3:
		node = astar_search(puzzle, h=h3, display = False)
	t2 = time.time()

	print("Nodes Removed:", (counter))
	print("Length:", len(node.solution()))
	print("Total time elapsed:", (t2-t1), "\n")


class DuckPuzzle(Problem):
    #Duck puzzle problem

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        """ Define goal state and initialize a problem """
        super().__init__(initial, goal)

    def find_blank_square(self, state):
        return state.index(0)

    def actions(self, state):
        #taken from EightPuzzle in search.py and modified to work for DuckPuzzle
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        index_blank_square = self.find_blank_square(state)

        if index_blank_square == 0 or index_blank_square == 2 or index_blank_square == 6:
            possible_actions.remove('LEFT')
        if index_blank_square < 2 or index_blank_square == 4 or index_blank_square == 5:
            possible_actions.remove('UP')
        if index_blank_square == 1 or index_blank_square == 5 or index_blank_square == 8:
            possible_actions.remove('RIGHT')
        if index_blank_square > 5 or index_blank_square == 2:
            possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        #taken from EightPuzzle in search.py and modified to work for DuckPuzzle
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

        # blank is the index of the blank square
        blank = self.find_blank_square(state)
        new_state = list(state)

        if blank <= 1:
            delta = {'UP': -2, 'DOWN': 2, 'LEFT': -1, 'RIGHT': 1}
        elif blank > 1 and blank <= 3:
            delta = {'UP': -2, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        else:
            delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return tuple(new_state)

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        # Misplaced Tile Heuristic
        #taken from EightPuzzle in search.py
        goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        sum = 0
        for i in range(0,9):
            if node.state[i] != 0 and node.state[i] != goal[i]:
                sum += 1
        return sum

    def h2(self, node):
        # Manhattan Heuristic
        sum = 0
        v1 = 0
        v2 = 0
        h1 = 0
        h2 = 0
        
        for i in range(0,9):

            if node.state[i] == 0:
                continue
            
            if node.state[i] < 3 and node.state[i] != 0:
                v2 = 1
            elif node.state[i] >= 3 and node.state[i] < 7:
                v2 = 2
            else:
                v2 = 3
            
            if i < 2:
                v1 = 1
            elif i >= 2 and i < 6:
                v1 = 2
            else:
                v1 = 3

            if node.state[i] == 1 or node.state[i] == 3:
                h2 = 1
            elif node.state[i] == 2 or node.state[i] == 4 or node.state[i] == 7:
                h2 = 2
            elif node.state[i] == 5 or node.state[i] == 8:
                h2 = 3
            else:
                h2 = 4

            if i == 0 or i == 2:
                h1 = 1
            elif i == 1 or i == 3 or i == 6:
                h1 = 2
            elif i == 4 or i == 7:
                h1 = 3
            else:
                h1 = 4

            v = abs(v2 - v1)
            h = abs(h2 - h1)
            sum += v
            sum += h

        return sum

    def h3(self, node):
        # Max of Misplaced Tile Heuristic and Manhattan Heuristic
        return max(self.h2(node), self.h(node))

def make_rand_duckPuzzle():

    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    puzzle = DuckPuzzle(state)
    
    for i in range(100):
        
        validAction = False
        #do 100 actions to mix puzzle up
        
        while(validAction == False):
            #continue until random action is valid
            y = random.randint(0, 3)
            actions = puzzle.actions(state)
            
            if y == 0:
                action = "UP"
            elif y == 1:
                action = "DOWN"
            elif y == 2:
                action = "LEFT"
            elif y == 3:
                action = "RIGHT"
                
            if(action in actions):
                validAction = True

        #do valid action on puzzle
        state = puzzle.result(state, action)

    return DuckPuzzle(state)

def solve_puzzle_duck(puzzleNum, puzzle):
    #helper function to solve puzzle and print results

	global counter
	counter = 0
	t1 = time.time()
	if puzzleNum == 1:
		node = astar_search(puzzle, h=puzzle.h, display = False)
	elif puzzleNum == 2:
		node = astar_search(puzzle, h=puzzle.h2, display = False)
	elif puzzleNum == 3:
		node = astar_search(puzzle, h=puzzle.h3, display = False)
	t2 = time.time()

	print("Nodes Removed:", (counter))
	print("Length:", len(node.solution()))
	print("Total time elapsed:", (t2-t1), "\n")


# Main

counter = 0

# create 10 random eight puzzles
puzzle1 = make_rand_8puzzle()
puzzle2 = make_rand_8puzzle()
puzzle3 = make_rand_8puzzle()
puzzle4 = make_rand_8puzzle()
puzzle5 = make_rand_8puzzle()
puzzle6 = make_rand_8puzzle()
puzzle7 = make_rand_8puzzle()
puzzle8 = make_rand_8puzzle()
puzzle9 = make_rand_8puzzle()
puzzle10 = make_rand_8puzzle()

#create 10 random duck puzzles
duck1 = make_rand_duckPuzzle()
duck2 = make_rand_duckPuzzle()
duck3 = make_rand_duckPuzzle()
duck4 = make_rand_duckPuzzle()
duck5 = make_rand_duckPuzzle()
duck6 = make_rand_duckPuzzle()
duck7 = make_rand_duckPuzzle()
duck8 = make_rand_duckPuzzle()
duck9 = make_rand_duckPuzzle()
duck10 = make_rand_duckPuzzle()

puzzle11 = puzzle1
puzzle12 = puzzle2
puzzle13 = puzzle3
puzzle14 = puzzle4
puzzle15 = puzzle5
puzzle16 = puzzle6
puzzle17 = puzzle7
puzzle18 = puzzle8
puzzle19 = puzzle9
puzzle20 = puzzle10

puzzle21 = puzzle1
puzzle22 = puzzle2
puzzle23 = puzzle3
puzzle24 = puzzle4
puzzle25 = puzzle5
puzzle26 = puzzle6
puzzle27 = puzzle7
puzzle28 = puzzle8
puzzle29 = puzzle9
puzzle30 = puzzle10

duck11 = duck1
duck12 = duck2
duck13 = duck3
duck14 = duck4
duck15 = duck5
duck16 = duck6
duck17 = duck7
duck18 = duck8
duck19 = duck9
duck20 = duck10

duck21 = duck1
duck22 = duck2
duck23 = duck3
duck24 = duck4
duck25 = duck5
duck26 = duck6
duck27 = duck7
duck28 = duck8
duck29 = duck9
duck30 = duck10


print("Misplaced Tile Heuristic\n")

solve_puzzle(1, puzzle1)
solve_puzzle(1, puzzle2)
solve_puzzle(1, puzzle3)
solve_puzzle(1, puzzle4)
solve_puzzle(1, puzzle5)
solve_puzzle(1, puzzle6)
solve_puzzle(1, puzzle7)
solve_puzzle(1, puzzle8)
solve_puzzle(1, puzzle9)
solve_puzzle(1, puzzle10)

print("Manhattan Heuristic\n")

solve_puzzle(2, puzzle11)
solve_puzzle(2, puzzle12)
solve_puzzle(2, puzzle13)
solve_puzzle(2, puzzle14)
solve_puzzle(2, puzzle15)
solve_puzzle(2, puzzle16)
solve_puzzle(2, puzzle17)
solve_puzzle(2, puzzle18)
solve_puzzle(2, puzzle19)
solve_puzzle(2, puzzle20)

print("Max of Misplaced Tile and Manhattan Heuristic\n")

solve_puzzle(3, puzzle21)
solve_puzzle(3, puzzle22)
solve_puzzle(3, puzzle23)
solve_puzzle(3, puzzle24)
solve_puzzle(3, puzzle25)
solve_puzzle(3, puzzle26)
solve_puzzle(3, puzzle27)
solve_puzzle(3, puzzle28)
solve_puzzle(3, puzzle29)
solve_puzzle(3, puzzle30)

print("Misplaced Tile Heuristic Duck\n")

solve_puzzle_duck(1, duck1)
solve_puzzle_duck(1, duck2)
solve_puzzle_duck(1, duck3)
solve_puzzle_duck(1, duck4)
solve_puzzle_duck(1, duck5)
solve_puzzle_duck(1, duck6)
solve_puzzle_duck(1, duck7)
solve_puzzle_duck(1, duck8)
solve_puzzle_duck(1, duck9)
solve_puzzle_duck(1, duck10)

print("Manhattan Heuristic Duck\n")

solve_puzzle_duck(2, duck11)
solve_puzzle_duck(2, duck12)
solve_puzzle_duck(2, duck13)
solve_puzzle_duck(2, duck14)
solve_puzzle_duck(2, duck15)
solve_puzzle_duck(2, duck16)
solve_puzzle_duck(2, duck17)
solve_puzzle_duck(2, duck18)
solve_puzzle_duck(2, duck19)
solve_puzzle_duck(2, duck20)

print("Max of Misplaced Tile and Manhattan Heuristic Duck\n")

solve_puzzle_duck(3, duck21)
solve_puzzle_duck(3, duck22)
solve_puzzle_duck(3, duck23)
solve_puzzle_duck(3, duck24)
solve_puzzle_duck(3, duck25)
solve_puzzle_duck(3, duck26)
solve_puzzle_duck(3, duck27)
solve_puzzle_duck(3, duck28)
solve_puzzle_duck(3, duck29)
solve_puzzle_duck(3, duck30)
