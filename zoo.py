import typer
from typing import Optional
import numpy as np
import sys

## Helper functions:

def find_section(exhibit_name: str):
    for i in range(1,9):
        if exhibit_name in zoo[i]:
            return i   

def process_input(input):
    # Split the line into words
    arguments = input.split(" ")
    print(f"Given Arguments: {arguments}")

    if (arguments[0] == "help"):
        help()
    elif (arguments[0] == "add_exhibit"):
        # check count of arguments
        if len(arguments) == 3:
            # Try to cast argument[2] to int 
            try: 
                int(arguments[2])
            except ValueError as e:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
                return
            if (arguments[1].isalnum() and isinstance(int(arguments[2]), int)):
                add_exhibit(arguments[1], int(arguments[2]))
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        elif len(arguments) == 2:
            add_exhibit(arguments[1])
        # if more than 3 and less than 2 argument is given - print warning
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "assign_exhibit"):
        # check correct number of arguments
        if len(arguments) == 3:
            # Try to cast argument[2] to int  
            try: 
                int(arguments[2])
            except ValueError as e:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
                return
            # check if arguments are valid 
            if (arguments[1].isalnum() and isinstance(int(arguments[2]), int)):
                assign_exhibit(arguments[1], int(arguments[2]))
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "unassign_exhibit"):
        # check correct number of arguments
        if len(arguments) == 3:
            # Try to cast argument[2] to int  
            try: 
                int(arguments[2])
            except ValueError as e:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
                return
            # check if arguments are valid 
            if (arguments[1].isalnum() and isinstance(int(arguments[2]), int)):
                unassign_exhibit(arguments[1], int(arguments[2]))
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "rename_exhibit"):
        # check correct number of arguments
        if len(arguments) == 3:
            # check if arguments are valid 
            if (arguments[1].isalnum() and arguments[2].isalnum()):
                rename_exhibit(arguments[1], arguments[2])
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "move_exhibit"):
        # check correct number of arguments
        if len(arguments) == 4:
            # Try to cast argument[2] to int  
            try: 
                int(arguments[2])
                int(arguments[3])
            except ValueError as e:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
                return
            # check if arguments are valid 
            if (arguments[1].isalnum() and isinstance(int(arguments[2]), int) and isinstance(int(arguments[3]), int)):
                move_exhibit(arguments[1], int(arguments[2]), int(arguments[3]))
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "delete_exhibit"):
        # check correct number of arguments
        if len(arguments) == 3:
            # Try to cast argument[2] to int  
            try: 
                int(arguments[2])
            except ValueError as e:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
                return
            # check if arguments are valid 
            if (arguments[1].isalnum() and isinstance(int(arguments[2]), int)):
                delete_exhibit(arguments[1], int(arguments[2]))
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "add_animal"):
        # check correct number of arguments
        if len(arguments) == 3:
            # check if arguments are valid 
            if (arguments[1].isalnum() and arguments[2].isalnum()):
                add_animal(arguments[1], arguments[2])
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.") 
    elif (arguments[0] == "delete_animal"):
        # check correct number of arguments
        if len(arguments) == 3:
            # check if arguments are valid 
            if (arguments[1].isalnum() and arguments[2].isalnum()):
                delete_animal(arguments[1], arguments[2])
            else:
                print("At least one argument is invalid. Please, review the command arguments and try again.")
        else:
            print("Incorrect number of arguments for the command.")
    elif (arguments[0] == "report_zoo"):
        report_zoo()
    elif (arguments[0] == "report_unassigned_exhibits"):
        report_unassigned_exhibits()
    else:
        print("Unknown command. Please, enter help to check the available options.")


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


## Required functions:

def help():
    print("This is the list of commands: bla bla")

def add_exhibit(exhibit_name: str, section_id=None):
    if (section_id != None and section_id in [1,2,3,4,5,6,7,8,9]):
        zoo[section_id][exhibit_name] = []
        print("Exhibit " + exhibit_name + " added to section " + str(section_id))
    elif section_id == None:
        unassigned_exhibits[exhibit_name] = []
        print("Exhibition " + exhibit_name +" added to list of unassigned exhibits")

    else:
        print("Warning: Invalid section ID")

def assign_exhibit(exhibit_name: str, section_id: int):
    if section_id not in [1,2,3,4,5,6,7,8,9]:
        print("Error: Invalid section ID")
    elif len(zoo[section_id]) <= 4:
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
    if not section_id in range(1, 10): 
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
    if not current_section_id in range(1, 10): 
        print("Error: Invalid current section ID")
    elif not new_section_id in range(1, 10): 
        print("Error: Invalid new section ID")
    elif not exhibit_name in get_exhibit_names():
        print("Error:  Exhibit not found")
    elif not exhibit_name in list(zoo[current_section_id].keys()):
        print(f"Error: {exhibit_name} was not found on section {current_section_id}")
    elif len(zoo[new_section_id]) > 4:
        print("Error: The new section selected is full")
    else:
        exhibit = zoo[current_section_id].pop(exhibit_name)
        zoo[new_section_id][exhibit_name] = exhibit
        print(f"Exhibit name for {exhibit_name} moved to {new_section_id}")

def delete_exhibit(exhibit_name: str, section_id: int) -> None:
    # Description: delete an exhibit stored.
    if not section_id in range(1, 10): 
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
        if len(unassigned_exhibits[exhibit_name]) < 5:
            unassigned_exhibits[exhibit_name].append(animal_name)
            print("Animal " + animal_name + " added to unassigned exhibition " + exhibit_name)
        else:
            print("Error: The exhibit selected (" + exhibit_name + ") is full.")  
            print("Animal " + animal_name + " cannot be added") 
    elif len(zoo[section_id][exhibit_name]) < 5:
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


def main(filename: Optional[str] = typer.Argument(None)):

    # Define the dicts
    global zoo, unassigned_exhibits
    zoo = {
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {},
            9: {},
    }
    unassigned_exhibits = {}
    
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
    
    
