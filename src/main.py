class UTXOManager:
    def __init__(self):
        self.utxo_set = {}

    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        key = (tx_id, index)
        value = (amount, owner)
        self.utxo_set[key] = value

    def remove_utxo(self, tx_id: str, index: int):
        self.utxo_set.pop((tx_id, index), None)

    def get_balance(self, owner: str) -> float:
        total = 0.0
        for key in self.utxo_set:
            if self.utxo_set[key][1] == owner:
                total += self.utxo_set[key][0]
        return total

    def exists(self, tx_id: str, index: int) -> bool:
        return (tx_id, index) in self.utxo_set

    def get_utxos_for_owner(self, owner: str) -> list:
        utxo_list = []
        for (tx_id, index), (amount, utxo_owner) in self.utxo_set.items():
            if utxo_owner == owner:
                utxo_list.append((tx_id, index, amount))
        return utxo_list
