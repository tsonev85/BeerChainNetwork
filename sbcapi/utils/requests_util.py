import requests as r
import json
from collections import namedtuple
from sbcapi.model import *


HEADERS = {'content-type': 'application/json'}

def get_block_chain_from_peer(peer):
    peer_chain = r.get(peer+"/chain").content.decode()
    print(peer_chain)
    # return BlockChain()

def get_block_by_index(peer, index):
    # TODO Block is deserelialized from JSON, but list of transactions need different object hook
    request_data = {"index": str(index)}
    url = peer + "/get_block_by_index"
    response = r.post(url, data=json.dumps(request_data), headers=HEADERS).content.decode()
    # block_from_peer = json2obj(response)
    block_from_peer = json.loads(response, cls=Block)
    print(block_from_peer)

def _json_object_hook(d):
    return namedtuple('Block', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

# get_block_by_index("http://localhost:5555", 1)
# @app.route('/get_block_by_hash', methods=['POST'])
# def get_block_by_hash():
#     values = request.get_json()
#     required = ['hash']
#     if not all(k in values for k in required):
#         return 'Missing values', 400
#     response = [item for item in node.block_chain.blocks if item.miner_hash == values['hash']]
#     return jsonify(response), 200
#
# @app.route('/get_block_by_index', methods=['POST'])
# def get_block_by_index():
#     values = request.get_json()
#     required = ['index']
#     if not all(k in values for k in required):
#         return 'Missing values', 400
#     return jsonify(node.block_chain.blocks[int(values['index'])]), 200
#
# @app.route('/get_last_block', methods=['GET'])
# def get_last_block():
#     return jsonify(node.block_chain.blocks[-1]), 200
# @app.route('/get_blocks_range', methods=['POST'])
# def get_blocks_range():