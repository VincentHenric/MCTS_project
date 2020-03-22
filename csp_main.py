#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 18:49:02 2020

@author: henric
"""

import sudoku
import constraint
import csp_problems
import parser

import logging
import os
import time
#puzzle = sudoku.random_puzzle(27, 3, model = 'CP')

#NO_FILE = [nqueens]

class Experiment:
    def __init__(self, class_of_problems, solver=constraint.BacktrackingSolver()):
        #logging.basicConfig(filename='stats_{}.log'.format(class_of_problems), level=logging.INFO)
        self.path= 'data/{}/data'.format(class_of_problems)
        self.parser_func = parser.PARSE[class_of_problems]
        self.class_of_problems = class_of_problems
        self.output_file = 'stats_{}_{}.log'.format(class_of_problems, solver.name)
        self.solver = solver
        
    def write(self, msg):
        with open(self.output_file, 'a') as file:
            file.write(msg + '\n')
        
    def launch(self, filenames=None, timeout=300, symmetry_break=False):
        if not filenames:
            filenames = os.listdir(self.path)
        for filename in filenames:
            print('processing for {} started'.format(filename))
            try:
                csp_object = self.parser_func(filename)
                if symmetry_break:
                    self.solver.change_logfile('{}-{}_{}'.format(self.class_of_problems, 'sym', filename))
                else:
                    self.solver.change_logfile('{}_{}'.format(self.class_of_problems, filename))
                start_time = time.time()
                new_csp_object, finished = csp_problems.solve_with_timeout(csp_object, solver=self.solver, timeout_sec=timeout, symmetry_break=symmetry_break)()
                #new_csp_object = csp_problems.solve(csp_object, solver=solver)
                end_time = time.time()
                res = {'filename':filename, 'time':round(end_time-start_time, 5), 'solver':self.solver.name, 'solved':new_csp_object.is_solved()}
                self.write(str(res))
            except:
                self.write('{} encountered an error'.format(filename))
                continue
            print('processing for {} finished'.format(filename))
        return True
                
                
if __name__ == '__main__':  
    if False:
        #exp = Experiment('nqueens', solver=constraint.NMCSSolver(level=1))
        exp = Experiment('nqueens', solver=constraint.BacktrackingSolver())
        exp.launch(None, timeout=300, symmetry_break=True)

    if False:
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
        
    if False:
        filename = '4_4'
        #filename = '3_3'
        puzzle = parser.parse_sudoku(filename)
        #puzzle_solved_backtrack = csp_problems.solve(puzzle, solver=constraint.BacktrackingSolver())
        start_time = time.time()
        puzzle_solved_nmcs = csp_problems.solve(puzzle, solver=constraint.NMCSSolver(level=1))
        end_time = time.time()
        #print(puzzle_solved_backtrack)
        print(end_time-start_time)
        print(puzzle_solved_nmcs)
    
    if False:
        nqueens = csp_problems.NQueens(8)
        nq_solved_backtrack = csp_problems.solve(nqueens, solver=constraint.BacktrackingSolver())
        nq_solved_nmcs = csp_problems.solve(nqueens, solver=constraint.NMCSSolver(level=1))
        print(nq_solved_backtrack)
        print(nq_solved_nmcs)
        
    if True:
        nqueens = csp_problems.NQueens_2(16)
        solver = constraint.NRPA(level=1, playouts=100)
        nq_solved_nrpa = csp_problems.solve(nqueens, solver=solver)
        print(nq_solved_nrpa)
        
    if False:
        nqueens = csp_problems.NQueens_3(4)
        nq_solved_backtracks = csp_problems.solve_all(nqueens, solver=constraint.BacktrackingSolver(), symmetry_break=True)
        for k in range(min(len(nq_solved_backtracks),20)):
            print(nq_solved_backtracks[k])
        print(len(nq_solved_backtracks))
        
    if False:
        nqueens = csp_problems.NQueens_2(4)
        nq_solved_backtracks = csp_problems.solve_all(nqueens, solver=constraint.BacktrackingSolver(), symmetry_break=True)
        for k in range(min(len(nq_solved_backtracks),20)):
            print(nq_solved_backtracks[k])
        print(len(nq_solved_backtracks))
        
    if False:
        nqueens = csp_problems.NQueens_3(4)
        p = nqueens.create_csp_problem(solver=constraint.BacktrackingSolver(), symmetry_break=False)
        sol = p.getSolution()
    
    if False:
        nqueens = csp_problems.NQueens_3(4)
        nq_solved_backtrack = csp_problems.solve(nqueens, solver=constraint.BacktrackingSolver(), symmetry_break=False)
        #nq_solved_nmcs = csp_problems.solve(nqueens, solver=constraint.NMCSSolver(level=1),)
        print(nq_solved_backtrack)
        #print(nq_solved_nmcs)
        
    if False:
        filename = 'gc_100_3_10'
        graph = parser.parse_coloring(filename)
        graph_solved_backtrack = csp_problems.solve(graph, solver=constraint.BacktrackingSolver())
        graph_solved_nmcs = csp_problems.solve(graph, solver=constraint.NMCSSolver(level=1))
        print(graph_solved_backtrack)
        print(graph_solved_nmcs)
        
    if False:
        filename = 'gc_100_1_5'
        timeout_sec = 300
        graph = parser.parse_coloring(filename)
        graph_solved_backtrack, finished_backtrack = csp_problems.solve_with_timeout(graph, solver=constraint.BacktrackingSolver(), timeout_sec=timeout_sec)()
        graph_solved_nmcs, finished_nmcs = csp_problems.solve_with_timeout(graph, solver=constraint.NMCSSolver(level=1), timeout_sec=timeout_sec)()
        print(graph_solved_backtrack)
        print(graph_solved_nmcs)