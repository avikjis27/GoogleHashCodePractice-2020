#!/usr/bin/env python3
import sys
import os
import copy 

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

def dp_solution(max_required_slices, type_of_pizzas):
    pizza_type_map = {0: []}
    last_computed_result = [0] * (max_required_slices + 1)
    got_result = False
    for index, slices in enumerate(type_of_pizzas):
        current_computed_result = [0] * (max_required_slices + 1)
        current_map = {0: []}
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
        if got_result:
           break
    return max_possible_slices, required_pizza_types

def greedySolution(max_required_slice, number_of_slices):
    pizza_types_orderd_dsc = []
    ordered_till = 0
    for index in range(len(number_of_slices)-1, -1, -1):
        if (ordered_till + number_of_slices[index] <= max_required_slice):
            ordered_till = ordered_till + number_of_slices[index]
            pizza_types_orderd_dsc = [index] + pizza_types_orderd_dsc
        else:
            break
    return ordered_till, pizza_types_orderd_dsc


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
    ordered_using_greedy, pizza_types_orderd_greedy = greedySolution(max_required_slice, number_of_slices)
    order_remaining = max_required_slice - ordered_using_greedy
    ordered_using_dp, pizza_types_orderd_dp = dp_solution(order_remaining, number_of_slices)
    max_possible_slices = ordered_using_greedy + ordered_using_dp
    required_pizza_types = pizza_types_orderd_dp + pizza_types_orderd_greedy
    print(f"Total Ordered -> {max_possible_slices}")
    generateOutput(max_possible_slices, required_pizza_types, filename)