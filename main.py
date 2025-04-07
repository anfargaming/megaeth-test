from web3 import Web3
from eth_account import Account
import time

# === Load target address and private keys ===
with open("target_address.txt", "r") as f:
    TARGET_ADDRESS = f.read().strip()

with open("private_keys.txt", "r") as f:
    PRIVATE_KEYS = [line.strip() for line in f if line.strip()]

# === Connect to MEGA Testnet ===
RPC_URL = "https://carrot.megaeth.com/rpc"
CHAIN_ID = 6342  # Correct MegaETH testnet chain ID
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# === Main transfer logic ===
for i, pk in enumerate(PRIVATE_KEYS, 1):
    try:
        acct = Account.from_key(pk)
        address = acct.address

        print(f"\n[{i}] Processing: {address}")

        balance = w3.eth.get_balance(address)
        if balance == 0:
            print(" - Balance is 0, skipping.")
            continue

        gas_price = w3.eth.gas_price
        gas_limit = 21000
        gas_fee = gas_price * gas_limit

        if balance <= gas_fee:
            print(" - Not enough ETH to cover gas.")
            continue

        send_value = balance - gas_fee
        nonce = w3.eth.get_transaction_count(address)

        tx = {
            "nonce": nonce,
            "to": TARGET_ADDRESS,
            "value": send_value,
            "gas": gas_limit,
            "gasPrice": gas_price,
            "chainId": CHAIN_ID
        }

        signed_tx = w3.eth.account.sign_transaction(tx, pk)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(f" - TX sent: {tx_hash.hex()}")
        time.sleep(2)

    except Exception as e:
        print(f" - Error: {e}")
