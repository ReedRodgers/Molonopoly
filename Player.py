from Property import Property
from EngineInterface import Engine
from Logger import Logger


class Player:
    def __init__(self, cash, identifier, net: Engine, logger: Logger):
        self.name = identifier
        self.cash = int(cash)
        self.properties = []   # Perhaps this should be a dictionary, with 4 keys corresponding to the colours
        self.position = -1
        self.network = net
        self.value = cash
        self.logger = logger

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
        if self.cash < 0:
            print('op')
        future = self.network.predict(self, board)
        board.move_property(prop, self, 0)  # Undo property buy
        board.deposit(prop.cost, self)
        loss = self.network.loss
        if current <= future:
            self.logger.turn(loss, future[0][0], len(self.properties) + 1)
            return True
        self.logger.turn(loss, current[0][0], len(self.properties))
        return False

    def final_training(self, board, turns):
        self.value = self.cash / turns
        assessment = self.network.assess(self, board)[0][0]
        self.logger.game(self.network.loss, self.value, assessment)

    def __repr__(self):
        return f'{self.name}: ({self.cash}, {self.valuate()})'

    def __str__(self):
        return f'{self.name}'
