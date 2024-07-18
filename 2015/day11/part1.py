
input = "vzbxkghb"
test0 = "abcdefgh"  #Result: abcdffaa
test1 = "ghijklmn"  #Result: ghjaabcc
test2 = "acdfhjka"


def new_pass(password):
    carry = 1
    new_password = ""
    for c in reversed(password):
        if (c == "z" and carry == 1):
            new_password += "a"
            carry = 1
        else:
            new_password += chr(ord(c) + carry)
            carry = 0

    return new_password[::-1]

def test_pass(password):

    ok = False
    for i,c in enumerate(password[:-2]):
        if(ord(password[i+1]) == ord(c) + 1 and ord(password[i+2]) == ord(c) + 2):
            ok = True
    if(ok == False):
        return 1

    if("i" in password or "l" in password or "o" in password):
        return 2

    pairs = 0
    skip = False
    for i,c in enumerate(password[:-1]):
        if(password[i + 1] == c and skip == False):
            pairs += 1
            skip = True
        else:
            skip = False
    if(pairs < 2):
        return 3

    return 0

password = input
i = 0
while(test_pass(password) != 0):
    password = new_pass(password)
    i += 1
    if(i == 3000):
        print(password, test_pass(password))
        i = 0

print(password, test_pass(password))
