import requests
from sklearn.cluster import DBSCAN
import numpy as np
import csv
from requests.exceptions import RequestException
# Test TX Hash: ed1b8647be6a514e589e9450255f7e85fee534c6b2536f8a04f64ed330087e7b
# BlockCypher API token
API_TOKEN = '<YOUR-API-KEY>'
BASE_URL = 'https://api.blockcypher.com/v1/btc/main/'

# Manually enter the current value of 1 BTC to INR
btc_to_inr = 5053094.57

def get_transaction_details(tx_hash):
    """
    Retrieve details of a Bitcoin transaction using its hash.
    """
    url = f'{BASE_URL}txs/{tx_hash}?token={API_TOKEN}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"Transaction with hash {tx_hash} not found.")
        else:
            print(f"Error retrieving transaction details: {response.status_code}")
    except RequestException as e:
        print(f"Error contacting BlockCypher API: {e}")
    return None

def trace_transaction_chain(tx_hash, visited=None):
    """
    Recursively trace the transaction chain until reaching unspent outputs.
    """
    if visited is None:
        visited = set()
    
    if tx_hash in visited:
        return []

    visited.add(tx_hash)

    transaction = get_transaction_details(tx_hash)
    if not transaction:
        return []

    receivers = []

    outputs = transaction.get('outputs', [])
    for output in outputs:
        if 'spent_by' in output:
            next_tx_hash = output['spent_by']
            receivers.extend(trace_transaction_chain(next_tx_hash, visited))
        else:
            receivers.append({
                'address': output['addresses'][0],
                'value': output['value'] / 1e8  # Convert satoshis to BTC
            })

    return receivers

def get_wallet_details(address):
    """
    Retrieve details of a Bitcoin wallet using its address.
    """
    try:
        url = f'{BASE_URL}addrs/{address}?token={API_TOKEN}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error retrieving wallet details: {response.status_code}")
            return {}
    except RequestException as e:
        print(f"Error contacting BlockCypher API: {e}")
        return {}

def analyze_suspicious_wallets(wallet_details):
    """
    Analyze the list of wallet details to find the most significant and potentially suspicious wallets using clustering analysis.
    """
    data = []
    for details in wallet_details:
        if details:
            data.append([
                details.get('balance', 0),
                details.get('n_tx', 0),
                details.get('total_received', 0)
            ])
    
    if not data:
        print("No wallet data available for clustering.")
        return {}

    data = np.array(data)
    clustering = DBSCAN(eps=0.5, min_samples=5).fit(data)
    labels = clustering.labels_

    unique_labels = np.unique(labels)
    if len(unique_labels) <= 1:
        print("Warning: Only one cluster found. Adjusting clustering parameters may be necessary.")
    
    suspicious_wallets = {}
    for label, details in zip(labels, wallet_details):
        if label not in suspicious_wallets:
            suspicious_wallets[label] = []
        suspicious_wallets[label].append(details)

    return suspicious_wallets

