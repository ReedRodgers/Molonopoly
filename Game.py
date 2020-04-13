import json

class Game:
    def __init__(self, file):
        self.states = []
        self.file = file

    def record(self, state):
        self.states.append(state)

    def write(self):
        self.file.write('\n'.join(self.states))
