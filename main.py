from my_utils import engineer_features, calculate_scores, save_scores
import json

def main():
    input_path = r"C:\Users\AbhiG\Downloads\CreditScoreModel\data\user-wallet-transactions.json"
    output_path = "output/wallet_scores.json"

    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    print(f"Total records loaded: {len(data)}")

    features = engineer_features(data)
    print(f"Features DataFrame shape: {features.shape}")
    print(f"Features index sample: {features.index[:5]}")

    scores = calculate_scores(features)
    print(f"Scores sample: {list(scores.items())[:5]}")

    save_scores(scores, output_path)
    print(f"Saved scores to {output_path}")

if __name__ == "__main__":
    main()
