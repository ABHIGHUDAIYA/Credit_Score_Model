import json
import pandas as pd
from tqdm import tqdm

def engineer_features(data):
    """
    Convert raw transaction list into a DataFrame with wallet-level aggregated features.
    """
    # Create a DataFrame from the list of transactions
    df = pd.DataFrame(data)
    
    # Confirm userWallet column exists
    if 'userWallet' not in df.columns:
        raise ValueError("userWallet column not found in data")

    # Convert amounts to numeric (from actionData.amount)
    # First, extract amount and convert it to float for aggregation
    def extract_amount(tx):
        try:
            return float(tx['actionData']['amount'])
        except Exception:
            return 0.0

    df['amount'] = df['actionData'].apply(extract_amount)
    
    # Aggregate features per wallet
    features = df.groupby('userWallet').agg(
        total_transactions = ('txHash', 'count'),
        total_deposited = ('amount', lambda x: x[df.loc[x.index, 'action'] == 'deposit'].sum()),
        total_borrowed = ('amount', lambda x: x[df.loc[x.index, 'action'] == 'borrow'].sum()),
        total_repaid = ('amount', lambda x: x[df.loc[x.index, 'action'] == 'repay'].sum()),
        total_redeemed = ('amount', lambda x: x[df.loc[x.index, 'action'] == 'redeemunderlying'].sum()),
        total_liquidations = ('amount', lambda x: x[df.loc[x.index, 'action'] == 'liquidationcall'].sum())
    )
    
    # Fill NaN with 0 for wallets missing some actions
    features.fillna(0, inplace=True)

    # Add some simple ratios or other engineered features if you want
    features['repay_to_borrow_ratio'] = features.apply(
        lambda row: row['total_repaid'] / row['total_borrowed'] if row['total_borrowed'] > 0 else 0, axis=1
    )
    features['redeem_to_deposit_ratio'] = features.apply(
        lambda row: row['total_redeemed'] / row['total_deposited'] if row['total_deposited'] > 0 else 0, axis=1
    )

    return features

def calculate_scores(features):
    """
    Simple scoring based on features:
    - Higher total transactions → higher score
    - High repay_to_borrow_ratio → higher score
    - High redeem_to_deposit_ratio → higher score
    - Penalize wallets with zero or very low repay_to_borrow_ratio or redeem_to_deposit_ratio
    Scores scaled 0-1000.
    """
    scores = {}
    
    # Normalize helpers to avoid division by zero
    max_tx = features['total_transactions'].max() or 1
    max_repay_ratio = features['repay_to_borrow_ratio'].max() or 1
    max_redeem_ratio = features['redeem_to_deposit_ratio'].max() or 1

    for wallet, row in features.iterrows():
        tx_score = row['total_transactions'] / max_tx
        repay_score = row['repay_to_borrow_ratio'] / max_repay_ratio
        redeem_score = row['redeem_to_deposit_ratio'] / max_redeem_ratio

        # Weighted sum
        score = 0.4 * tx_score + 0.3 * repay_score + 0.3 * redeem_score
        score = max(0, min(score, 1))  # Clamp between 0 and 1

        scores[wallet] = int(score * 1000)

    return scores

def save_scores(scores, output_path):
    """
    Save scores dict to JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(scores, f, indent=2)
