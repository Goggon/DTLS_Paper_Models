import os
import pathlib

def modify_variables(file_path, variable_dict: dict[str, str]):
    # open file with read write permissions
    with open(file_path, "r") as file:
        # read all lines
        lines = file.readlines()

        changed_lines = []

        # iterate over all lines
        # lines marked with MARK: are the lines one above those that a variable
        for i, line in enumerate(lines):
            # check if line contains MARK:
            if "MARK:" in line:
                # iterate over all variables
                for key, new_line in variable_dict.items():
                    # check if variable is in line
                    if key.upper() in line:
                        # save the line that will be changed
                        changed_lines.append((i+1, lines[i+1]))
                        # update variable
                        lines[i + 1] = f"{new_line}\n"
                        break
        
    with open(file_path, "w") as file:
        file.writelines(lines)

    return changed_lines

def reset_variables(file_path, changed_lines):
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line_number, line in changed_lines:
        lines[line_number] = line

    with open(file_path, "w") as file:
        file.writelines(lines)

def add_new_line_under_marks(file_path, new_lines:dict[str, str]):
    with open(file_path, "r") as file:
        lines = file.readlines()

    added_lines = []
    for i, line in enumerate(lines):
        if "MARK:" in line:
            for key, value in new_lines.items():
                if key.upper() in line:
                    lines.insert(i+1, f"{value}\n")
                    added_lines.append((i+1, value))

    with open(file_path, "w") as file:
        file.writelines(lines)

    return added_lines

def remove_changed_lines(file_path, changed_lines):
    with open(file_path, "r") as file:
        lines = file.readlines()

    for line_number, _ in changed_lines:
        # remove element line_number from lines
        lines.pop(line_number)

    with open(file_path, "w") as file:
        file.writelines(lines)

if __name__ == "__main__":
    # define variables
    variableToChange = {"psk": "bool psk[N] = {true};",
                        "requestInterval": "const int requestInterval = 40000;"}
    
    path = pathlib.Path("./Models/NoHeartbeat.xml")

    cl = modify_variables(path, variableToChange)
    print(cl)
    reset_variables(path, cl)