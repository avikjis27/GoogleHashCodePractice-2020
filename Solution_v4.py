#!/usr/bin/env python3
import sys
import numpy as np
import os
import copy 
import time
from memory_profiler import profile

def validateInput(required_pizza_slice, number_of_pizza_slices, types_of_pizza):
    isValidInput = True
    if len(number_of_pizza_slices) != types_of_pizza:
        isValidInput = False
    if required_pizza_slice > pow(10,9):
        isValidInput = False
    if types_of_pizza > pow(10,5):
        isValidInput = False
    return isValidInput


def processInput(file_name):
    input_file = open(file_name, "r")
    required_pizza_slice, types_of_pizza = input_file.readline().strip().split(" ")
    number_of_pizza_slices = input_file.readline().strip().split(" ")
    number_of_pizza_slices,  required_pizza_slice, types_of_pizza = list(map(int, number_of_pizza_slices)), int(required_pizza_slice), int(types_of_pizza)
    
    if validateInput(required_pizza_slice, number_of_pizza_slices, types_of_pizza):
        return required_pizza_slice, number_of_pizza_slices
    else:
        raise Exception('Not a valid input')

def greedySolution(max_required_slice, number_of_slices):
    pizza_types_orderd_dsc = []
    ordered_till = 0
    for index in range(len(number_of_slices)-1, -1, -1):
        if (ordered_till + number_of_slices[index] <= max_required_slice):
            ordered_till = ordered_till + number_of_slices[index]
            pizza_types_orderd_dsc = [index] + pizza_types_orderd_dsc
        else:
            break
    pizza_types_orderd_inc = []
    for index in range(len(number_of_slices)):
        if (ordered_till + number_of_slices[index] <= max_required_slice):
            ordered_till = ordered_till + number_of_slices[index]
            pizza_types_orderd_inc = pizza_types_orderd_inc + [index]
        else:
            break

    return ordered_till, pizza_types_orderd_inc + pizza_types_orderd_dsc


def generateOutput(max_required_slice, number_of_slices,filename):
    first_line = len(number_of_slices)
    second_line = ""
    for pizza_type in number_of_slices:
        second_line = second_line + " " +str(pizza_type)
    with open(f"{filename}.out", 'w') as output_file:
         output_file.write(str(first_line)+"\n"+second_line.strip())

if __name__ == '__main__':
    
    max_required_slice, number_of_slices = processInput(sys.argv[1])
    filename = os.path.basename(sys.argv[1])
    max_possible_slices, required_pizza_types = greedySolution(max_required_slice, number_of_slices)
    print(f"Total Ordered -> {max_possible_slices}")
    generateOutput(max_possible_slices, required_pizza_types, filename)