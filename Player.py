from Property import Property
from EngineInterface import Engine


class Player:
    def __init__(self, cash, identifier, net: Engine):
        self.name = identifier
        self.cash = int(cash)
        self.properties = []   # Perhaps this should be a dictionary, with 4 keys corresponding to the colours
        self.position = -1
        self.network = net
        self.value = 0.0

    def purchase(self, some_property: Property):
        self.cash -= some_property.cost
        self.properties.append(some_property)
        some_property.owner = self

    def pay_rent(self, prop: Property, colour_counts):
        fee = prop.determine_rent(self, colour_counts)
        self.cash -= fee
        prop.owner.cash += fee

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
        return [p.index for p in self.properties]

    def decide_purchase(self, prop, board):
        current = self.network.assess(self, board)
        board.move_property(prop, self, 1)  # Simulate property buy
        board.deposit(0-prop.cost, self)
        future = self.network.predict(self, board)
        board.move_property(prop, self, 0)  # Undo property buy
        board.deposit(prop.cost, self)
        return current <= future

    def final_training(self, board, turns):
        self.value = self.cash / turns
        self.network.assess(self, board)
        self.network.save()

    def __repr__(self):
        return f'{self.name}: ({self.cash}, {self.valuate()})'

    def __str__(self):
        return f'{self.name}'