class Individual:
    def __init__(self, vector):
        self.vector = vector  # z. B. Liste von Koordinaten oder Indizes
        self.fitness = None

    def evaluate(self, problem):
        self.fitness = problem.evaluate(self.vector)
