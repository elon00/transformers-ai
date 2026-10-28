# -*- coding: utf-8 -*-
import hashlib
import time
import json

class TransformersMorphicAgent:
    def __init__(self, commander: str = "Optimus Prime", faction: str = "Autobots"):
        self.commander = commander
        self.faction = faction
        self.matrix_of_leadership_held = True

    def transform_and_roll_out(self, destination: str, payload_units: int) -> dict:
        if not isinstance(destination, str) or not destination.strip() or len(destination.strip()) > 256 or not destination.isprintable():
            raise ValueError("destination must be 1-256 printable characters")
        if type(payload_units) is not int or not 1 <= payload_units <= 1_000_000:
            raise ValueError("payload_units must be an integer from 1 to 1000000")
        destination = destination.strip()
        dispatch_hash = hashlib.sha256(f"{self.commander}:{destination}:{payload_units}:{time.time()}".encode()).hexdigest()
        return {
            "commander": self.commander,
            "faction": self.faction,
            "morphic_transition": "ROBOT_TO_TRUCK_CONVOY",
            "destination": destination,
            "energon_consumed": payload_units * 0.45,
            "matrix_of_leadership_verified": self.matrix_of_leadership_held,
            "allspark_hash": f"0x{dispatch_hash[:32]}",
            "directive": "Freedom is the right of all sentient beings",
            "timestamp": int(time.time())
        }

if __name__ == "__main__":
    agent = TransformersMorphicAgent()
    res = agent.transform_and_roll_out("Earth Orbital Relay Station", 500)
    print("Morphic Compute Telemetry:", json.dumps(res, indent=2))
