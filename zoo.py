from typing import Optional
import numpy as np
import typer
import json
import os

# ----- Constants -----
arg_parser = None
zoo = None 
unassigned_exhibits = None
MAX_ANIMAL_PER_EXHIBIT = 5
MAX_EXHIBITS_PER_SECTION = 4
SECTION_NAMES = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ----- Helper functions -----
def find_section(exhibit_name: str):
    for n in SECTION_NAMES:
        if exhibit_name in zoo[n]:
            return n 

def get_exhibit_names() -> list:
    assigned_names = [n for s in zoo.keys() for n in list(zoo[s].keys())]
    unassigned_names =  list(unassigned_exhibits.keys())
    return assigned_names + unassigned_names

def get_assigned_animals() -> list:
    assigned_animals = [a for s in zoo.keys() for n in zoo[s].keys() for a in zoo[s][n]]
    return assigned_animals

def get_unassigned_animals() -> list:
    unassigned_animals = [a for s in unassigned_exhibits.keys() for a in unassigned_exhibits[s]]
    return unassigned_animals

def args_are_valid(function_args: list) -> bool:
    function_name = function_args[0]
    if not len(function_args) in arg_parser[function_name][0]: # check argument number
        print("Incorrect number of arguments for the command.")
        return False
    for i in range(1, len(function_args)):
        expected_type = arg_parser[function_name][1][i-1]
        try:
            expected_type(function_args[i]) # check the arg cast
        except ValueError as e:
            print("At least one argument is invalid. Please, review the command arguments and try again.")
            return False
        if expected_type == str and not function_args[i].replace("_", "").isalnum(): # check if str args are alphanumeric ('_' allowed)
            print("Command name is not valid. Please, review the command name and try again.")
            return False
    return True

def convert_args(function_args: list) -> list: # convert args into the required format
    function_name = function_args[0]
    converted_args = []
    for i in range(1, len(function_args)):
        expected_output = arg_parser[function_name][1][i-1]
        converted_args.append(expected_output(function_args[i]))
    return converted_args

def process_input(input):
    # Split the line into words
    arguments = input.split(" ")
    print(f"Given Arguments: {arguments}")

    if arguments[0] in arg_parser.keys():
        launch_func = arg_parser[arguments[0]][2]
        if args_are_valid(arguments):
            launch_func(*convert_args(arguments))
    else:
        print("Unknown command. Please, enter help to check the available options.")

def save_json_file(filename: str, d: dict) -> None:
    try:
        f = open(f"{filename}.json", 'w')
        json.dump(d, f, indent=4)
    except:
        print("Warning: An error occurred while saving the zoo")

def load_zoo_from_json(filename: str) -> dict:
    try:
        with open(f"{filename}.json") as json_file:
            d = json.load(json_file)
            return d
    except:
        print("Warning: There was an error loading the zoo")
    

def zoo_structure_is_valid(input_zoo: dict) -> bool:
    if len(input_zoo.keys()) != 9: # 9 sections
        return False
    for section_id, exhibits in input_zoo.items():
        if not int(section_id) in SECTION_NAMES: # same section names
            return False
        if len(exhibits) > MAX_EXHIBITS_PER_SECTION: # more than 4 exhibits
            return False
        for exhibit_id, animals in exhibits.items():
            if not exhibit_id.replace("_", "").isalnum():
                return False
            if len(animals) > MAX_ANIMAL_PER_EXHIBIT:
                return False
    return True

# ----- Required functions -----
def help():
    print("This is the list of commands: bla bla")

def add_exhibit(exhibit_name: str, section_id=None):
    if (section_id != None and section_id in SECTION_NAMES):
        zoo[section_id][exhibit_name] = []
        print("Exhibit " + exhibit_name + " added to section " + str(section_id))
    elif section_id == None:
        unassigned_exhibits[exhibit_name] = []
        print("Exhibition " + exhibit_name +" added to list of unassigned exhibits")

    else:
        print("Warning: Invalid section ID")

