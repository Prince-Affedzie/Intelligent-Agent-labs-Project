import random

class DisasterEnvironment:
    def __init__(self):
        self.disaster_type = "NONE"
        self.severity = "LOW"

    def update(self):
        disaster_types = ["FLOOD", "EARTHQUAKE", "FIRE", "LANDSLIDE"]
        severity_levels = ["LOW", "MEDIUM", "HIGH"]

        self.disaster_type = random.choice(disaster_types)
        self.severity = random.choice(severity_levels)

    def get_state(self):
        return {
            "type": self.disaster_type,
            "severity": self.severity
        }
