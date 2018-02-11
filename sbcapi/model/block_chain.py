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
        """
        Iterates trough elements of chain and checks if they are valid
        :param chain:
        :return:
        """
        if len(chain) <= 1:
            # Only 1 or 0 elements in chain -> nothing to check
            return True
        # start from second element of chain
        for index, element in enumerate(chain[1:]):
            if not BlockChain.new_block_valid(element, chain[index]):
                return False
        return True

    @staticmethod
    def new_block_valid(new_block, previous_block):
        """
        Validates if new_block has valid index, hash and miner hash
        :param new_block: <dict> Block
        :param previous_block: <dict> Block
        :return: bool
        """
        return Block.is_block_valid(new_block, previous_block)


