import random

def Dice(begin: int, end: int) -> int:
    return random.randint(begin, end)

def DiceFloat(begin: float, end: float) -> float:
    return random.uniform(begin, end)

def DiceElem(inlist: list) -> list:
    newList = inlist.copy()
    random.shuffle(newList)
    return newList

def DiceElemChoice(anyContainer):
    return random.choice(anyContainer)

def DiceExclude(begin: int, end: int, excludes: list[int]):
    numbers = [n for n in range(begin, end+1) if not n in excludes]
    return DiceElemChoice(numbers)