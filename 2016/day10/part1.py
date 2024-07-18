#!/usr/bin/python

import sys

class bot:

    def __init__(self, number):
        self.bid = number
        self.chips = []
        self.cmd_low = ("", 0)
        self.cmd_high = ("", 0)

    def get_id(self):
        return self.bid

    def give_chip(self, number):
         self.chips.append(number)
         if len(self.chips) > 2:
             print ("too many chips")

    def take_chips(self):
        tmp = self.chips
        self.chips = []
        return tmp

    def number_of_chips(self):
        return len(self.chips)

    def set_command(self, low, high):
        self.cmd_low = low
        self.cmd_high = high

    def get_high_taget(self):
        return self.cmd_high

    def get_low_taget(self):
        return self.cmd_low

    def __str__(self):
        return "Bot " + str(self.bid) + ": " + str(self.chips) + " \tlow: " + str(self.cmd_low) + " \thigh: " + str(self.cmd_high)

bots = []
outputs = []
target_bot = 0

def parse_bots(line):

    tokens = line.split()

    if tokens[0] == "bot":
        bots.append(bot(int(tokens[1])))
        bots[-1].set_command( (tokens[5], int(tokens[6])), (tokens[10], int(tokens[11])) )

def parse_value(line):

    tokens = line.split()
    if tokens[0] == "value":
        bots[int(tokens[5])].give_chip(int(tokens[1]))

def move_chip():
    global target_bot

    for bot in bots:
        if bot.number_of_chips() == 2:
            chips = sorted(bot.take_chips())
            if chips == [17, 61]:
                target_bot = bot.bid
            print(bot.get_low_taget(), bot.get_high_taget(), chips)
            if bot.get_low_taget()[0] == "bot":
                bots[bot.get_low_taget()[1]].give_chip(chips[0])
            else:
                outputs.append((bot.get_low_taget()[1], chips[0]))
            if bot.get_high_taget()[0] == "bot":
                bots[bot.get_high_taget()[1]].give_chip(chips[1])
            else:
                outputs.append((bot.get_high_taget()[1], chips[1]))
            return False

    return True


def process(input):
    global bots
    global outputs

    for line in input:
        parse_bots(line)

    bots = sorted(bots, key=lambda bot: bot.bid)

    input.seek(0)
    for line in input:
        parse_value(line)



    i = 0
    for bot in bots:
        if bot.number_of_chips() > 0:
            print(bot)
            i += 1
    print(i)

    ready = False
    while not ready:
        ready = move_chip()

    i = 0
    for bot in bots:
        if bot.number_of_chips() > 0:
            print(bot)
            i += 1
    print(i)

    outputs = sorted(outputs)
    print(outputs)

    return outputs[0][1] * outputs[1][1] * outputs[2][1]

with open("input.txt") as input:
    ret = process(input)
    print (ret)
