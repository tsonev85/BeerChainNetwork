from sbcapi.utils import *

class Block:

    def __init__(self,
                 index,
                 prev_block_hash,
                 date_created,
                 transactions=None,
                 difficulty=4,
                 nonce=0,
                 mined_by=None):
        """
        Constructor
        :param index: <int>
        :param prev_block_hash: <hex>
        :param date_created: <int>
        :param transactions: <dict[]> Transaction
        :param difficulty: <int>
        :param nonce: <int>
        :param mined_by: <str>
        """
        self.index = index
        self.block_hash = self.calculate_block_hash()
        self.prev_block_hash = prev_block_hash
        self.date_created = date_created
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = nonce
        self.mined_by = mined_by

    def calculate_transactions_hash(self):
        pass

    def calculate_block_hash(self):
        #index + prev_block_hash + date_created + hash of transactions + difficulty + mined_by
        # return sha256
        return 1

    def is_block_valid(self):
        # return (calculateHashForBlock(newBlock) !== newBlock.hash)
        pass


