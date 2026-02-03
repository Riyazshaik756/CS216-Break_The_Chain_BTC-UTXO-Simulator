# CS216-Break_The_Chain_BTC-UTXO-Simulator
UTXO Simulator for CS216

 Team Details

Team Name: Break The Chain

Team Members:
	•	Name: Boddu_Kunal_______ | Roll No: 240003020
	•	Name: Shaik Riyaj_______ | Roll No: 240001068
	•	Name: Sangati Chakradhar Reddy | Roll No: 240001063
	•	Name: Kesavarapu__Deepak__Reddy | Roll No: 240041022



▶ Instructions to Run the Program

This project is implemented in Python and simulates a simplified Bitcoin transaction system using the UTXO model.

To run the program, first ensure that Python 3.8 or higher is installed on your system. Download or clone the project repository and open a terminal or command prompt in the project directory. Make sure that all project files are present in the same folder.

Run the program using the following command:
 main.py


After running the program, a menu-driven interface will be displayed on the terminal. Using this menu, the user can create new transactions, view the current UTXO set, view pending transactions in the mempool, mine new blocks, and run test scenarios such as a double-spend attack simulation.

⸻

 Design Explanation

The project is designed to simulate a simplified version of the Bitcoin blockchain transaction mechanism using the Unspent Transaction Output (UTXO) model. Instead of maintaining account balances directly, the system tracks individual unspent outputs that belong to users. Each transaction consumes existing UTXOs as inputs and creates new UTXOs as outputs.

The "UTXOManager" module is responsible for maintaining the global UTXO set. It stores all unspent outputs and provides functionality to add new UTXOs, remove spent ones, and calculate user balances.

The "Transaction" module represents a transaction object containing inputs and outputs. Inputs refer to previous UTXOs, while outputs define new ownership and amounts. The transaction also supports fee calculation based on the difference between total inputs and outputs.

The "Validator" module performs validation of each transaction before it is added to the mempool. It checks whether the referenced UTXOs exist, whether they belong to the sender, whether they have already been spent, and whether the total input amount is sufficient. This ensures that invalid and double-spend transactions are rejected.

The "Mempool" module stores all valid but unconfirmed transactions. These transactions remain in the mempool until they are selected by the miner and included in a block.

The "Mining" module simulates block mining. During mining, a set of transactions is selected from the mempool and applied to the UTXO set. Spent outputs are removed, new outputs are added, and transaction fees are collected by the miner. A new block object is created and appended to the blockchain list.

Additionally, the project includes a test scenario module that demonstrates a double-spend attack attempt. This helps in showing how the validator and UTXO system correctly prevent the same UTXO from being spent more than once.


