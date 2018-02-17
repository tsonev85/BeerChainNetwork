from uuid import uuid4
from flask import Flask, jsonify, request
from sbcapi.model import *
from sbcapi.utils import *
from sbcapi.utils import ArgParser
import threading


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
    # broadcast to all except sender
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


@app.route('/get_block_by_hash', methods=['POST'])
def get_block_by_hash():
    values = request.get_json()
    required = ['hash']
    if not all(k in values for k in required):
        return 'Missing values', 400
    response = [item for item in node.block_chain.blocks if item.miner_hash == values['hash']]
    return jsonify(response), 200


@app.route('/get_block_by_index', methods=['POST'])
def get_block_by_index():
    values = request.get_json()
    required = ['index']
    if not all(k in values for k in required):
        return 'Missing values', 400
    return jsonify(node.block_chain.blocks[int(values['index'])]), 200


@app.route('/get_last_block', methods=['GET'])
def get_last_block():
    return jsonify(node.block_chain.blocks[-1]), 200


@app.route('/get_blocks_range', methods=['POST'])
def get_blocks_range():
    values = request.get_json()
    required = ['from_index', 'to_index']
    if not all(k in values for k in required):
        return 'Missing values', 400
    from_index = int(values['from_index'])
    to_index = int(values['to_index'])
    range = to_index-from_index
    if range < 0 or range > 50:
        return 'Invalid range', 400
    return jsonify(node.block_chain.blocks[from_index:to_index]), 200


@app.route('/add_peer', methods=['POST'])
def add_peer():
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['peer', 'node_identifier']
    if not all(k in values for k in required):
        return 'Missing values', 400
    node.peers.append({
        "peer": values['peer'],
        "node_identifier": values['node_identifier']
    })
    # TODO
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
    # broadcast to all
    return 'Mined block successfully added.', 200


def flask_runner(port):
    app.run(host='127.0.0.1', port=port)


if __name__ == '__main__':
    port = ArgParser.get_args().port
    flask_starter = threading.Thread(target=flask_runner, args=[port])
    flask_starter.start()

