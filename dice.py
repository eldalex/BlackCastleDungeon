import random


def roll_the_dice(count):
    dice1 = random.randrange(1, 7)
    dice2 = random.randrange(1, 7)
    if count == 1:
        return dice1
    if count == 2:
        return dice1, dice2
