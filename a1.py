# a1.py

from search import *

def make_rand_8puzzle():

	state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
	puzzle = EightPuzzle(state)

	for i in range(100):

		validAction = False

		while(validAction == False):
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
	display(state)
	if puzzle.check_solvability(state) == True:
		return EightPuzzle(state)
	else:
		return "Error"

def display(state):
	
	for i in range(9):

		if state[i] == 0:
			print('*', end = ' ')
		else:
			print(state[i], end = ' ')

		if (i+1) % 3 == 0:
			print('\n', end = '')

def display_duck(state):

	for i in range(9):

		if state[i] == 0:
			print('*', end = ' ')
		else:
			print(state[i], end = ' ')

		if i == 1:
			print('\n', end = '')
		elif i == 5:
			print('\n  ', end = '')

make_rand_8puzzle()