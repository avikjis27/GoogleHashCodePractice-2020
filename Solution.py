#!/usr/bin/env python3
import sys
import os

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
        

def calculateRequiredPizzaSlice(required_pizza_slice, number_of_slices):
    last_computed_result = [{'total_slice': 0, 'ordered_pizza_types':[]}] * (required_pizza_slice + 1)
    current_computed_result = [None] * (required_pizza_slice + 1)
    
    for index, number_of_slice in enumerate(number_of_slices):
        for required_slice in range(required_pizza_slice + 1):
            if required_slice == 0:
                current_computed_result[required_slice] = {'total_slice': 0, 'ordered_pizza_types':[]} 
            elif number_of_slice > required_slice:
                current_computed_result[required_slice] = last_computed_result[required_slice]
            else:
                if last_computed_result[required_slice].get('total_slice') > number_of_slice + last_computed_result[required_slice-number_of_slice].get('total_slice') :
                    total_slice = last_computed_result[required_slice].get('total_slice') 
                    ordered_pizza_types = last_computed_result[required_slice].get('ordered_pizza_types')
                else:
                    total_slice = number_of_slice + last_computed_result[required_slice-number_of_slice].get('total_slice') 
                    ordered_pizza_types = last_computed_result[required_slice-number_of_slice].get('ordered_pizza_types') + [index]

                current_computed_result[required_slice] = {'total_slice': total_slice, 'ordered_pizza_types': ordered_pizza_types}
        last_computed_result = current_computed_result
        current_computed_result = [None] * (required_pizza_slice + 1)
    
    return last_computed_result

def generateOutput(result, max_required_slice, number_of_slices,filename):
    ordered_pizza_types = result[-1].get('ordered_pizza_types')
    first_line = len(ordered_pizza_types)
    second_line = ""
    for pizza_type in ordered_pizza_types:
        second_line = second_line + " " +str(pizza_type)
    with open(f"{filename}.out", 'w') as output_file:
         output_file.write(str(first_line)+"\n"+second_line.strip())

if __name__ == '__main__':
    max_required_slice, number_of_slices = processInput(sys.argv[1])
    filename = os.path.basename(sys.argv[1])
    result = calculateRequiredPizzaSlice(max_required_slice, number_of_slices)
    generateOutput(result, max_required_slice, number_of_slices, filename)