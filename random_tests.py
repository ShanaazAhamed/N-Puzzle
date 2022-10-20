import numpy as np
import random
from copy import deepcopy
import scipy.stats as stats
import command_line_n_puzzle 

def find(Puzzle):
    for i in range(len(Puzzle)):
        for j in range(len(Puzzle)):
            if Puzzle[i][j] == '-':
                return (i, j)

def shuffle_puzzle(puzzle, iterations):
    t = deepcopy(puzzle)
    for i in range(iterations):
        x, y = find(t)
        moves = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
        while True:
            p, q = random.choice(moves)
            if (0 <= p < len(puzzle) and 0 <= q < len(puzzle)):
                break
        t[p][q], t[x][y] = t[x][y], t[p][q]
    return t

def random_puzzle_creation(n):
    puzzle = np.full((n, n), '-', dtype=object)
    items = list(range(1, n**2 + 1))
    mixed_items = items[:]
    random.shuffle(mixed_items)
    for i in items[:-2]:
        x = (mixed_items[i-1] - 1)//n
        y = mixed_items[i-1]-1-x*n
        puzzle[x][y] = str(i)
    return puzzle.tolist()


if __name__ == "__main__":
    N = 100
    start, goal = [], []
    misplaced_steps,manhattan_steps = [],[]
    i = 0
    while i < N:
        n = random.randint(4, 20)
        different_moves = random.randint(12, 15)
        start = random_puzzle_creation(n)
        goal = shuffle_puzzle(start, different_moves)

        if start != goal:
            print("i", i+1)
            print("Start: ", start,"\n")
            print("Goal: ", goal,"\n")

            misplaced_moves = command_line_n_puzzle.process(n,start,goal,1)
            print("Misplaced Steps Count: ",misplaced_moves,"\n")
            

            manhattan_moves = command_line_n_puzzle.process(n,start,goal,2)
            print("Manhattan Steps: ",manhattan_moves,"\n")

            manhattan_steps.append(manhattan_moves)
            misplaced_steps.append(misplaced_moves)
            i += 1
    
    mean = abs(np.mean(misplaced_steps)-np.mean(manhattan_steps))
    alpha = 0.05
    t_score, p_val = (stats.ttest_rel(misplaced_steps, manhattan_steps))

    print("Mean difference: ", mean)
    print("Test statistic score: ",t_score)
    print("P value: ",p_val)
    if p_val <= alpha:
        print('Difference between two algorithms')
    else:
        print('No difference between two algorithms')







