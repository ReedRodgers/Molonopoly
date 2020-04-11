from Property import Property
from EngineInterface import Engine


class Player:
    def __init__(self, cash, identifier, net: Engine):
        self.name = identifier
        self.cash = int(cash)
        self.properties = []   # Perhaps this should be a dictionary, with 4 keys corresponding to the colours
        self.position = 0
        self.network = net
        self.value = 0

    def purchase(self, some_property: Property):
        self.cash -= some_property.cost
        self.properties.append(some_property)
        some_property.owner = self

    def pay_rent(self, fee: int):
        self.cash -= int(fee)

    def valuate(self):
        # Account for cash
        net_worth = self.cash

        # Account for property value(s)
        for prop in self.properties:
            net_worth += prop.cost
        return net_worth

    def get_property_indices(self):
        if not self.properties:
            return []
        else:
            output = []
            for p in self.properties:
                output.append(int(p.index))
            return output

    def decide_purchase(self, others, prop, board):
        current = self.network.predict(others, self, board)
        self.properties.append(prop)
        self.cash -= prop.cost
        future = self.network.predict(others, self, board)
        self.properties.pop()
        self.cash += prop.cost
        if current < future:
            return True
        else:
            return False


    def __repr__(self):
        return f'{self.name}: ({self.cash}, {self.valuate()})'

    def __str__(self):
        return f'{self.name}'