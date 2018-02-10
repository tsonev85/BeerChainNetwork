from sbcapi.utils import *

class Block:

    def __init__(self,
                 index,
                 block_hash,
                 block_data_hash,
                 prev_block_hash,
                 date_created,
                 transactions,
                 difficulty,
                 nonce,
                 mined_by):
        """
        Constructor
        :param index: <int>
        :param block_hash: <hex>
        :param block_data_hash: <hex>
        :param prev_block_hash: <hex>
        :param date_created: <int>
        :param transactions: <dict[]> Transaction
        :param difficulty: <int>
        :param nonce: <int>
        :param mined_by: <str>
        """
        self.index = index
        self.block_hash = block_hash
        self.block_data_hash = block_data_hash
        self.prev_block_hash = prev_block_hash
        self.date_created = date_created
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = nonce
        self.mined_by = mined_by

    def calculate_transactions_hash(self):
        pass

    def calculate_hash_for_miner(self):
        pass

