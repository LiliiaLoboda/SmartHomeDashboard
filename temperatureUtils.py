import random


def increase_temperature(prev_temperature):
    return round(random.uniform(prev_temperature+0.1, prev_temperature+1), 1)


def decrease_temperature(prev_temperature):
    return round(random.uniform(prev_temperature-1, prev_temperature-0.1), 1)

