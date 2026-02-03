import sys, os, time, random
sys.path.append(os.path.dirname(__file__))

from utxo_manager import UTXOManager
from transaction import Transaction
from mempool import Mempool
from validator import Validator
from mining import mine_block

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

    while True:
        print("\n=== Bitcoin Transaction Simulator ===")
        print("1. Create transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test (double-spend)")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            sender = input("Sender: ")
            receiver = input("Receiver: ")
            amount = float(input("Amount: "))

            utxos = utxo.get_utxos_for_owner(sender)
            if not utxos:
                print("No funds")
                continue

            tx_id, index, bal = utxos[0]
            fee = 0.001
            change = bal - amount - fee
            tx = Transaction(
                gen_tx_id(),
                [(tx_id, index)],
                [(amount, receiver), (change, sender)]
            )

            ok, msg = mempool.add_transaction(tx, utxo, validator)
            print(msg)

        elif choice == "2":
            show_utxos(utxo)

        elif choice == "3":
           for tx in mempool.transactions:
            print(f"{tx.tx_id}: inputs={tx.inputs}, outputs={tx.outputs}, fee={tx.fee(utxo):.4f}")


        elif choice == "4":
            miner = input("Miner name: ")
            block = mine_block(miner, mempool, utxo,blockchain)
            print("Block mined. Fees:", block.total_fees)

        elif choice == "5":
            print("Double-spend test")
            tx1 = Transaction("tx1", [("genesis", 0)], [(10, "Bob"), (39.999, "Alice")])
            tx2 = Transaction("tx2", [("genesis", 0)], [(10, "Charlie"), (39.999, "Alice")])
            print(mempool.add_transaction(tx1, utxo, validator))
            print(mempool.add_transaction(tx2, utxo, validator))

        elif choice == "6":
            break

if __name__ == "__main__":
    main()
