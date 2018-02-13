import requests as r
import json
from sbcapi.model import *
from sbcapi.utils import *


HEADERS = {'content-type': 'application/json'}

def get_block_chain_from_peer(peer):
    peer_chain = r.get(peer+"/chain").content.decode()
    print(peer_chain)
    # return BlockChain()

def get_block_by_index(peer, index):
    request_data = {"index": str(index)}
    url = peer + "/get_block_by_index"
    response = r.post(url, data=json.dumps(request_data), headers=HEADERS).content.decode()
    return json.loads(response, object_hook=json_block_decoder)

def get_last_block():
    pass

def get_block_by_hash():
    pass

def get_blocks_range():
    pass
