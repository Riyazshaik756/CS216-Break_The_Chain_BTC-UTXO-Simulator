
class Validator:
    def __init__(self, utxo_manager):
        self.utxo_manager = utxo_manager

    def validate(self, tx, mempool):
        seen_inputs = set()
        input_sum = 0.0

        # Rule 1 + 2 + 5
        for tx_id, index in tx.inputs:
            if not self.utxo_manager.exists(tx_id, index):
                return False, "UTXO does not exist"

            if (tx_id, index) in seen_inputs:
                return False, "Double-spend in same transaction"

            if (tx_id, index) in mempool.spent_utxos:
                return False, "UTXO already spent in mempool"

            seen_inputs.add((tx_id, index))
            input_sum += self.utxo_manager.utxo_set[(tx_id, index)][0]

        # Rule 4
        for amount, _ in tx.outputs:
            if amount < 0:
                return False, "Negative output amount"

        # Rule 3
        if tx.output_sum() > input_sum:
            return False, "Insufficient funds"

        return True, "Valid transaction"
