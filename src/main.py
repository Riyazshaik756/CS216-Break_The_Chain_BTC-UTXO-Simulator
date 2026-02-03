import sys, os, time, random

from matplotlib.pylab import block
sys.path.append(os.path.dirname(__file__))

from utxo_manager import UTXOManager
from transaction import Transaction
from mempool import Mempool
from validator import Validator
from mining import mine_block
from Check_doubleepnd import run_double_spend_attack

def gen_tx_id():
    return f"tx_{int(time.time())}_{random.randint(1000,9999)}"


def create_genesis(utxo):
    utxo.add_utxo("genesis", 0, 50.0, "Alice")
    utxo.add_utxo("genesis", 1, 30.0, "Bob")
    utxo.add_utxo("genesis", 2, 20.0, "Charlie")
    utxo.add_utxo("genesis", 3, 10.0, "David")
    utxo.add_utxo("genesis", 4, 5.0, "Eve")

def show_utxos(utxo):
    for k, v in utxo.utxo_set.items():
        print(k, "->", v)

def main():
    utxo = UTXOManager()
    create_genesis(utxo)
    mempool = Mempool()
    validator = Validator(utxo)
    blockchain = []
    last_rejected_tx = None

    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("1. Create transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            print("\nCreating new transaction")
            sender = input("Enter sender : ")
            total_balance = utxo.get_balance(sender)

            if total_balance == 0:
                print("No funds")
                continue
            print(f"Available balance : {total_balance:.6f} BTC")

            receiver = input("Enter recipient : ")
            try:
                amount = float(input("Enter amount : "))
            except ValueError:
                print("Invalid amount! Please enter a number.")
                continue

            print("\nCreating transaction ...")
            if amount == total_balance:
                fee = 0.0
            else:
                fee = 0.001
            
            needed = amount + fee

            sender_utxos = utxo.get_utxos_for_owner(sender)
            selected_inputs = []
            total_input = 0.0

            for tx_id, index, bal in sender_utxos:
                selected_inputs.append((tx_id, index))
                total_input += bal
                if total_input >= needed:
                    break
            
            if total_input < needed:
                print(f"Insufficient total funds (including fee of {fee:.6f} BTC).")
                continue

            change = total_input - needed

            tx = Transaction(
                gen_tx_id(),
                selected_inputs,
                [(amount, receiver), (change, sender)]
            )

            ok, msg = mempool.add_transaction(tx, utxo, validator)

            if ok:
                print(f"Transaction valid ! Fee : {fee:.6f} BTC")
                print(f"Transaction ID : {tx.tx_id}")
                print("Transaction added to mempool .")
                print(f"Mempool now has {len(mempool.transactions)} transactions .")
            else:
                print("Transaction invalid :", msg)
                last_rejected_tx = {
                    "sender": sender,
                    "recipient": receiver,
                    "amount": amount,
                    "error": msg
                }
        elif choice == "2":
                show_utxos(utxo)

        elif choice == "3":
            if not mempool.transactions:
                print("\nMempool is empty.")
            else:
                print(f"\n--- Current Mempool ({len(mempool.transactions)} transactions) ---")
                for tx in mempool.transactions:
                        current_fee = tx.fee(utxo)
                        print(f"{tx.tx_id}: inputs={tx.inputs}, outputs={tx.outputs}, fee={current_fee:.4f}\n")
         


        elif choice == "4":
            miner = input("Miner name: ")

            block = mine_block(miner, mempool, utxo, blockchain)

            if block is not None:
                print("Block mined")
                print(f"Block ID: {block.block_id}")
                print(f"Transactions: {len(block.transactions)}")
            else:
                 print("No block mined.")
        
        elif choice == "5":
            print("\nSelect test scenario:")
            print("1. Invalid Signature (Optional)")
            print("2. Double-spend")
            test_choice = input("Enter choice: ")
            
            if test_choice == "2":
                print("Running test ...\n")
                run_double_spend_attack(utxo, mempool, validator,last_rejected_tx)
        elif choice == "6":
            break

if __name__ == "__main__":
    main()

