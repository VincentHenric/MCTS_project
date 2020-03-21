#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:41:45 2020

@author: henric
"""
import sudoku
import constraint

import numpy as np
import time
from threading import Thread, Event
from multiprocessing import Process, Queue
import copy
import string
import itertools
import functools

class TimeoutException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
   
def solve_with_timeout(problem, solver=constraint.BacktrackingSolver(), timeout_sec=300, symmetry_break=False):
    def solve():
        finished = True
        queue = Queue()
        proc = Process(target=solve2, args=(problem, solver, queue, symmetry_break))
        proc.start()
        try:
            problem2 = queue.get(timeout=timeout_sec)
        except:
            proc.terminate()
            problem2 = copy.deepcopy(problem)
            finished = False
        finally:
            return problem2, finished
            
    return solve
  
def solve2(problem, solver=constraint.BacktrackingSolver(), queue=None, symmetry_break=False):
    p = problem.create_csp_problem(solver, symmetry_break)
    fixed = p.getSolution()
    problem2 = copy.deepcopy(problem)
    problem2.fixed = fixed
    queue.put(problem2)
    
    
def solve(problem, solver=constraint.BacktrackingSolver(), symmetry_break=False):
    p = problem.create_csp_problem(solver, symmetry_break)
    fixed = p.getSolution()
    problem2 = copy.deepcopy(problem)
    problem2.fixed = fixed
    return problem2

def solve_all(problem, solver=constraint.BacktrackingSolver(), symmetry_break=False):
    p = problem.create_csp_problem(solver, symmetry_break)
    fixed_list = p.getSolutions()
    problems = []
    for fixed in fixed_list:
        problem2 = copy.deepcopy(problem)
        problem2.fixed = fixed
        problems.append(problem2)
    return problems

def vertical_symetry(*args):
    return args>args[::-1]

def horizontal_symetry(n):
    def func(*args):
        n = len(args)
        return args>tuple(n-x for x in args)
    return func

def diag_symetry(n):
    def func(*args):
        l2 = np.arange(n)
        l2[np.array(args)-1]=np.arange(n)+1
        return args>tuple(l2)
    return func

def anti_diag_symetry(n):
    def func(*args):
        l2 = np.arange(n)
        l2[n-np.array(args)]=n-np.arange(n)
        return args>tuple(l2)
    return func

def rotation_90(n):
    def func(*args):
        l2 = np.arange(n)
        l2[n-np.array(args)]=np.arange(n)
        return args>tuple(l2)
    return func

def rotation_180(n):
    def func(*args):
        l2 = np.arange(n)
        l2[n-1-np.arange(n)]=n+1-np.array(args)
        return args>=tuple(l2)
    return func

def rotation_270(n):
    def func(*args):
        l2 = np.arange(n)
        l2[np.array(args)-1]=n-np.arange(n)
        return args>tuple(l2)
    return func

#def lexicographic_order(*args):
#    return args<args[::-1]

class Problems:
    def __init__(self, fixed):
        self.fixed = fixed
    
    def create_csp_problem(self, solver=constraint.BacktrackingSolver(), symmetry_break=False):
        pass
    
    def is_solved(self):
        p = self.create_csp_problem(solver=constraint.BacktrackingSolver(), symmetry_break=False)
        return p.isSolution(self.fixed)
    
    
class Sudoku_problem(Problems):
    def __init__(self, fixed, boxsize, format = 'd'):
        self.boxsize = boxsize
        if format == 'd':
            self.fixed = fixed
        elif format == 's':
            self.fixed = sudoku.string_to_dict(fixed, boxsize)
        else:
            raise NameError('No such format: ' + format)
            
    def create_csp_problem(self, solver, symmetry_break=False):
        return sudoku.puzzle_as_CP(self.fixed, self.boxsize, solver=solver)

    def __repr__(self):
        return sudoku.dict_to_string(self.fixed, self.boxsize, padding = 1, rowend = "\n")

    def _repr_latex_(self):
        s = r"""$$\begin{array}"""
        s += '{' + self.boxsize*('|' + self.boxsize*'c') + '|' + '}'
        s += sudoku.dict_to_string_(self.fixed, self.boxsize, padding = 0, rowend = "\\\\ \n", row_sep = "\hline ", box_sep = "", col_sep = " & ", last_row_hack = "\hline")
        s += r"""\end{array}$$"""
        return s

    def __str__(self):
        return self.__repr__()

    def get_boxsize(self):
        return self.boxsize

    def get_fixed(self):
        return self.fixed

class NQueens(Problems):
    def __init__(self, n, fixed={}):
        self.size = n
        self.fixed = fixed
        
    def __repr__(self):
        return self.dict_to_string(padding = 1, rowend = "\n")

    def __str__(self):
        return self.__repr__()

    def get_boxsize(self):
        return self.boxsize

    def get_fixed(self):
        return self.fixed
    
    def create_csp_problem(self, solver=constraint.BacktrackingSolver(), symmetry_break=False):
        p = constraint.Problem(solver)
        p.addVariables(self.cells(), self.symbols()) 
        self.add_row_constraints(p)
        self.add_col_constraints(p)
        self.add_diag_left_constraints(p)
        self.add_diag_right_constraints(p)
#        if symmetry_break:
#            self.add_vertical_sym_constraint(p)
        return p
    
    def dict_to_string(self, padding = 0, rowend = "", row_sep = "", box_sep = "", col_sep = "", last_row_hack = ""):
        """Returns a puzzle string of dimension 'boxsize' from a dictionary of 
        'fixed' cells."""
        s = ''
        s += row_sep
        for row in range(1, self.size + 1):
            s += box_sep
            for col in range(1, self.size + 1):
                symbol = self.fixed.get(self.cell(row, col))
                if symbol is not None:
                    s += string.printable[symbol] + " "*padding
                else:
                    s += '.' + ' '*padding
                if col < self.n_cols():
                   s += col_sep
            s += rowend               
            if row == self.n_rows():
                s += last_row_hack
        return s

    def add_row_constraints(self, problem):
        """add_row_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on rows."""
        for row in self.cells_by_row():
            problem.addConstraint(constraint.ExactSumConstraint(1), row)
    
    def add_col_constraints(self, problem):
        """add_col_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on columns."""
        for col in self.cells_by_col():    
            problem.addConstraint(constraint.ExactSumConstraint(1), col)
            
    def add_diag_left_constraints(self, problem):
        """add_box_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on boxes."""
        for box in self.cells_by_diag_left():
            problem.addConstraint(constraint.MaxSumConstraint(1), box)
            
    def add_diag_right_constraints(self, problem):
        """add_box_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on boxes."""
        for box in self.cells_by_diag_right():
            problem.addConstraint(constraint.MaxSumConstraint(1), box)
    
            
    def cells_by_row(self):
        """cells_by_row(boxsize) -> list
    
        Returns a list of cell labels ordered by row for the given boxsize."""
        return [self.row_r(row) for row in self.rows()]
    
    def cells_by_col(self):
        """cells_by_col(boxsize) -> list
    
        Returns a list of cell labels ordered by column for the given boxsize."""
        return [self.col_r(column) for column in self.cols()]
    
    def cells_by_diag_left(self):
        """cells_by_col(boxsize) -> list
    
        Returns a list of cell labels ordered by column for the given boxsize."""
        return [self.diag_r_left(diag) for diag in self.diags_left()]
    
    def cells_by_diag_right(self):
        """cells_by_col(boxsize) -> list
    
        Returns a list of cell labels ordered by column for the given boxsize."""
        return [self.diag_r_right(diag) for diag in self.diags_right()]
    
    def rows(self): return range(1, self.n_rows() + 1)
    def cols(self): return range(1, self.n_cols() + 1)
    def diags_left(self): return range(2, self.n_diags_left() + 1)
    def diags_right(self): return range(1-self.n_rows(), -self.n_rows() + self.n_diags_right())
    def cell(self, row, column): return (row - 1) * self.n_rows() + column
    def symbols(self): return range(0, 1 + 1)    
    def cells(self): return range(1, self.n_cells() + 1)
    
    def row_r(self, row):
        """Cell labels in 'row' of Sudoku puzzle of dimension 'boxsize'."""
        nr = self.n_rows()
        return range(nr * (row - 1) + 1, nr * row + 1)
    
    def col_r(self, column):
        """Cell labels in 'column' of Sudoku puzzle of dimension 'boxsize'."""
        nc = self.n_cols()
        ncl = self.n_cells()
        return range(column, ncl + 1 - (nc - column), nc)
    
    def diag_r_left(self, diag):
        return [self.cell(diag-j,j) for j in range(max(1, diag-self.n_rows()), min(self.n_cols(), diag-1)+1)]
    
    def diag_r_right(self, diag):
        return [self.cell(diag+j,j) for j in range(max(1, 1-diag), min(self.n_cols(), self.n_rows()-diag)+1)]
    
    def n_rows(self): return self.size
    def n_cols(self): return self.size
    def n_diags_left(self): return 2*self.size
    def n_diags_right(self): return 2*self.size
    def n_cells(self): return self.n_rows()*self.n_cols()
    def n_symbols(self): return 2
    
    
class NQueens_2(Problems):
    def __init__(self, n, fixed={}):
        self.size = n
        self.fixed = fixed
        
    def __repr__(self):
        return self.dict_to_string(padding = 1, rowend = "\n")

    def __str__(self):
        return self.__repr__()

    def get_boxsize(self):
        return self.boxsize

    def get_fixed(self):
        return self.fixed
    
    def create_csp_problem(self, solver=constraint.BacktrackingSolver(), symmetry_break=False):
        p = constraint.Problem(solver)
        p.addVariables(self.rows(), self.cols()) 
        
        p.addConstraint(constraint.AllDifferentConstraint(), self.rows())
        self.add_diag_left_constraints(p)
        self.add_diag_right_constraints(p)
        if symmetry_break:
            #self.add_axes_sym_constraints(p)
            #self.add_rotation_sym_constraints(p)
            self.sym_constraints(p)
        return p
    
    def dict_to_string(self, padding = 0, rowend = "", row_sep = "", box_sep = "", col_sep = "", last_row_hack = ""):
        """Returns a puzzle string of dimension 'boxsize' from a dictionary of 
        'fixed' cells."""
        if len(self.fixed) == self.n_rows():
            default_symbol='0'
        else:
            default_symbol='.'
        s = ''
        s += row_sep
        for row in range(1, self.size + 1):
            s += box_sep
            col_pos = self.fixed.get(row)
            for col in range(1, self.size + 1):
                if col == col_pos:
                    s += "1" + " "*padding
                else:
                    s += default_symbol + ' '*padding
                if col < self.n_cols():
                   s += col_sep
            s += rowend               
            if row == self.n_rows():
                s += last_row_hack
        return s
    
    def left_constraint(self, i, j):
        def constraint(yi, yj):
            return i+yi!=j+yj
        return constraint
    
    def right_constraint(self, i, j):
        def constraint(yi, yj):
            return i-yi!=j-yj
        return constraint
    
    def add_axes_sym_constraints(self, problem):
        problem.addConstraint(constraint.FunctionConstraint(horizontal_symetry(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(vertical_symetry), self.rows())
        problem.addConstraint(constraint.FunctionConstraint(diag_symetry(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(anti_diag_symetry(self.n_rows()), self.rows()))
        
    def add_rotation_sym_constraints(self, problem):
        problem.addConstraint(constraint.FunctionConstraint(rotation_90(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(rotation_180(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(rotation_270(self.n_rows()), self.rows()))
           
    def sym_constraints(self, problem):
        problem.addConstraint(constraint.FunctionConstraint(lambda x,y: x-y<0), [self.rows()[i] for i in [0,-1]])
        problem.addConstraint(constraint.MaxSumConstraint((self.n_cols()+1)/2), [self.rows()[0]])
        
    def add_diag_left_constraints(self, problem):
        """add_box_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on boxes."""
        for i,j in itertools.combinations(self.rows(), 2):
            problem.addConstraint(constraint.FunctionConstraint(self.left_constraint(i,j)), [i, j])
            
    def add_diag_right_constraints(self, problem):
        """add_box_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on boxes."""
        for i,j in itertools.combinations(self.rows(), 2):
            problem.addConstraint(constraint.FunctionConstraint(self.right_constraint(i,j)), [i, j])
    
    def rows(self): return range(1, self.n_rows() + 1)
    def cols(self): return range(1, self.n_cols() + 1)
    def diags_left(self): return range(2, self.n_diags_left() + 1)
    def diags_right(self): return range(1-self.n_rows(), -self.n_rows() + self.n_diags_right())
    def cell(self, row, column): return (row - 1) * self.n_rows() + column
    def symbols(self): return range(0, 1 + 1)    
    def cells(self): return range(1, self.n_cells() + 1)
   
    def n_rows(self): return self.size
    def n_cols(self): return self.size
    def n_diags_left(self): return 2*self.size
    def n_diags_right(self): return 2*self.size
    def n_cells(self): return self.n_rows()*self.n_cols()
    def n_symbols(self): return 2
    

class NQueens_3(Problems):
    def __init__(self, n, fixed={}):
        self.size = n
        self.fixed = fixed
        
    def __repr__(self):
        return self.dict_to_string_2(padding = 1, rowend = "\n")

    def __str__(self):
        return self.__repr__()

    def get_boxsize(self):
        return self.boxsize

    def get_fixed(self):
        return self.fixed
    
    def create_csp_problem(self, solver=constraint.BacktrackingSolver(), symmetry_break=False):
        p = constraint.Problem(solver)
        p.addVariables(self.rows(), self.cols())
        p.addVariables(self.col_vars(), self.rows())
        
        p.addConstraint(constraint.AllDifferentConstraint(), self.rows())
        p.addConstraint(constraint.AllDifferentConstraint(), self.col_vars())
        self.add_diag_left_constraints(p)
        self.add_diag_right_constraints(p)
        self.add_dual_constraints(p)
        if symmetry_break:
            #self.add_axes_sym_constraints(p)
            #self.add_rotation_sym_constraints(p)
            self.sym_constraints(p)
        return p
    
    def dict_to_string(self, padding = 0, rowend = "", row_sep = "", box_sep = "", col_sep = "", last_row_hack = ""):
        """Returns a puzzle string of dimension 'boxsize' from a dictionary of 
        'fixed' cells."""
        if len(self.fixed) == self.n_rows()+self.n_cols():
            default_symbol='0'
        else:
            default_symbol='.'
        s = ''
        s += row_sep
        for row in range(1, self.size + 1):
            s += box_sep
            col_pos = self.fixed.get(row)
            for col in range(1, self.size + 1):
                if col == col_pos:
                    s += "1" + " "*padding
                else:
                    s += default_symbol + ' '*padding
                if col < self.n_cols():
                   s += col_sep
            s += rowend               
            if row == self.n_rows():
                s += last_row_hack
        return s
    
    def dict_to_string_2(self, padding = 0, rowend = "", row_sep = "", box_sep = "", col_sep = "", last_row_hack = ""):
        """Returns a puzzle string of dimension 'boxsize' from a dictionary of 
        'fixed' cells."""
        if len(self.fixed) == self.n_rows()+self.n_cols():
            default_symbol='0'
        else:
            default_symbol='.'
    
        assignments = {k-self.n_rows():v for (k,v) in self.fixed.items() if k>self.n_rows()}
        fixed={v:k for k,v in assignments.items()}
        
        s = ''
        s += row_sep
        for row in range(1, self.size + 1):
            s += box_sep
            col_pos = fixed.get(row)
            for col in range(1, self.size + 1):
                if col == col_pos:
                    s += "1" + " "*padding
                else:
                    s += default_symbol + ' '*padding
                if col < self.n_cols():
                   s += col_sep
            s += rowend               
            if row == self.n_rows():
                s += last_row_hack
        return s
    
    def left_constraint(self, i, j):
        def constraint(yi, yj):
            return i+yi!=j+yj
        return constraint
    
    def right_constraint(self, i, j):
        def constraint(yi, yj):
            return i-yi!=j-yj
        return constraint
    
    def add_axes_sym_constraints(self, problem):
        problem.addConstraint(constraint.FunctionConstraint(horizontal_symetry(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(vertical_symetry), self.rows())
        problem.addConstraint(constraint.FunctionConstraint(diag_symetry(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(anti_diag_symetry(self.n_rows()), self.rows()))
        
        problem.addConstraint(constraint.FunctionConstraint(horizontal_symetry(self.n_cols()), self.col_vars()))
        problem.addConstraint(constraint.FunctionConstraint(vertical_symetry), self.col_vars())
        problem.addConstraint(constraint.FunctionConstraint(diag_symetry(self.n_cols()), self.col_vars()))
        problem.addConstraint(constraint.FunctionConstraint(anti_diag_symetry(self.n_cols()), self.col_vars()))
        
    def add_rotation_sym_constraints(self, problem):
        problem.addConstraint(constraint.FunctionConstraint(rotation_90(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(rotation_180(self.n_rows()), self.rows()))
        problem.addConstraint(constraint.FunctionConstraint(rotation_270(self.n_rows()), self.rows()))
        
        problem.addConstraint(constraint.FunctionConstraint(rotation_90(self.n_cols()), self.col_vars()))
        problem.addConstraint(constraint.FunctionConstraint(rotation_180(self.n_cols()), self.col_vars()))
        problem.addConstraint(constraint.FunctionConstraint(rotation_270(self.n_cols()), self.col_vars()))
           
    def sym_constraints(self, problem):
        #problem.addConstraint(constraint.FunctionConstraint(lambda x,y: x-y<0), [self.rows()[i] for i in [0,-1]])
        problem.addConstraint(constraint.MaxSumConstraint((self.n_cols()+1)/2), [self.rows()[0]])
        
        #problem.addConstraint(constraint.FunctionConstraint(lambda x,y: x-y<0), [self.col_vars()[i] for i in [0,-1]])
        problem.addConstraint(constraint.MaxSumConstraint((self.n_rows()+1)/2), [self.col_vars()[0]])
        
    def add_dual_constraints(self, problem):
        problem.addConstraint(constraint.DualConstraint(self.n_rows()), self.all_vars())

        
    def add_diag_left_constraints(self, problem):
        """add_box_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on boxes."""
        for i,j in itertools.combinations(self.rows(), 2):
            problem.addConstraint(constraint.FunctionConstraint(self.left_constraint(i,j)), [i, j])
            
        for i,j in itertools.combinations(self.col_vars(), 2):
            problem.addConstraint(constraint.FunctionConstraint(self.left_constraint(i-self.n_rows(),j-self.n_rows())), [i, j])
            
    def add_diag_right_constraints(self, problem):
        """add_box_constraints(problem, boxsize)
    
        Adds to constraint problem 'problem', all_different constraints on boxes."""
        for i,j in itertools.combinations(self.rows(), 2):
            problem.addConstraint(constraint.FunctionConstraint(self.right_constraint(i,j)), [i, j])
            
        for i,j in itertools.combinations(self.col_vars(), 2):
            problem.addConstraint(constraint.FunctionConstraint(self.right_constraint(i-self.n_rows(),j-self.n_rows())), [i, j])
    
    def rows(self): return range(1, self.n_rows() + 1)
    def cols(self): return range(1, self.n_cols() + 1)
    def col_vars(self): return range(self.n_rows()+1, self.n_rows()+self.n_cols()+1)
    def all_vars(self): return range(1, self.n_rows()+self.n_cols()+1)
    def diags_left(self): return range(2, self.n_diags_left() + 1)
    def diags_right(self): return range(1-self.n_rows(), -self.n_rows() + self.n_diags_right())
    def cell(self, row, column): return (row - 1) * self.n_rows() + column
    def symbols(self): return range(0, 1 + 1)    
    def cells(self): return range(1, self.n_cells() + 1)
   
    def n_rows(self): return self.size
    def n_cols(self): return self.size
    def n_diags_left(self): return 2*self.size
    def n_diags_right(self): return 2*self.size
    def n_cells(self): return self.n_rows()*self.n_cols()
    def n_symbols(self): return 2
    
class Graph_coloring(Problems):
        def __init__(self, edges, nb_colors, fixed={}):
            self.fixed = fixed
            self.edges = edges
            self.node_count = functools.reduce(max, map(max, edges))+1
            self.nb_colors = nb_colors
            
        def __repr__(self):
            solved = 'solved'
            if len(self.fixed) != self.node_count:
                solved = 'not solved'
            return solved + ' ' + str(self.fixed)
    
        def __str__(self):
            return self.__repr__()
    
        def get_fixed(self):
            return self.fixed
        
        def create_csp_problem(self, solver=constraint.BacktrackingSolver(), symmetry_break=False):
            p = constraint.Problem(solver)
            p.addVariables(self.nodes(), self.colors()) 
            
            self.add_edge_constraint(p)
            return p
        
        def add_edge_constraint(self, problem):
            for i,j in self.edges:
                problem.addConstraint(constraint.AllDifferentConstraint(), [i,j])
        
        def nodes(self):
            return range(0, self.node_count)
        
        def edges(self):
            return self.edges
        
        def colors(self):
            return range(self.nb_colors)