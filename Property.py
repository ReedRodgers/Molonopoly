from InputGenerator import rent_check


class Square:
    def __init__(self):
        self.colour = "BLACK"
        self.players_present = []

    def __repr__(self):
        return "CornerSquare"

    def __str__(self):
        return "CornerSquare"


class Property(Square):
    def __init__(self, cost: int, colour: str, rent: int, name: str, index: int):
        self.cost = int(cost)
        self.colour = colour
        self.rent = int(rent)
        self.name = name
        self.index = index
        self.owner = False
        self.players_present = []

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    def determine_rent(self, landing_player, colour_counts):
        # if the property isn't owned by anyone, there is no rent
        if not self.owner:
            return 0
        elif self.owner is landing_player:  # if property is owned by the player who lands on it, no rent.
            #  This may be pointless- this should never arise given the logic of stage2_transactions()
            #  But it's still good practice to include this check in case that logic changes
            return 0
        else:  # property is owned by the opponent
            counter = 0
            for prop in self.owner.properties:
                if prop.colour == self.colour:
                    counter += 1
            if counter == colour_counts[self.colour]:
                return self.rent * 2
            else:
                return self.rent