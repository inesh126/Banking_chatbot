from tools.transaction import get_transactions


def generate_statement(month):
    txns = get_transactions(month=month)

    statement = f"Statement for month {month}:\n"

    if not txns:
        return statement + "No transactions found."

    for txn in txns:
        statement += f"{txn['date']} | {txn['description']} | {txn['amount']}\n"

    return statement
