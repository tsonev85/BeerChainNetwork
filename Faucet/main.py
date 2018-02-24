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
        'max_avail': faucet.config['max_avail'],
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


app.run(host=faucet.config['default_host'], port=int(faucet.config['default_port']))