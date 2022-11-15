import typer


def help():
     print("This is the list of commands: bla bla")

def add_exhibit(exhibit_name: str, section_id: str):
    print("Execute add_exhibit")
    print("name of exhibit: " + exhibit_name + " section id: " + section_id)



def main(filename: str):
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
                add_exhibit(arguments[1], arguments[2])
            else:
                print(arguments[0])

                

    
if __name__ == '__main__':
    typer.run(main)
    
    
