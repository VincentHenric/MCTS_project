# IASD Monte Carlo Tree Search project

This repository contains the code, experiments results and report for the MCTS course project.
The goal is to investigate the use of MCTS algorithms for constraint satisfaction problems (CSP)

## Requirements
The project make use of several Python libraries, they are all standard libraries:
- `numpy`,`scipy`: scientific computing
- `pandas`: data organisation, using dataframes
- `matplotlib`: results visualization

## Project structure and files

### Jupyter notebooks

- `results.ipynb`: do some interesting plots on the results on the simulations
- `log_analysis.ipynb`: interesting plots on the analysis of the logs

### Main code

- `constraint.py`: implementation of the CSP framework, and the solvers. Extended work from the work of WillDHB  and  scls19fr (https://github.com/python-constraint/python-constraint)
- `csp_problems.py`: implementation of the classes for the different CSP problems, in particular N-queens, graph-coloring, and sudoku
- `csp_main.py`: the main file used to launch the simulations. Tu run all the simulations, simply launch it
- `find_solutions.py`: utility file used to get the optimal number of colors for graph coloring. Used only for pre-processing, in conjunction with files from kouei (https://github.com/kouei/discrete-optimization/tree/master/coloring). To use it, the folder from kouei entitled coloring, should be placed in a folder names `solutions`.
- `generator.py`: utility file to create sudoku problems (and nqueens file with the appropriate format to be parsed)
- `parser.py`: utility file to parse problem files, and create the corresponding CSP
- `sudoku.py`: extra utility file for sudoku problems. Based on MHenderson work (https://gist.github.com/MHenderson/7639387)

### Data management

- `data/`: repository where are stored the instances of the problems. Credit to P. V. Hentenryck and C. Coffrin Coursera MOOC for the problem instances for graph-coloring (https://www.coursera.org/learn/discrete-optimization/programming/npnKe/graph-coloring)
- `images/`: images of plots used for the report
- `results/`: results of solving the different optimization problems
- `logs/`: due to file size (around 1GB), we did not upload the logs of the solving of the CSP with NMCS and NRPA. They should be located in this repository.

### Credits

- WillDHB  and  scls19fr,  “python-constraint  —  Github,”  2019. Available at https://github.com/python-constraint/python-constraint.
- P. V. Hentenryck and C. Coffrin, “Discrete optimization — Coursera.” Available at https://www.coursera.org/learn/discrete-optimization/programming/npnKe/graph-coloring.
- kouei,“discrete-optimization—Github.” Available at https://github.com/kouei/discrete-optimization/tree/master/coloring.
- MHenderson,“sudoku—Github.”Available at https://gist.github.com/MHenderson/7639387.
