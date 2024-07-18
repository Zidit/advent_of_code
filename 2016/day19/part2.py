

elf_count = 5
elf_count = 3014387

elfs = [i + 1 for i in range(elf_count)]

current = 0
while len(elfs) > 2:
    middle = (len(elfs) // 2 + current) % len(elfs)
    #print(current, middle) 
    del elfs[middle]

    current += 1
    #if len(elfs) > 1:
    #    current %= len(elfs) -1
    #print(elfs)

    if len(elfs) % 1000 == 0:
        print(".", end="", flush=True)


print(elfs, current, (current +1)%2)
print(elfs[(current +1)%2])


