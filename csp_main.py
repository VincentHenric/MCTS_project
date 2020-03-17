#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:49:02 2020

@author: henric
"""

import sudoku
import constraint
import csp_problems

#puzzle = sudoku.random_puzzle(27, 3, model = 'CP')

fixed = {1: 9,
         2: 8,
         3: 7,
         5: 5,
         6: 4,
         11: 5,
         12: 4,
         18: 7,
         13: 3,
         19: 3,
         20: 2,
         22: 9,
         28: 8,
         29: 7,
         35: 1,
         52: 8,
         45: 6,
         53: 9,
         59: 4,
         64: 5,
         65: 6,
         68: 1,
         74: 4,
         75: 2,
         76: 7,
         78: 9,
         80: 3}

fixed = {8: 2, 9: 1, 16: 9, 17: 8, 18: 7, 15: 1, 19: 3, 20: 2, 22: 9, 25: 6, 28: 8, 29: 7, 34: 2, 50: 7, 43: 7, 38: 3, 37: 2, 42: 8, 46: 4, 47: 1, 58: 8, 65: 6, 73: 1, 66: 8, 69: 3, 76: 7, 81: 8}

boxsize = 3

puzzle = sudoku.Puzzle(fixed, boxsize, format = 'd')
print(puzzle)

solved = sudoku.solve(puzzle, model = 'CP')
print(solved)


solved_2 = sudoku.solve(puzzle, model = 'CP', solver=constraint.BacktrackingSolver())
print(solved_2)

solved_3 = sudoku.solve(puzzle, model = 'CP', solver=constraint.NMCSSolver(level=2))
print(solved_3)

nqueens = csp_problems.NQueens(8)
nq_solved_backtrack = csp_problems.solve(nqueens, solver=constraint.BacktrackingSolver(), logfile=None)
nq_solved_nmcs = csp_problems.solve(nqueens, solver=constraint.NMCSSolver(level=1), logfile=None)
print(nq_solved_backtrack)
print(nq_solved_nmcs)

nqueens = csp_problems.NQueens_2(16)
nq_solved_backtrack = csp_problems.solve(nqueens, solver=constraint.BacktrackingSolver(), logfile=None)
nq_solved_nmcs = csp_problems.solve(nqueens, solver=constraint.NMCSSolver(level=1), logfile=None)
print(nq_solved_backtrack)
print(nq_solved_nmcs)