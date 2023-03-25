from item import ITEM_INPUT

def dist(s, d):
    return ((s[0]-d[0]) ** 2 + (s[1]-d[1]) ** 2) ** 0.5

def is_in_set(b: int, b_set: int):
    return (b_set & (1<<b)) != 0