
input = "3113322113"
test = "1"

def look_and_say(number):

    count = 1
    new_number = ""
    current_number = number[0]
    for c in number[1:]:
        if(c == current_number):
            count += 1
        else:
            new_number += str(count) + str(current_number)
            current_number = c
            count = 1

    new_number += str(count) + str(current_number)
    return new_number

num = input
for i in range(50):
    num = look_and_say(num)

print(len(num))
