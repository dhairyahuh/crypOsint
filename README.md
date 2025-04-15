# 🚨 CryptoSint

**CryptoSint** is a blockchain transaction analysis tool that helps trace suspicious Bitcoin activity. Built with a Flask backend and an interactive frontend, it supports real-time transaction monitoring, wallet behavior analysis, and clustering of anomalous addresses using machine learning.

## 🔍 Features

- 🧾 **Transaction Hash Lookup** – Search any Bitcoin transaction by its hash.
- 🧠 **Suspicious Wallet Detection** – Uses DBSCAN clustering to identify wallets with abnormal transaction behavior.
- 📊 **Interactive Visuals** – Embeds visual transaction graphs and Sankey-like flow summaries.
- 👮 **For Law Enforcement & Analysts** – Simplifies blockchain forensics with structured reports.

## 🧰 Tech Stack

- **Frontend**: HTML5, Bootstrap, Tailwind CSS, Materialize CSS
- **Backend**: Python, Flask
- **Blockchain APIs**: BlockCypher, Coinbase
- **ML**: DBSCAN (scikit-learn)
- **Visualization**: Embedded tools (txgraph.info, fbbe.info)

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8+
- pip
- (Optional) Node.js & npm for frontend extensions

### 🔧 Installation & Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/cryptosint.git
   cd cryptosint


🚀 Getting Started

Follow these steps to run the CryptoSint application locally:

📦 Prerequisites
Python 3.8+
pip (Python package manager)
Node.js & npm (if planning to extend frontend)


🖥️ Installation & Setup

Clone the Repository
git clone https://github.com/your-username/cryptosint.git
cd cryptosint

Set Up Python Environment
python-m venv venv
source venv/bin/activate 
# On Windows use
`venv\Scripts\activate`
pip install -r requirements.txt

Run the Flask App
python app.py

Open in Browser
Navigate to:
http://127.0.0.1:5000

🧪 Usage Flow

Enter a Bitcoin Transaction Hash on the home page (index.html).
The backend fetches and analyzes wallet data.
The result page (result.html) shows:
Input and output wallet summaries
INR conversion estimates
Suspicious wallet clusters
Transaction visualizations via embedded iframes

