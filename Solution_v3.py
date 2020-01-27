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
        

def solve_using_greedy(max_required_slices, type_of_pizzas, greedy_percent=0):
    total_slices = 0
    greedy_index = -1
    for index, slices in enumerate(type_of_pizzas):
        total_slices = total_slices + slices
        if(total_slices >= max_required_slices * greedy_percent):
            print("total_slices",total_slices,"Percent",max_required_slices * greedy_percent)
            greedy_index = index
            break
    print(f"Greedy portion: greedy_index={greedy_index}, total_slices={total_slices}")
    return greedy_index, total_slices


#@profile
def solve_dynamic_programing(max_required_slices, type_of_pizzas, greedy_index):
    print(f"Size of dynamic programin is: {len(type_of_pizzas) - (greedy_index+1)} X {max_required_slices}")
    pizza_type_map = {0: []}
    last_computed_result = [0] * (max_required_slices + 1)
    got_result = False

    for index, slices in enumerate(type_of_pizzas):
        if index <= greedy_index:
            continue
        current_computed_result = [0] * (max_required_slices + 1)
        current_map = {0: []}
        start_a_type = time.time()
        for required_slices in range(max_required_slices + 1):
            if required_slices == 0 :
                current_computed_result[required_slices] = 0
                current_map[required_slices] = []
            elif slices > required_slices:
                current_computed_result[required_slices] = last_computed_result[required_slices]
                current_map[required_slices] = pizza_type_map.get(required_slices, [])
            else:
                if last_computed_result[required_slices] > slices + last_computed_result[required_slices-slices]:
                    current_computed_result[required_slices] = last_computed_result[required_slices]
                    current_map[required_slices] = pizza_type_map.get(required_slices, [])
                else:
                    current_computed_result[required_slices] = slices + last_computed_result[required_slices-slices]
                    current_map[required_slices] = pizza_type_map.get(required_slices-slices, []) + [index]
                    if current_computed_result[required_slices] == max_required_slices:
                        got_result = True
                        break
        last_computed_result = copy.copy(current_computed_result)
        pizza_type_map = copy.copy(current_map)
        max_possible_slices = last_computed_result[-1]
        required_pizza_types = pizza_type_map.get(max_possible_slices, [])
        stop_a_type = time.time()
        print(f"time taken for {index} = {stop_a_type - start_a_type}")
        if got_result:
           break
    return max_possible_slices, required_pizza_types



def generateOutput(max_required_slice, number_of_slices,filename):
    first_line = len(number_of_slices)
    second_line = ""
    for pizza_type in number_of_slices:
        second_line = second_line + " " +str(pizza_type)
    with open(f"{filename}.out", 'w') as output_file:
         output_file.write(str(first_line)+"\n"+second_line.strip())

if __name__ == '__main__':
    inverted = False
    max_required_slice, number_of_slices = processInput(sys.argv[1])
    greedy_percent = float(sys.argv[2])
    filename = os.path.basename(sys.argv[1])
    total_slices_if_consider_all_types = np.sum(number_of_slices)
    extra_slice_if_ordered_all_types = total_slices_if_consider_all_types - max_required_slice
    
    if (extra_slice_if_ordered_all_types > max_required_slice):
        inverted = True
        greedy_index, total_slices = solve_using_greedy(extra_slice_if_ordered_all_types, number_of_slices, greedy_percent)
        max_possible_slices, not_required_pizza_types = solve_dynamic_programing(extra_slice_if_ordered_all_types - total_slices, number_of_slices, greedy_index)
        required_pizza_types = set(range(len(number_of_slices))) - set(not_required_pizza_types)

    else:
        greedy_index, total_slices = solve_using_greedy(max_required_slice, number_of_slices, greedy_percent)
        max_possible_slices, required_pizza_types = solve_dynamic_programing(max_required_slice - total_slices, number_of_slices, greedy_index)
    
    print("inverted->", inverted)
    generateOutput(max_possible_slices, required_pizza_types, filename)