def print_summary(fund_summary, btc_to_inr):
    """
    Print the summary of funds including input wallets, end wallets, and suspicious wallets.
    """
    print("Input Wallets:")
    for wallet in fund_summary['input_wallets']:
        balance_btc = wallet.get('balance', 0) / 1e8  # Convert satoshis to BTC
        total_received_btc = wallet.get('total_received', 0) / 1e8
        total_sent_btc = wallet.get('total_sent', 0) / 1e8
        print(f"  Address: {wallet['address']}")
        print(f"    Balance: {balance_btc} BTC ({balance_btc * btc_to_inr:.2f} INR)")
        print(f"    Total Received: {total_received_btc} BTC ({total_received_btc * btc_to_inr:.2f} INR)")
        print(f"    Total Sent: {total_sent_btc} BTC ({total_sent_btc * btc_to_inr:.2f} INR)")
        print(f"    Total Transactions: {wallet.get('n_tx', 0)}")

    print("\nEnd Wallets:")
    for wallet in fund_summary['end_wallets']:
        balance_btc = wallet.get('balance', 0) / 1e8  # Convert satoshis to BTC
        total_received_btc = wallet.get('total_received', 0) / 1e8
        total_sent_btc = wallet.get('total_sent', 0) / 1e8
        print(f"  Address: {wallet['address']}")
        print(f"    Balance: {balance_btc} BTC ({balance_btc * btc_to_inr:.2f} INR)")
        print(f"    Total Received: {total_received_btc} BTC ({total_received_btc * btc_to_inr:.2f} INR)")
        print(f"    Total Sent: {total_sent_btc} BTC ({total_sent_btc * btc_to_inr:.2f} INR)")
        print(f"    Total Transactions: {wallet.get('n_tx', 0)}")

    print("\nSuspicious Wallets:")
    for cluster, wallets in fund_summary['suspicious_wallets'].items():
        print(f"\nCluster {cluster}:")
        for wallet in wallets:
            balance_btc = wallet.get('balance', 0) / 1e8  # Convert satoshis to BTC
            total_received_btc = wallet.get('total_received', 0) / 1e8
            total_sent_btc = wallet.get('total_sent', 0) / 1e8
            print(f"  Address: {wallet['address']}")
            print(f"    Balance: {balance_btc} BTC ({balance_btc * btc_to_inr:.2f} INR)")
            print(f"    Total Received: {total_received_btc} BTC ({total_received_btc * btc_to_inr:.2f} INR)")
            print(f"    Total Sent: {total_sent_btc} BTC ({total_sent_btc * btc_to_inr:.2f} INR)")
            print(f"    Total Transactions: {wallet.get('n_tx', 0)}")

def trace_input_wallet(tx_hash):
    """
    Trace the input wallet(s) of a transaction.
    """
    transaction = get_transaction_details(tx_hash)
    if not transaction:
        return None

    inputs = transaction.get('inputs', [])
    input_wallets = []
    for input_tx in inputs:
        if 'addresses' in input_tx:
            address = input_tx['addresses'][0]
            wallet_details = get_wallet_details(address)
            if wallet_details:
                input_wallets.append({
                    'address': address,
                    'balance': wallet_details.get('balance', 0),
                    'total_received': wallet_details.get('total_received', 0),
                    'total_sent': wallet_details.get('total_sent', 0),
                    'n_tx': wallet_details.get('n_tx', 0)
                })
    
    return input_wallets

def summarize_funds(input_wallets, receivers, suspicious_wallets):
    """
    Summarize the flow of funds, including spent and unspent amounts.
    """
    total_spent = sum(receiver['value'] for receiver in receivers)
    
    total_unspent = 0
    for cluster_wallets in suspicious_wallets.values():
        for wallet in cluster_wallets:
            total_unspent += wallet.get('balance', 0) / 1e8  # Convert satoshis to BTC
    
    return {
        'input_wallets': input_wallets,
        'end_wallets': receivers,
        'suspicious_wallets': suspicious_wallets,
        'total_spent': total_spent,
        'total_unspent': total_unspent
    }

def load_csv_data(file_path):
    """
    Load wallet addresses and associated data from a CSV file.
    """
    csv_data = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                address = row.get('address')
                if address:
                    csv_data[address] = row
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return csv_data

def match_wallets(wallet_details, csv_data):
    """
    Cross-reference wallet addresses with known entities from CSV data.
    """
    matched_wallets = []
    for wallet in wallet_details:
        address = wallet.get('address')
        if address in csv_data:
            matched_wallets.append({**wallet, **csv_data[address]})
    return matched_wallets

# Execution
TX_HASH = "ed1b8647be6a514e589e9450255f7e85fee534c6b2536f8a04f64ed330087e7b"

try:
    input_wallets = trace_input_wallet(TX_HASH)
    receivers = trace_transaction_chain(TX_HASH)
    wallet_addresses = [wallet['address'] for wallet in receivers]
    wallet_details = [get_wallet_details(address) for address in wallet_addresses]
    suspicious_wallets = analyze_suspicious_wallets(wallet_details)
    fund_summary = summarize_funds(input_wallets, receivers, suspicious_wallets)
    print_summary(fund_summary, btc_to_inr)
except Exception as e:
    print(f"Error tracing funds: {e}")
