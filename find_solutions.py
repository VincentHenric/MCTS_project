#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 19:21:54 2020

@author: henric
"""
import subprocess
import os
import time

class Problem:
    @staticmethod
    def take_file():
        pass
    
    def solve_instance():
        pass
    
    def solve_all():
        pass
    
    def change_name():
        pass

class Coloring:
    path_1 = './solutions/coloring'
    path_2 = 'data/coloring'
    
    @staticmethod
    def solve_instance(filename):
        os.system("{}/main {}/data/{} > {}/solution/{}".format(Coloring.path_1, Coloring.path_1, filename, Coloring.path_2, filename))
        
#    @staticmethod
#    def change_name(filename):
#        with open("{}/cpp_output.txt".format(Coloring.path_1)) as file:
#            input_data = file.read()
#        lines = input_data.split('\n')
#        obj = lines[0].split(' ')[0]
#        new_filename = filename + '_' + obj
#        #print('{}/{}'.format(Coloring.path_2, filename))
#        #print('{}/{}'.format(Coloring.path_2, new_filename))
#        try:
#            os.rename('{}/data/{}'.format(Coloring.path_2, filename), '{}/data/{}'.format(Coloring.path_2, new_filename))
#            print('{} renamed as {}'.format(filename, new_filename))
#        except:
#            print('{} not renamed'.format(filename))
      
    @staticmethod
    def change_name(filename, relaunch=False):
        try:
            renamed_filenames = [file for file in os.listdir('{}/data/'.format(Coloring.path_2)) if file.startswith(filename + '_')]
            if len(renamed_filenames)==0 or relaunch:
                with open("{}/solution/{}".format(Coloring.path_2, filename)) as file:
                    input_data = file.read()
                lines = input_data.split('\n')
                obj = lines[-3].split(' ')[0]
                if len(renamed_filenames)==1:
                    filename = renamed_filenames[0]
                    new_filename = '_'.join(filename.split('_')[:-1]) + '_' + obj
                elif len(renamed_filenames)==0:
                    new_filename = filename + '_' + obj
                else:
                    raise ValueError()
            
                os.rename('{}/data/{}'.format(Coloring.path_2, filename), '{}/data/{}'.format(Coloring.path_2, new_filename))
                print('{} renamed as {}'.format(filename, new_filename))
            else:
                print('{} already renamed'.format(filename))
        except:
            print('{} not renamed'.format(filename))
        
    @staticmethod
    def rename_all(relaunch=False):
        filenames = os.listdir('{}/data/'.format(Coloring.path_1))
        for filename in filenames:
            Coloring.change_name(filename, relaunch)
        
    @staticmethod
    def process_file(filename):
        try:
            Coloring.solve_instance(filename)
            print("{} solved".format(filename))
            #time.sleep(0.5)
            #Coloring.change_name(filename)
        except:
            print("{} could not be solved".format(filename))
            
    @staticmethod
    def process_all():
        filenames = os.listdir('{}/data/'.format(Coloring.path_1))
        for filename in filenames:
            Coloring.process_file(filename)
            
            
if __name__=='__main__':
    if False:
        Coloring.process_all()
        
    if False:
        Coloring.rename_all(relaunch=False)