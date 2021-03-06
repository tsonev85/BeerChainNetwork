from uuid import uuid4
from flask import Flask, jsonify, request
from sbcapi.model import *
from sbcapi.utils import *
from sbcapi.threading.server_queue import *
from sbcapi.utils import requests_util as r
from flask_cors import CORS
import threading


# Instantiate our node server
app = Flask(__name__)
app.json_encoder = BeerChainJSONEncoder

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Node
node = Node(node_identifier)

# Instantiate the server task queue
task_queue = ServerTaskQueue()


@app.route('/', methods=["GET"])
def node_info():
    response = {
        'nodeIdentifier': node.node_identifier,
        'lengthOfBlockChain': len(node.get_blockchain().blocks)
    }
    return jsonify(response), 200


@app.route('/add_new_block', methods=['POST'])
def add_new_block():
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['block', 'node_identifier']
    if not all(k in values for k in required):
        return 'Missing values', 400
    new_block = values['block']
    required_for_new_block = Block.get_required_fields()
    if not all(k in new_block for k in required_for_new_block):
        return 'Missing required values for new block creation', 400
    new_block = json_block_decoder(new_block)
    if not node.add_new_block(new_block):
        return 'Block validation failed. Block NOT added to block chain', 400
    return "Block successfully added", 200


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
    # return None if nothing found
    response = next((item for item in node.block_chain.blocks if item.miner_hash == values['hash']), None)
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
    return jsonify(node.get_blockchain().blocks[-1]), 200


@app.route('/get_blocks_range', methods=['POST'])
def get_blocks_range():
    values = request.get_json()
    required = ['from_index', 'to_index']
    if not all(k in values for k in required):
        return 'Missing values', 400
    from_index = int(values['from_index'])
    if values['to_index'] == "None":
        return jsonify(node.get_blockchain().blocks[from_index:]), 200
    to_index = int(values['to_index'])
    range = to_index-from_index
    if range < 0 or range > 50:
        return 'Invalid range', 400
    return jsonify(node.get_blockchain().blocks[from_index:to_index]), 200


@app.route('/get_transaction_by_hash', methods=['POST'])
def get_transaction_by_hash():
    values = request.get_json()
    required = ['hash']
    if not all(k in values for k in required):
        return 'Missing values', 400
    # return None if nothing found
    requested_hash = int(values['hash']);
    for t in node.new_block.transactions:
        if requested_hash == t.transaction_hash:
            return jsonify(t), 200

    for block in node.get_blockchain().blocks:
        for t in block.transactions:
            if requested_hash == t.transaction_hash:
                return jsonify(t), 200

    return jsonify({}), 200


@app.route('/add_peer', methods=['POST'])
def add_peer():
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['peer', 'node_identifier']
    if not all(k in values for k in required):
        return 'Missing values', 400

    if values['node_identifier'] == node_identifier:
        return 'Cant add itself', 400

    existing_peer = next((peer for peer in node.get_peers() if peer['peer'] == values['peer']), None)
    if existing_peer:
        return 'Peer already exists', 400

    new_peer = {
        "peer": values['peer'],
        "node_identifier": values['node_identifier']
    }
    node.add_peer(new_peer)
    task_queue.put_task(sync_peers, (node, [new_peer]))
    # TODO
    return "Peers successfully added.", 200


@app.route('/peers', methods=["GET"])
def get_peers():
    response = {
        'peers': node.get_peers()
    }
    return jsonify(response), 200