def assign_exhibit(exhibit_name: str, section_id: int):
    if section_id not in SECTION_NAMES:
        print("Error: Invalid section ID")
    elif len(zoo[section_id]) <= MAX_EXHIBITS_PER_SECTION:
        try:
            zoo[section_id][exhibit_name] = unassigned_exhibits[exhibit_name]
            del unassigned_exhibits[exhibit_name]
            print("Exhibit " + exhibit_name + " added to section " + str(section_id))
        except Exception as e:
            print("Exhibit name: " + exhibit_name + " not found in the list of unassigned exhibits")   
    else:
        print("Error: The section selected is full")

def unassign_exhibit(exhibit_name: str, section_id: int) -> None:
    # Description: unassign an exhibit to a section. Both arguments are mandatory.
    if not section_id in SECTION_NAMES: 
        print("Error: Invalid section ID")
    elif not exhibit_name in get_exhibit_names():
        print("Error:  Exhibit not found")
    elif not exhibit_name in list(zoo[section_id].keys()):
        print(f"Error: {exhibit_name} was not found on section {section_id}")
    else:
        exhibit = zoo[section_id].pop(exhibit_name)
        unassigned_exhibits[exhibit_name] = exhibit 
        print(f"Exhibit {exhibit_name} unassigned from section {section_id}")

def rename_exhibit(exhibit_name: str, new_exhibit_name: str) -> None:
    # Description: rename an exhibit stored.
    if not exhibit_name in get_exhibit_names():
        print("Error:  Exhibit not found")
        return None
    elif exhibit_name == new_exhibit_name:
        print("Error: The new name is the same as the old name")
        return None
    elif exhibit_name in unassigned_exhibits.keys():
        exhibit = unassigned_exhibits.pop(exhibit_name)
        unassigned_exhibits[new_exhibit_name] = exhibit
    else:
        for s, ex in zoo.items():
            if exhibit_name in ex.keys():
                exhibit = zoo[s].pop(exhibit_name)
                zoo[s][new_exhibit_name] = exhibit
    print(f"Exhibit name for {exhibit_name} changed to {new_exhibit_name}.")

def move_exhibit(exhibit_name: str, current_section_id: int, new_section_id: int) -> None:
    # Description: move an exhibit to another section.
    if not current_section_id in SECTION_NAMES: 
        print("Error: Invalid current section ID")
    elif not new_section_id in SECTION_NAMES: 
        print("Error: Invalid new section ID")
    elif not exhibit_name in get_exhibit_names():
        print("Error:  Exhibit not found")
    elif not exhibit_name in list(zoo[current_section_id].keys()):
        print(f"Error: {exhibit_name} was not found on section {current_section_id}")
    elif len(zoo[new_section_id]) > MAX_EXHIBITS_PER_SECTION:
        print("Error: The new section selected is full")
    else:
        exhibit = zoo[current_section_id].pop(exhibit_name)
        zoo[new_section_id][exhibit_name] = exhibit
        print(f"Exhibit name for {exhibit_name} moved to {new_section_id}")

def delete_exhibit(exhibit_name: str, section_id: int) -> None:
    # Description: delete an exhibit stored.
    if not section_id in SECTION_NAMES: 
        print("Error: Invalid section ID")
    elif not exhibit_name in get_exhibit_names():
        print("Error:  Exhibit not found")
    elif not exhibit_name in list(zoo[section_id].keys()):
        print(f"Error: {exhibit_name} was not found on section {section_id}")
    else:
        zoo[section_id].pop(exhibit_name)
        print(f"Exhibit {exhibit_name} was deleted")

def add_animal(animal_name: str, exhibit_name: str):
    section_id = find_section(exhibit_name)
    if section_id == None:
        print("Exhibit name: " + exhibit_name + " not found in assigned exhibits")
        if len(unassigned_exhibits[exhibit_name]) < MAX_ANIMAL_PER_EXHIBIT:
            unassigned_exhibits[exhibit_name].append(animal_name)
            print("Animal " + animal_name + " added to unassigned exhibition " + exhibit_name)
        else:
            print("Error: The exhibit selected (" + exhibit_name + ") is full.")  
            print("Animal " + animal_name + " cannot be added") 
    elif len(zoo[section_id][exhibit_name]) < MAX_ANIMAL_PER_EXHIBIT:
        zoo[section_id][exhibit_name].append(animal_name)
        print("Animal " + animal_name + " added to exhibition " + exhibit_name)
    else:
        print("Error: The exhibit selected (" + exhibit_name + ") is full.")  
        print("Animal " + animal_name + " cannot be added") 

