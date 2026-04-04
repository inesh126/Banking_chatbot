from datetime import datetime

from utils.data_loader import load_simulation_data


def get_transactions(month=None, min_amount=None, txn_type=None):
    data = load_simulation_data()
    txns = data["transactions"]

    results = []

    for txn in txns:
        txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")

        if month:
            if txn_date.month != month:
                continue

        if min_amount:
            if abs(txn["amount"]) < min_amount:
                continue

        if txn_type:
            if txn["type"] != txn_type:
                continue

        results.append(txn)

    return results
