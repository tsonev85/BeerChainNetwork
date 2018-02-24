import requests as r
import json
from sbcapi.model import *
from sbcapi.utils import *


HEADERS = {'content-type': 'application/json'}


def get_block_chain_from_peer(peer):
    """
    Retrieves block chain from provided peer
    :param peer: <str>
    :return: <Block[]>
    """
    response = r.get(peer+"/chain").content.decode()
    return json.loads(response, object_hook=json_block_decoder)


def get_block_by_index(peer, index):
    """
    Retrieves a block by its index from provided peer
    :param peer: <str>
    :param index: <str>
    :return: <Block>
    """
    request_data = {"index": str(index)}
    url = peer + "/get_block_by_index"
    response = r.post(url, data=json.dumps(request_data), headers=HEADERS).content.decode()
    return json.loads(response, object_hook=json_block_decoder)


def get_last_block(peer):
    """
    Retrieves the last block of provided peer block chain
    :param peer: <str>
    :return: <Block>
    """
    response = r.get(peer + "/get_last_block").content.decode()
    return json.loads(response, object_hook=json_block_decoder)


def get_block_by_hash(peer, hash):
    """
    Retrieves a block by MINER HASH from provided peer
    :param peer: <str>
    :param hash: <str>
    :return: <Block>
    """
    request_data = {"hash": str(hash)}
    url = peer + "/get_block_by_hash"
    response = r.post(url, data=json.dumps(request_data), headers=HEADERS).content.decode()
    return json.loads(response, object_hook=json_block_decoder)


def get_blocks_range(peer, from_index, to_index):
    """
    Retrieves a range of blocks by the specified from and to indexes
    :param peer: <str>
    :param from_index: <str>
    :param to_index: <str>
    :return: <Block[]>
    """
    request_data = {"from_index": str(from_index),
                    "to_index": str(to_index)}
    url = peer + "/get_blocks_range"
    response = r.post(url, data=json.dumps(request_data), headers=HEADERS).content.decode()
    return json.loads(response, object_hook=json_block_decoder)


def sync_peers(node, new_peers):
    """
    Loops through new_peers and request their peers list to add their peers to ours if missing
    Requesting to add our node in their list.

    This method is usually called when a new peer is added or by the timed 'peers_list_sync' job running in the server.
    :param node: <Node>
    :param new_peers: [<dict>]
    """
    for new_peer in new_peers:
        url = new_peer + "/peers"
        add_me_url = new_peer + "/add_peer"
        my_id = json.dumps({
            "peer": "http://127.0.0.1",
            "node_identifier": node.node_identifier
        })
        try:

            r.post(add_me_url, data=my_id, headers=HEADERS)

            response = r.get(url).content.decode()
            peers = json.loads(response)['peers']
            for peer in peers:
                _p = peer['peer']
                _id = peer['node_identifier']
                if _p == node.node_identifier:
                    continue
                existing_peer = next((p for p in node.get_peers() if p['peer'] == _p), None)
                if existing_peer:
                    continue
                node.add_peer({
                    "peer": _p,
                    "node_identifier": _id
                })
                add_me_url = _p + "/add_peer"
                r.post(add_me_url, data=my_id, headers=HEADERS)
        except Exception as ex:
            print("Connecting to peer [ " + peer + " ] went wrong: " + str(ex))


def broadcast_newly_mined_block(node, mined_block):
    """
    Broadcast the newly mined block to all peers
    :param node: <Node>
    :param mined_block: <Block>
    """
    try:
        for p in node.peers:
            url = p['peer'] + "/add_new_block"
            r.post(url, data=json.dumps(mined_block), HEADERS=HEADERS)
    except Exception as ex:
        print("Broadcasting to [ " + p + " ] went wrong" + str(ex))


def send_transactions(peer, transactions):
    """
    Sends transactions to be added to pending transactions in the node
    :param peer: <str>
    :param transactions: <Transaction[]>
    :return: <dict> response
    """
    url = peer + "/add_transactions"
    request_data = {
        "transactions": transactions
    }
    response = r.post(url, data=json.dumps(request_data, cls=BeerChainJSONEncoder), headers=HEADERS).content.decode()
    return json.loads(response, object_hook=json_block_decoder)


def get_coins_from_faucet(faucet_url, to_address, amount=None):
    """
    Orders the faucet to send coins to the provided address.
    Faucet will send a transaction that will be added to pending transactions
    of the node it is connected to.
    :param faucet_url: <str> Faucet url
    :param to_address: <str> Coins will be send to this address
    :param amount: <int> amount of coins to request, if empty default amount will be send
    :return: <dict> response
    """
    request_data = {
        "to_address": str(to_address),
        "amount": amount
    }
    url = faucet_url + "/send_coins"
    response = r.post(url, data=json.dumps(request_data), headers=HEADERS).content.decode()
    return json.loads(response)
