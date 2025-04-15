from flask import Flask, render_template, request
from crypto import trace_input_wallet, trace_transaction_chain, get_wallet_details, analyze_suspicious_wallets, summarize_funds, print_summary

app = Flask(__name__)

btc_to_inr = 5053094.57

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tx/<tx_hash>')
def transaction_details(tx_hash):
    try:
        
        input_wallets = trace_input_wallet(tx_hash)
        receivers = trace_transaction_chain(tx_hash)
        wallet_addresses = [wallet['address'] for wallet in receivers]
        wallet_details = [get_wallet_details(address) for address in wallet_addresses]
        suspicious_wallets = analyze_suspicious_wallets(wallet_details)
        fund_summary = summarize_funds(input_wallets, receivers, suspicious_wallets)

        
        return render_template('result.html', fund_summary=fund_summary, btc_to_inr=btc_to_inr)
    except Exception as e:
        return f"Error processing the transaction: {e}"

if __name__ == '__main__':
    app.run(debug=True)
