import typer
import numpy as np

## Helper functions:

def find_section(exhibit_name: str):
    for i in range(1,9):
        if exhibit_name in zoo[i]:
            return i   


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
            print("Exhibit name: " + exhibit_name + " not found in the list if unassigned exhibits")   
    else:
        print("Error: The section selected is full")

def add_animal(animal_name: str, exhibit_name: str):
    section_id = find_section(exhibit_name)
    if section_id == None:
        print("Exhibit name: " + exhibit_name + " not found in assigned exhibits")
    elif len(zoo[section_id][exhibit_name]) < 5:
        zoo[section_id][exhibit_name].append(animal_name)
        print("Animal " + animal_name + " added to exhibition " + exhibit_name)
    else:
        print("Error: The exhibit selected (" + exhibit_name + ") is full.")  
        print("Animal " + animal_name + " cannot be added") 

def report_zoo():
    print("Current report of zoo: ")
    print(zoo)


def main(filename: str):

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

    with open(str(filename + ".txt")) as file:

        # Process each line after the other of the document
        while (line := file.readline().rstrip()):

            # Convert the characters in line to lowercase to avoid case mismatch
            line = line.lower()

            # Split the line into words
            arguments = line.split(" ")

            if (arguments[0] == "help"):
                help()
            elif (arguments[0] == "add_exhibit"):
                #add_exhibit(exhibit_name: str, section_id=None)
                if len(arguments) > 2:
                    add_exhibit(arguments[1], int(arguments[2]))
                else:
                    add_exhibit(arguments[1])
            elif (arguments[0] == "assign_exhibit"):
                #assign_exhibit(exhibit_name: str, section_id: int)
                assign_exhibit(arguments[1], int(arguments[2]))
            elif (arguments[0] == "add_animal"):
                #add_animal(animal_name: str, exhibit_name: str)
                add_animal(arguments[1], arguments[2])
            elif (arguments[0] == "report_zoo"):
                report_zoo()
            else:
                print(arguments[0])

                

    
if __name__ == '__main__':
    typer.run(main)
    
    
