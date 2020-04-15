class Logger:
    def __init__(self):
        self.per_turn_metrics = {'loss': [],
                                 'value': [],
                                 'properties': []}
        self.game_metrics = {'loss': [],
                             'assessment': [],
                             'value': []}

    def turn(self, loss, value, properties):
        self.per_turn_metrics['loss'].append(loss)
        self.per_turn_metrics['value'].append(value)
        self.per_turn_metrics['properties'].append(properties)

    def game(self, loss, value, assessment):
        self.game_metrics['loss'].append(loss)
        self.game_metrics['value'].append(value)
        self.game_metrics['assessment'].append(assessment)
