#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:48:07 2020

@author: henric
"""
import csp_problems
import sudoku
import os

def generate_sudokus(n, percent=0.33, boxsize=3, erase=False):
    path = 'data/sudoku/data'
    filenames = os.listdir(path)
    start_n=0
    if filenames and not erase:
        start_n = max(int(filename.split('_')[-1]) for filename in filenames if filename.split('_')[0]==str(boxsize))+1
    
    for i in range(start_n, start_n+n):
        fixed = generate_sudoku(percent, boxsize)
        with open(os.path.join(path,'{}_{}'.format(boxsize, i)), 'w') as file:
            file.write('{}\n{}'.format(boxsize, fixed))

def generate_sudoku(percent=0.33, boxsize=3):
    n_fixed = int(round(boxsize**4 * percent,0))
    fixed = sudoku.random_fixed(n_fixed, boxsize, model='CP')
    return fixed
        
def generate_nqueens(n_list):
    path = 'data/nqueens/data'
    for n in n_list:
        with open(os.path.join(path,'{}_{}'.format('nqueens', n)), 'w') as file:
            file.write('{}'.format(n))

if __name__ == '__main__':
    if False:
        generate_sudokus(10, erase=False)
        generate_sudokus(10, boxsize=4, erase=False)
        generate_sudokus(10, boxsize=5, erase=False)
        
    if True:
        generate_nqueens([8,16,32,64,96,128,192,256])