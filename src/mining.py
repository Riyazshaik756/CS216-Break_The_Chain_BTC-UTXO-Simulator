from block import Block

def mine_block(miner: str, mempool: 'Mempool', utxo_manager: 'UTXOManager', blockchain: list, num_txs=5):
    """
    Simulate mining a block.
    1. Select top transactions from mempool
    2. Update UTXO set (remove inputs, add outputs)
    3. Add miner fee as special UTXO
    4. Remove mined transactions from mempool
    """
    selected_txs = mempool.get_top_transactions(num_txs, utxo_manager)
    if not selected_txs:
        print("No transactions to mine.")
        return None
    total_fees = sum(tx.fee(utxo_manager) for tx in selected_txs)

    for tx in selected_txs:
        # Remove spent UTXOs
        for tx_id, index in tx.inputs:
            utxo_manager.remove_utxo(tx_id, index)
        # Add new UTXOs from transaction outputs
        for i, (amount, owner) in enumerate(tx.outputs):
            utxo_manager.add_utxo(tx.tx_id, i, amount, owner)

    #  Add miner fee as a unique coinbase UTXO
    block_id = blockchain[-1].block_id + 1 if blockchain else 1
    coinbase_tx_id = f"coinbase_{block_id}"
    utxo_manager.add_utxo(coinbase_tx_id, 0, total_fees, miner)

    #  Remove mined transactions from mempool
    for tx in selected_txs:
        mempool.remove_transaction(tx)

    #  Create block object
    new_block = Block(block_id, selected_txs, miner, total_fees)

    #  Append block to blockchain
    blockchain.append(new_block)

    print(f"Block {block_id} mined by {miner}, total fees: {total_fees}")
    return new_block