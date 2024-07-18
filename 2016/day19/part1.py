

elf_count = 5
elf_count = 3014387

elfs = [i + 1 for i in range(elf_count)]

while len(elfs) > 1:
    is_even = len(elfs) % 2 == 0
    elfs = elfs[::2]
    if not is_even:
        elfs = elfs[1:]

print()
print(elfs[0])


