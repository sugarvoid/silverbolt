
import re


# Read the input file
with open('data/the_list.txt', 'r') as file:
    lines = file.readlines()

filtered_lines = []

for line in lines:
    _line = line.strip()
    _line = _line[:len(_line)-1]
    if len(_line) == 9 and _line.isnumeric():
        #print("true")
        filtered_lines.append(f"{_line}|{_line}@fvtc.edu\n")
    


# Process each line and filter out non-9-digit numbers
#filtered_lines = [line.strip() for line in lines if re.match(r'^\d{9}$', line.strip())]

# Format the filtered lines
#formatted_lines = [f"{line}|{line}@abcd.edu\n" for line in filtered_lines]

# Write the formatted lines to a new file
with open('clean_list.txt', 'w') as file:
    file.writelines(filtered_lines)
