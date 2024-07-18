
input_file = "example.txt"
#input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

floors = [f.split() for f in data]
print(floors)