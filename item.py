
# the input item of every workbench
ITEM_INPUT=[0, 0, 0, 0b0, 0b110, 0b1010, 0b1100, 0b1110000, 0b10000000, 0b11111110]

# the output item of every workbench
ITEM_OUTPUT = [0, 0b10, 0b100, 0b1000, 0b10000, 0b100000, 0b1000000, 0b1000000, 0, 0]

ITEM_BUY = [0, 3000, 4400, 5800, 15400, 17200, 19200, 76000]

ITEM_SELL = [0, 6000, 7600, 9200, 22500, 25000, 27500, 105000]

class Item:
    def __init__(self, id:int):
        self.id = id
        self.buy = ITEM_BUY[id]   # not init
        self.sell = ITEM_SELL[id] # not init
