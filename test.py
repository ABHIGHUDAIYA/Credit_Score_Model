import json

def main():
    input_path = r"C:\Users\AbhiG\Downloads\CreditScoreModel\data\user-wallet-transactions.json"

    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return

    print(f"Total records in JSON: {len(data)}")
    if len(data) == 0:
        print("The JSON file is empty.")
        return

    print("First 5 transactions userWallet values:")
    for i, txn in enumerate(data[:5]):
        wallet = txn.get('userWallet')
        print(f"Transaction {i+1} userWallet: {repr(wallet)}")

if __name__ == "__main__":
    main()