def delete_animal(animal_name: str, exhibit_name: str):
    # check if exhibit exits
    if not exhibit_name in get_exhibit_names():
        print("Error:  Exhibit not found")
    # check if animal exists 
    elif animal_name not in get_assigned_animals() and animal_name not in get_unassigned_animals():
        print("Error: Animal " + animal_name + " not found")
    else:
        # get section_id of exibit if possible
        section_id = find_section(exhibit_name)
        # if no section_id exists, exhibit is unassigned
        if section_id == None:
            print("Animal: " + animal_name + " not found in assigned exhibits")
            # check if animal exists in given exhibit
            if animal_name in get_unassigned_animals():
                unassigned_exhibits[exhibit_name].remove(animal_name)
                print(f"{animal_name} was removed from unassigned exhibit {exhibit_name}")
            else:
                print(f"Error: {animal_name} was not found in unassigned exhibit {exhibit_name}")
        # section_id exists
        else:
            # check if animal exists in given exhibit
            if animal_name in get_assigned_animals():
                zoo[section_id][exhibit_name].remove(animal_name)
                print(f"{animal_name} was removed from assigned exhibit {exhibit_name}")
            else:
                print(f"Error: {animal_name} was not found in assigned exhibit {exhibit_name}")

def report_zoo():
    print("Current report of zoo: ")
    print(zoo)

def report_unassigned_exhibits():
    print("List of unassigned exhibits:")
    print(unassigned_exhibits)

def save_zoo(zoo_name: str = "new_zoo") -> None:
    if f"{zoo_name}.json" in os.listdir():
        savefile_in = ""
        while not savefile_in in ["y", "n", "Y", "N"]:
            savefile_in = input(f"The zoo '{zoo_name}' already exists. Do you want to overwrite it? y/n:")
        if savefile_in in ["y", "Y"]:
            save_json_file(zoo_name, zoo)
            print(f"Zoo '{zoo_name}' saved")
        else:
            print(f"Zoo '{zoo_name}' not saved")
    else:
        save_json_file(zoo_name, zoo)
        print(f"Zoo '{zoo_name}' saved")

def load_zoo(zoo_name: str) -> None:
    global zoo
    if not f"{zoo_name}.json" in os.listdir():
        print("Warning: The file was not found")
    else:
        loaded_zoo = load_zoo_from_json(zoo_name)
        if loaded_zoo:
            if zoo_structure_is_valid(loaded_zoo):
                zoo = loaded_zoo
            else:
                print("Warning: The file does not have valid zoo information")

# ----- Main -----
def main(filename: Optional[str] = typer.Argument(None)):

    # Define the dicts
    global zoo, unassigned_exhibits, arg_parser
    zoo = {}
    for s in SECTION_NAMES:
        zoo.update({s:{}})
    unassigned_exhibits = {}
    arg_parser = {  # funct_name: ([allowed_lens], [allowed_formats], launch_function)
        "help" : ([1], [], help),
        "add_exhibit" : ([2,3], [str, int], add_exhibit),
        "assign_exhibit" : ([3], [str, int], assign_exhibit),
        "unassign_exhibit" : ([3], [str, int], unassign_exhibit),
        "rename_exhibit" : ([3], [str, str], rename_exhibit),
        "move_exhibit" : ([4], [str, int, int], move_exhibit),
        "delete_exhibit" : ([3], [str, int], delete_exhibit),
        "add_animal" : ([3], [str, str], add_animal),
        "delete_animal" : ([3], [str, str], delete_animal),
        "report_zoo" : ([1], [], report_zoo),
        "report_unassigned_exhibits" : ([1], [], report_unassigned_exhibits),
        "save_zoo" : ([1,2], [str], save_zoo),
        "load_zoo" : ([2], [str], load_zoo)
    }
    
    if filename:
        with open(str(filename + ".txt")) as file:

            # Process each line after the other of the document
            while (line := file.readline().rstrip()):

                # Convert the characters in line to lowercase to avoid case mismatch
                line = line.lower()

                process_input(line)         
    else:
        while True:
            inp = input("Write commands (command argument_1 argument_2) [to exit type 'quit']: ")
            if inp == "quit":
                break
            process_input(inp)               
    
if __name__ == '__main__':
    typer.run(main)
    
    
