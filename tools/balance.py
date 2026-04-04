from utils.data_loader import load_simulation_data

def get_balance():
    data = load_simulation_data()
    return data["balance"]
