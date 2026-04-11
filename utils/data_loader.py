import json
from datetime import datetime

from config import SIMULATION_DATA_FILE


def load_simulation_data():
    with SIMULATION_DATA_FILE.open(encoding="utf-8") as file_obj:
        return json.load(file_obj)


def get_account_snapshot():
    data = load_simulation_data()
    return {
        "user_id": data.get("user_id"),
        "balance": data.get("balance"),
        "account": data.get("account", {}),
    }


def get_balance():
    return get_account_snapshot()["balance"]


def get_cards():
    data = load_simulation_data()
    return data.get("cards", [])


def get_beneficiaries():
    data = load_simulation_data()
    return data.get("beneficiaries", [])


def get_loans():
    data = load_simulation_data()
    return data.get("loans", [])


def get_deposits():
    data = load_simulation_data()
    return data.get("deposits", [])


def get_profile():
    data = load_simulation_data()
    return data.get("profile", {})


def get_support_tickets():
    data = load_simulation_data()
    return data.get("support", [])


def get_faq():
    data = load_simulation_data()
    return data.get("faq", {})


def get_transactions(month=None, min_amount=None, txn_type=None):
    data = load_simulation_data()
    txns = data.get("transactions", [])
    results = []

    for txn in txns:
        txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")

        if month is not None and txn_date.month != month:
            continue

        if min_amount is not None and abs(txn["amount"]) < min_amount:
            continue

        if txn_type is not None and txn["type"] != txn_type:
            continue

        results.append(txn)

    return results
