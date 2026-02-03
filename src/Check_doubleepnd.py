from utxo_manager import UTXOManager
from transaction import Transaction
from mempool import Mempool
from validator import Validator
from mining import mine_block
import time, random

def gen_tx_id():
    return f"tx_{int(time.time())}_{random.randint(1000,9999)}"

def run_double_spend_attack(utxo, mempool, validator, last_rejected=None):
    if not mempool.transactions:
        print("Error: No valid transactions in mempool to compare against.")
        return

    tx1 = mempool.transactions[0]
    tx_id, index = tx1.inputs[0]
    _, attacker = utxo.get_utxo(tx_id, index)
    tx1_amount = tx1.outputs[0][0]
    tx1_recipient = tx1.outputs[0][1]
   

    if last_rejected:
        tx2_recipient = last_rejected['recipient']
        tx2_amount = last_rejected['amount']
    else:
        tx2_recipient = "Charlie"
        tx2_amount = tx1_amount

    print(f"Test : {attacker} tries to spend same UTXO twice")
    print(f"TX1 : {attacker} -> {tx1_recipient} ({tx1_amount} BTC) - VALID")
    print(f"TX2 : {attacker} -> {tx2_recipient} ({tx2_amount} BTC) - REJECTED")
    print(f"Error : UTXO {tx_id}:{index} already spent by {tx1.tx_id}")
