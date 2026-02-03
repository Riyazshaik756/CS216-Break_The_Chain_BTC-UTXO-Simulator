
class UTXOManager:
    def __init__(self):
        self.utxo_set = {}

    def add_utxo(self, tx_id: str, index: int, amount: float, owner: str):
        key = (tx_id, index)
        value = (amount, owner)
        self.utxo_set[key] = value

    def remove_utxo(self, tx_id: str, index: int):
            if (tx_id, index) not in self.utxo_set:
                raise ValueError(f"UTXO not found: tx_id={tx_id}, index={index}")
            del self.utxo_set[(tx_id, index)]

    def get_balance(self, owner: str) -> float:
        return sum(
            amount
            for (amount, utxo_owner) in self.utxo_set.values()
            if utxo_owner == owner
    )

    def exists(self, tx_id: str, index: int) -> bool:
        return (tx_id, index) in self.utxo_set

    def get_utxo(self, tx_id: str, index: int):
        if (tx_id, index) not in self.utxo_set:
            raise ValueError(f"UTXO not found: tx_id={tx_id}, index={index}")
        return self.utxo_set[(tx_id, index)]
    
    def get_utxos_for_owner(self, owner: str):
        return [
            (tx_id, index, amount)
            for (tx_id, index), (amount, utxo_owner) in self.utxo_set.items()
            if utxo_owner == owner
        ]