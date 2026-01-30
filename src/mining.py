from block import Block

def mine_block(miner, mempool, utxo_manager, num_txs=5):
    selected = mempool.get_top_transactions(num_txs, utxo_manager)
    total_fees = 0.0

    for tx in selected:
        for tx_id, index in tx.inputs:
            utxo_manager.remove_utxo(tx_id, index)

        for i, (amount, owner) in enumerate(tx.outputs):
            utxo_manager.add_utxo(tx.tx_id, i, amount, owner)

        total_fees += tx.fee(utxo_manager)

    # Coinbase reward
    utxo_manager.add_utxo("coinbase", 0, total_fees, miner)

    for tx in selected:
        mempool.remove_transaction(tx)

    return Block(1, selected, miner, total_fees)
