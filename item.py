
# the input item of every workbench
ITEM_INPUT=[0, 0, 0, 0, 110, 1010, 1100, 1110000, 10000000, 11111110]

# the output item of every workbench
ITEM_OUTPUT = [0, 10, 100, 1000, 10000, 100000, 1000000, 1000000, 0, 0]

ITEM_BUY = [0, 3000, 4400, 5800, 15400, 17200, 19200, 76000]

ITEM_SELL = [0, 6000, 7600, 9200, 22500, 25000, 27500, 10500]

class Item:
    def __init__(self, id:int):
        self.id = id
        self.buy = ITEM_BUY[id]   # not init
        self.sell = ITEM_SELL[id] # not init
