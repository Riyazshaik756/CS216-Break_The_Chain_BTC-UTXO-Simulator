
class Mempool:
    def __init__(self, max_size=50):
        self.transactions = []
        self.spent_utxos = set()
        self.max_size = max_size

    def add_transaction(self, tx, utxo_manager, validator):
        if len(self.transactions) >= self.max_size:
            return False, "Mempool full"

        valid, msg = validator.validate(tx, self)
        if not valid:
            return False, msg

        self.transactions.append(tx)
        for tx_id, index in tx.inputs:
            self.spent_utxos.add((tx_id, index))

        return True, "Transaction added to mempool"

    def remove_transaction(self, tx):
        self.transactions.remove(tx)
        for tx_id, index in tx.inputs:
            self.spent_utxos.discard((tx_id, index))

    def get_top_transactions(self, n, utxo_manager):
        return sorted(
            self.transactions,
            key=lambda tx: tx.fee(utxo_manager),
            reverse=True
        )[:n]

    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()
