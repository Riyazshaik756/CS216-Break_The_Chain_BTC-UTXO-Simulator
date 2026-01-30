
class Transaction:
    def __init__(self, tx_id: str, inputs: list, outputs: list):
        self.tx_id = tx_id
        self.inputs = inputs      # [(tx_id, index)]
        self.outputs = outputs    # [(amount, owner)]

    def input_sum(self, utxo_manager):
        total = 0.0
        for tx_id, index in self.inputs:
            amount, _ = utxo_manager.utxo_set[(tx_id, index)]
            total += amount
        return total

    def output_sum(self):
        return sum(amount for amount, _ in self.outputs)

    def fee(self, utxo_manager):
        return self.input_sum(utxo_manager) - self.output_sum()
