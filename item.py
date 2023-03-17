ITEM_INPUT=[
    [],
    [],
    [],
    [],
    [1,2],
    [1,3],
    [2,3],
    [4,5,6],
    [],
    []
]

ITEM_OUTPUT = [
    [1],
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [],
    []
]

ITEM_BUY = [3000, 4400, 5800, 15400, 17200, 19200, 76000]
ITEM_SELL = [6000, 7600, 9200, 22500, 25000, 27500, 10500]

class Item:
    def __init__(self, id:int):
        self.id = id
        self.buy = ITEM_BUY[id]   # not init
        self.sell = ITEM_SELL[id] # not init
