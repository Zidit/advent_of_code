import functools


input_file = "example2.txt"
input_file = "input.txt"

with open(input_file, "r") as file:
    data = file.readlines()

input_molecule = data.pop(-1).strip()
repl = [[v.strip() for v in x.split("=>")] for x in data if len(x) > 1]


def replace_last(mol:str):
    pos_last = 0
    repl_last = None

    for t, f in repl:
        pos = molecule.rfind(f)
        if pos >= pos_last:
            pos_last = pos
            repl_last = t, f

    if repl_last is None:
        return

    t, f = repl_last
    print(mol, pos_last)
    print(mol[:pos_last], f ,mol[pos_last + len(f):])
    print(f, "->", t)
    print()
    return mol[:pos_last] + t +  mol[pos_last + len(f):]

count = 0
molecule = input_molecule
prev_molecule = None

while molecule != 'e':
    molecule = replace_last(molecule)

    count += 1

    if molecule == prev_molecule:
        break

    prev_molecule = molecule

    print(molecule)

print(count)
