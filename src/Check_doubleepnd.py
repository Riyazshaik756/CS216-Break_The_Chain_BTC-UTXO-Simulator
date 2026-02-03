def run_double_spend_tests(utxo_manager, mempool):
    print("\n=== Running Test Scenario: Double-spend Attempt ===\n")
    
    # Keep track of which UTXOs have been used for the test
    tested_utxos = set()

    # Iterate through current mempool transactions
    for tx in mempool.transactions:
        for tx_input in tx.inputs:
            utxo_ref = (tx_input['prev_tx'], tx_input['index'])
            
            # Skip if already tested
            if utxo_ref in tested_utxos:
                continue
            
            owner = tx_input['owner']
            amount = utxo_manager.utxo_set[utxo_ref][0] if utxo_ref in utxo_manager.utxo_set else 0

            # Attempt a double-spend: spend same UTXO again
            double_tx_id = gen_tx_id()
            recipient = next(r for r in ["Alice", "Bob", "Charlie", "David", "Eve"] if r != owner)
            tx2 = Transaction(
                double_tx_id,
                [(utxo_ref[0], utxo_ref[1])],  # same UTXO
                [(min(10, amount), recipient), (amount - min(10, amount) - 0.001, owner)]
            )

            ok, msg = mempool.add_transaction(tx2, utxo_manager, validator)
            
            if not ok:  # Only print if it fails (real double-spend)
                print(f"Test : {owner} tries to spend same UTXO twice")
                print(f"Selected UTXO for double-spend: {utxo_ref[0]}:{utxo_ref[1]} ({amount:.3f} BTC)")
                print(f"TX1 : {owner} -> {tx.outputs[0]['address']} ({tx.outputs[0]['amount']:.3f} BTC) - VALID")
                print(f"TX2 : {owner} -> {recipient} ({tx2.outputs[0]['amount']:.3f} BTC) - REJECTED")
                print("Error :", msg, "\n")

            tested_utxos.add(utxo_ref)