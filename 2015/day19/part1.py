
input_file = "example.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

input_molecule = data.pop(-1).strip()
repl = [[v.strip() for v in x.split("=>")] for x in data if len(x) > 1]

print(repl)
print(input_molecule)

output_molecules = set()

for i in range(len(input_molecule)):
    for r in repl:
        if r[0] in input_molecule[i:]:
            new_molecule = input_molecule[:i] + input_molecule[i:].replace(r[0], r[1], 1)
            #new_molecule = input_molecule[:i] + "," + input_molecule[i:]
            #print(input_molecule[:i], input_molecule[i:], new_molecule)
            output_molecules.add(new_molecule)


#print(output_molecules)
print(len(output_molecules))