import json

from config import SIMULATION_DATA_FILE


def load_simulation_data():
    with SIMULATION_DATA_FILE.open(encoding="utf-8") as file_obj:
        return json.load(file_obj)
