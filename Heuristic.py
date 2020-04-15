from Player import Player


class Heuristic:
    def __init__(self):
        self.loss = -1

    def predict(self, me: Player, board):
        value = 0
        others_cash = 0
        opposing_rent = 0
        other_properties = 0
        for player in board.players:
            for prop in player.properties:
                other_rent = prop.determine_rent(me, board.colour_counts)
                value -= other_rent
                opposing_rent += other_rent
                value += prop.determine_rent(player, board.colour_counts)
                if player != me:
                    others_cash += player.cash
                    other_properties += 1
        if value > 0:
            return [[me.cash + others_cash * 1.0 / value]]
        if value < 0:
            return [[other_rent * 1.0 / other_properties]]
        if value == 0:
            return [[0]]

    def assess(self, player, board):
        return self.predict(player, board)

    def save(self):
        pass
