from uuid import uuid4
from flask import Flask, jsonify, request
from sbcapi.model import *
from sbcapi.utils import *


# Instantiate our node server
app = Flask(__name__)
app.json_encoder = BeerChainJSONEncoder

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Node
node = Node(node_identifier)


@app.route('/', methods=["GET"])
def node_info():
    response = {
        'nodeIdentifier': node.node_identifier,
        'lengthOfBlockChain': len(node.block_chain.blocks)
    }
    return jsonify(response), 200

@app.route('/add_new_block', methods=['POST'])
def add_new_block():
    # TODO
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['block']
    if not all(k in values for k in required):
        return 'Missing values', 400
    new_block = values['block']
    required_for_new_block = ['']
    if not all(k in new_block for k in required_for_new_block):
        return 'Missing required values for new block creation', 400
    new_block = Block()
    # TODO check if exists
    if not node.add_new_block(new_block):
        return 'Block validation failed. Block NOT added to block chain', 400
    return jsonify({
        "result": "Block successfully added",
        "block": new_block
    }), 200

@app.route('/chain', methods=["GET"])
def get_block_chain():
    response = {
        'blocks': node.block_chain.blocks,
        'lengthOfBlockChain': len(node.block_chain.blocks)
    }
    return jsonify(response), 200

@app.route('/add_peers', methods=['POST'])
def add_peers():
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['peers']
    if not all(k in values for k in required):
        return 'Missing values', 400
    node.peers.append(values['peers'])
    return "Peers successfully added.", 200

@app.route('/peers', methods=["GET"])
def get_peers():
    response = {
        'peers': node.peers
    }
    return jsonify(response), 200

@app.route('/add_transactions', methods=['POST'])
def add_transactions():
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['transactions']
    if not all(k in values for k in required):
        return 'Missing values', 400
    transactions = values['transactions']
    failed_transactions = []
    successfully_added = []
    required_for_transaction = ['to_address', 'value', 'sender_pub_key', 'sender_signature', 'date_created']
    for transaction in transactions:
        # Check that the required fields are in the POSTed data
        if not all(k in transaction for k in required_for_transaction):
            failed_transactions.append(transaction)
            continue
        transaction = Transaction(to_address=transaction['to_address'],
                                  value=int(transaction['value']),
                                  sender_pub_key=tuple(int(x) for x in transaction['sender_pub_key']),
                                  sender_signature= tuple(int(x) for x in transaction['sender_signature']),
                                  date_created=float(transaction['date_created']))
        if node.add_to_pending_transactions(transaction):
            successfully_added.append(transaction)
        else:
            failed_transactions.append(transaction)
    response = {
        'successfullyAdded': successfully_added,
        'failedToAdd': failed_transactions
    }
    return jsonify(response), 200

@app.route('/pending_transactions', methods=["GET"])
def get_pending_transactions():
    response = {
        'pendingTransactions': node.new_block.transactions
    }
    return jsonify(response), 200

@app.route('/give_me_beer', methods=['POST'])
def get_job():
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['minerAddress', 'miner_name']
    if not all(k in values for k in required):
        return 'Missing values', 400
    hash, dificulty = node.get_mining_job(values)
    response = {
        'hash': hash,
        'dificulty': dificulty
    }
    return jsonify(response), 200

@app.route('/heres_beer', methods=['POST'])
def receive_mining_job():
    values = request.get_json()
    required = ['miner_name', 'miner_address', 'original_hash', 'mined_hash', 'nonce', 'difficulty']
    if not all(k in values for k in required):
        return 'Missing values', 400
    if not node.add_block_from_miner(values):
        return 'Mined block validation error', 400
    return 'Mined block successfully added.', 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5555, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1', port=port)