@app.route('/add_transactions', methods=['POST'])
def add_transactions():
    # TODO make it use json deserializer
    values = request.get_json()
    # Check that the required fields are in the POSTed data
    required = ['transactions']
    if not all(k in values for k in required):
        return 'Missing values', 400
    transactions = values['transactions']
    failed_transactions = []
    successfully_added = []
    required_for_transaction = ['from_address', 'to_address', 'value', 'sender_pub_key', 'sender_signature',
                                'date_created', 'transaction_hash']
    for transaction in transactions:
        # Check that the required fields are in the POSTed data
        if not all(k in transaction for k in required_for_transaction):
            failed_transactions.append(transaction)
            continue
        sender_pub_key = str(transaction['sender_pub_key'])[1:-1].split(",")
        sender_signature = str(transaction['sender_signature'])[1:-1].split(",")
        transaction = Transaction(from_address=transaction['from_address'],
                                  to_address=transaction['to_address'],
                                  value=int(transaction['value']),
                                  sender_pub_key=tuple(int(x) for x in sender_pub_key),
                                  sender_signature=tuple(int(x) for x in sender_signature),
                                  date_created=float(transaction['date_created']),
                                  transaction_hash=int(transaction['transaction_hash']),
                                  faucet_transaction=transaction['faucet_transaction'])
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
    with node.blockchain_sync_lock:
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
    with node.blockchain_sync_lock:
        values = request.get_json()
        required = ['miner_name', 'miner_address', 'original_hash', 'mined_hash', 'nonce', 'difficulty']
        if not all(k in values for k in required):
            return 'Missing values', 400
        mined_block = node.add_block_from_miner(values)
        if mined_block is None:
            return 'Mined block validation error', 400
        award_miner(mined_block)
        task_queue.put_task(broadcast_newly_mined_block, (node, mined_block))
        return 'Mined block successfully added.', 200


def award_miner(mined_block):
    try:
        get_coins_from_faucet(ArgParser.get_args().faucet, mined_block.minerAddress, 5)
    except Exception:
        pass


def flask_runner(host, port):
    CORS(app)
    app.run(threaded=True, host=host, port=port)


def peers_list_sync():
    """
    On an interval loops through all node peers and refreshes the list
    """
    while True:
        time.sleep(60)
        peers = node.get_peers()
        task_queue.put_task(sync_peers, (node, peers))


def blockchain_sync_timer():
    """
    Puts blockchain_sync task in the queue on set interval
    """
    while True:
        task_queue.put_task(blockchain_sync, [node])
        time.sleep(15)


def blockchain_sync(node):
    """
    Loops through node peers, request their blockchain length, if theirs is bigger that ours, syncs the missing blocks
    """
    with node.blockchain_sync_lock:
        try:
            peer_to_sync_with = None
            best_block = None
            for peer_data in node.get_peers():
                peer = peer_data['peer']
                block = r.get_last_block(peer)
                if block.index > node.get_blockchain().blocks[-1].index:
                    if best_block is None:
                        best_block = block
                        peer_to_sync_with = peer
                    elif block.index > best_block.index:
                        best_block = block
                        peer_to_sync_with = peer

            if peer_to_sync_with is None:
                return

            starting_block = None
            i = len(node.get_blockchain().blocks) - 1
            while starting_block is None:
                starting_block = r.get_block_by_hash(peer_to_sync_with, node.get_blockchain().blocks[i].miner_hash)
                i -= 1
                if i < 0:
                    break;

            if starting_block is None:
                return;

            from_index = starting_block.index
            if from_index == 0:
                from_index = 1
            to_index = int(from_index) + 50
            while True:
                blocks_to_add = r.get_blocks_range(peer_to_sync_with, from_index, to_index)
                if len(blocks_to_add) == 0:
                    break
                for block in blocks_to_add:
                    node.add_new_block(block, block.index)

                from_index = to_index
                to_index += 50

        except Exception as ex:
            print("Something went wrong while trying to sync the blockchain: " + str(ex))


def initialPeerSync(node, initial_peers):
    """
    If there are peers set up in the node_config.json file, makes initial sync with them on server start up
    :param node: <Node>
    :param initial_peers: [<dict>]
    """
    for p in initial_peers:
        new_peer = {
            "peer": p['peer'],
            "node_identifier": p['node_identifier']
        }
        node.add_peer(new_peer)
    task_queue.put_task(sync_peers, (node, node.get_peers()))


if __name__ == '__main__':
    host = ArgParser.get_args().url
    port = ArgParser.get_args().port
    flask_starter = threading.Thread(name="Flask_Runner_Thread", target=flask_runner, args=[host, port])
    flask_starter.start()
    print("Node Identifier: " + node_identifier)

    try:
        initialPeerSync(node, ArgParser.get_args().peers)
    except Exception as ex:
        print("No initial peers list")

    peers_list_syncer = threading.Thread(name="Peer_Sync_Thread", target=peers_list_sync)
    peers_list_syncer.setDaemon(True)
    peers_list_syncer.start()

    blockchain_synchronizer = threading.Thread(name="Blockchain_Sync_Thread", target=blockchain_sync_timer)
    blockchain_synchronizer.setDaemon(True);
    blockchain_synchronizer.start()
