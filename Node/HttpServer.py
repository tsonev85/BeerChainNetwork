from uuid import uuid4
from flask import Flask, jsonify, request
from sbcapi.model import *

# Instantiate our node server
app = Flask(__name__)

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

@app.route('/give_me_beer', methods=['POST'])
def get_job():
    values = request.get_json()
    # Check that the required fields are in the POST'ed data
    required = ['minerAddress']
    if not all(k in values for k in required):
        return 'Missing values', 400
    hash, dificulty = node.get_mining_job(values['minerAddress'])
    response = {
        'hash': hash,
        'dificulty': dificulty
    }
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5555, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1', port=port)



