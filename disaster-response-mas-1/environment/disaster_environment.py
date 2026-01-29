import random

class DisasterEnvironment:
    def __init__(self):
        self.severity = "LOW"

    def update(self):
        self.severity = random.choice(["LOW", "MEDIUM", "HIGH"])

    def get_state(self):
        return self.severity
