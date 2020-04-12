# from Board import Board


class Engine:

    def __init__(self, engine):
        self.engine = engine
        self.previous = False  # Allows each player to use their own engine that references the same network
        # while passing the correct previous prediction for training

    def predict(self, players, me, board):

        self.previous = self.engine.predict(players, me, board, self.previous)

        return self.previous

    def assess(self, players, me, board):
        self.previous = self.engine.predict(players, me, board, self.previous)

        return self.previous
