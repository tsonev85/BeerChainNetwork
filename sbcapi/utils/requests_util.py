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

