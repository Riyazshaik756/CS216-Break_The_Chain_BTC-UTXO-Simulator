
class Block:
    def __init__(self, block_id, transactions, miner, total_fees):
        self.block_id = block_id
        self.transactions = transactions
        self.miner = miner
        self.total_fees = total_fees
