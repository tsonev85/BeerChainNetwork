from flask import Flask, jsonify, request
from Faucet.faucet import *


# Instantiate faucet
faucet = Faucet()

# Instantiate faucet server
app = Flask(__name__)


@app.route('/faucet_info', methods=["GET"])
def faucet_info():
    response = {
        'faucet_address': faucet.faucet_address,
        'connected_to_node': faucet.config['node_url'],
        'default_coins_to_send': faucet.config['coins_to_send']
    }
    return jsonify(response), 200


@app.route('/send_coins', methods=['POST'])
def send_coins():
    values = request.get_json()
    required = ['to_address']
    if not all(k in values for k in required):
        return 'Missing values', 400
    result, msg = faucet.send_coins(values['to_address'], values['amount'])
    if result:
        return jsonify({
            'result': 'Coins successfully sent',
            'transaction_hash': msg
        }), 200
    else:
        return jsonify({
            'result': 'Coins not sent',
            'reason': msg
        }), 400


@app.route('/check_transaction', methods=['POST'])
def check_transaction():
    values = request.get_json()
    required = ['transaction_hash', 'sender_signature', 'sender_pub_key']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # sender_pub_key = tuple(int(x) for x in transaction['sender_pub_key']),
    # sender_signature = tuple(int(x) for x in transaction['sender_signature']),
    pub_key = tuple(int(x) for x in values['sender_pub_key'])
    transaction_hash = values['transaction_hash']
    signature = tuple(int(x) for x in values['sender_signature'])
    if faucet.validate_transaction(pub_key, transaction_hash, signature):
        return jsonify({
            'result': True,
            'msg': 'Transaction is valid'
        }), 200
    else:
        return jsonify({
            'result': False,
            'msg': 'Transaction validation error'
        }), 400


if __name__ == '__main__':

    app.run(host=faucet.config['default_host'], port=int(faucet.config['default_port']))