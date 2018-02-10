from sbcapi.model import *
import time


class BlockChain:

    def __init__(self):
        self.genesis_block = Block(
            index=0,
            prev_block_hash=0,
            date_created=int(time.time()),
            mined_by="BeerPpl"
        )
        self.blocks =[]
        self.blocks.append(self.genesis_block)

    def add_to_blockchain(self):
        pass

    def replace_chain(self, chain):
        pass

    @staticmethod
    def is_valid_chain(chain):
        pass

    def is_new_block_valid(self, new_block, nonce):
        pass


