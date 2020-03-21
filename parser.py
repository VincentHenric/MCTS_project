#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 18:35:11 2020

@author: henric
"""
import csp_problems



def parse_coloring(filename):
    def get_data(filename):
        with open('data/coloring/data/{}'.format(filename), 'r') as input_data_file:
            input_data = input_data_file.read()
                
        lines = input_data.split('\n')
    
        first_line = lines[0].split()
        node_count = int(first_line[0])
        edge_count = int(first_line[1])
        nb_colors = int(filename.split('_')[-1])
    
        edges = []
        for i in range(1, edge_count + 1):
            line = lines[i]
            parts = line.split()
            edges.append((int(parts[0]), int(parts[1])))
        return node_count, edge_count, edges, nb_colors
    
    node_count, edge_count, edges, nb_colors = get_data(filename)
    
    return csp_problems.Graph_coloring(edges, nb_colors)
    
def parse_sudoku(filename):
    def get_data(filename):
        with open('data/sudoku/data/{}'.format(filename), 'r') as input_data_file:
            input_data = input_data_file.read()
                
        lines = input_data.split('\n')
    
        boxsize = int(lines[0])
        fixed = eval(lines[1])
    
        return boxsize, fixed
    
    boxsize, fixed = get_data(filename)
    
    return csp_problems.Sudoku_problem(fixed, boxsize)

def parse_nqueens(filename):
    def get_data(filename):
        with open('data/nqueens/data/{}'.format(filename), 'r') as input_data_file:
            input_data = input_data_file.read()
                
        lines = input_data.split('\n')
    
        n = int(lines[0])
    
        return n
    
    n = get_data(filename)
    
    return csp_problems.NQueens_2(n)

PARSE = {
        'coloring': parse_coloring,
        'sudoku': parse_sudoku,
        'nqueens': parse_nqueens
        }

if __name__ == '__main__':
    if False:
        print(parse_sudoku('3_0'))
        
    if True:
        print(parse_nqueens('nqueens_8'))