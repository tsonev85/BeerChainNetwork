from sbcapi.utils import *


class Block(dict):

    def __init__(self,
                 index,
                 prev_block_hash,
                 date_created,
                 mined_by,
                 difficulty,
                 transactions=None,
                 nonce=0):
        """
        Constructor
        :param index: <int>
        :param prev_block_hash: <hex>
        :param date_created: <int>
        :param transactions: <Transaction[]>
        :param difficulty: <int>
        :param nonce: <int>
        :param mined_by: <str>
        """
        if transactions is None:
            transactions = []
        self.index = index
        self.prev_block_hash = prev_block_hash
        self.date_created = date_created
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = nonce
        self.mined_by = mined_by
        self.miner_hash = None
        self.block_hash = self.calculate_block_hash()
        # Added to be json serializable
        dict.__init__(self,
                      index=self.index,
                      prev_block_hash=self.prev_block_hash,
                      date_created=self.date_created,
                      transactions=self.transactions,
                      difficulty=self.difficulty,
                      nonce=self.nonce,
                      mined_by=self.mined_by,
                      miner_hash=self.miner_hash,
                      block_hash=self.block_hash)

    def calculate_transactions_hash(self):
        """
        Returns hash of block transactions.
        :return:
        """
        return CryptoUtils.calc_sha256(self.transactions)

    def calculate_block_hash(self):
        """
        Returns hash of block information.
        :return:
        """
        data = str(self.index) \
               + str(self.prev_block_hash) \
               + str(self.date_created) \
               + self.calculate_transactions_hash() \
               + str(self.difficulty) \
               + str(self.mined_by)
        return CryptoUtils.calc_sha256(data)

    def calculate_miner_hash(self):
        """
        Calculates miner hash taking into account nonce.
        :return:
        """
        return CryptoUtils.calc_miner_hash(self.calculate_block_hash(), self.nonce)

    @staticmethod
    def is_block_valid(new_block, previous_block):
        """
        Validates if new_block has valid index, hash and miner hash
        :param new_block: <Block> New block
        :param previous_block: <Block> Previous block
        :return: <bool>
        """
        if previous_block.index + 1 != new_block.index:
            print("Invalid index.")
            return False
        if previous_block.block_hash != new_block.prev_block_hash:
            print("Invalid previous hash.")
            return False
        if new_block.block_hash != new_block.calculate_block_hash():
            print("Invalid block hash.")
            return False
        if new_block.miner_hash != new_block.calculate_miner_hash():
            print("Invalid miner hash")
            return False
        return True




