# 🏦 DeFi Wallet Credit Scoring - Aave V2

This project builds a credit scoring model for wallets interacting with the **Aave V2 protocol**, assigning a score between **0 and 1000** based purely on transaction behavior. The purpose is to identify reliable DeFi users and distinguish them from potentially risky, bot-like, or exploitative wallets.

---

## 📁 Dataset

We use a raw JSON file (~87MB, ~100,000 records) containing transaction-level data from Aave V2 protocol. Each record includes:

- `userWallet`: Wallet address  
- `action`: Type of interaction (`deposit`, `borrow`, `repay`, `redeemunderlying`, `liquidationcall`)  
- `timestamp`, `blockNumber`, `txHash`, `assetSymbol`, `amount`, `assetPriceUSD`, etc.

📎 **[Download the Dataset](https://drive.google.com/file/d/1ISFbAXxadMrt7Zl96rmzzZmEKZnyW7FS/view?usp=sharing)**

---

## ⚙️ Methodology

### 🔧 1. Feature Engineering

We extract meaningful per-wallet financial signals:

| Feature Name            | Description                                         |
|------------------------|-----------------------------------------------------|
| `num_transactions`     | Total number of protocol interactions               |
| `total_deposit_usd`    | Total value of deposits in USD                      |
| `total_borrow_usd`     | Total borrow value in USD                           |
| `total_repay_usd`      | Total repayments in USD                             |
| `total_redeem_usd`     | Amount withdrawn via `redeemunderlying` in USD     |
| `num_liquidations`     | Count of liquidation events                         |
| `borrow_repay_ratio`   | Ratio of borrow to repay (risk signal)              |
| `deposit_redeem_ratio` | Ratio of deposit to redeem (loyalty signal)         |

---

### 📊 2. Scoring Logic

We assign scores by:

- **Rewarding** wallets that:
  - Deposit large stable amounts  
  - Regularly repay what they borrow
- **Penalizing** wallets that:
  - Get liquidated often  
  - Borrow heavily and never repay
- **Using ratios** to normalize across wallet scales and avoid whale dominance

✅ Final scores are scaled to a **0–1000** range for interpretability.

---

## 📈 3. Score Representation and Analysis

- The **`representation.py`** script is used to generate visualizations such as credit score distribution histograms and other insightful plots to analyze wallet behavior and scoring trends.
- The **`analysis.md`** file provides detailed analysis of the scoring results, including score distributions, behavioral insights for wallets in different score buckets, and potential areas for model improvement.

---

## 📝 Output Format

The wallet scores are saved in a JSON file at:

`output/wallet_scores.json`

**Example:**
```json
{
  "0x00000000001accfa9cef68cf5371a23025b6d4b6": 0,
  "0x0000000002032370b971dabd36d72f3e5a7bf1ee": 11,
  "0x000000003ce0cf2c037493b1dc087204bd7f713e": 13
}
````

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/defi-credit-score.git
cd defi-credit-score
```

### 2️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Main Script

```bash
python main.py
```

This loads the transaction file, computes features, assigns credit scores, and saves the results.

### 4️⃣ Generate Visualizations (Optional)

```bash
python representation.py
```

This generates graphical analyses of the wallet credit score distribution and other relevant plots saved in the `output/` folder.

---

## 🧪 Project Structure

```plaintext
CreditScoreModel/
├── data/
│   └── user-wallet-transactions.json     # Input data
├── output/
│   ├── wallet_scores.json                # Output credit scores
│   └── credit_score_distribution.png     # Visualizations output (from representation.py)
├── main.py                               # Main pipeline script
├── my_utils.py                           # Feature engineering & scoring logic
├── representation.py                     # Visualization and graphical analysis
├── test.py                               # Testing and validation helpers
├── README.md
└── analysis.md                           # Post-score analysis and insights
```

---

## 📌 Notes

* 📉 This model is unsupervised and based on heuristics (no labeled credit risk data).
* ⚖️ Ratios are used to ensure fair scoring between high- and low-volume wallets.
* 💡 Codebase is modular and can easily be extended with more features or ML models.

---

## 👨‍💻 Author

Abhi Ghudaiya
B.Tech CSE (Artificial Intelligence Specialization)

