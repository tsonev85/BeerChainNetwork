from sbcapi.utils import *


class Block(dict):

    def __init__(self,
                 index,
                 prev_block_hash,
                 date_created,
                 miner_name,
                 miner_address,
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
        :param miner_name: <str>
        :param miner_address: <str>
        """
        if transactions is None:
            transactions = []
        self.index = index
        self.prev_block_hash = prev_block_hash
        self.date_created = date_created
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = nonce
        self.mined_by = miner_name
        self.miner_address = miner_address
        self.miner_hash = None
        self.block_hash = Block.calculate_block_hash(self)
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
                      miner_address = self.miner_address,
                      block_hash=self.block_hash)

    @staticmethod
    def calculate_transactions_hash(block):
        """
        Returns hash of block transactions.
        :return:
        """
        return CryptoUtils.calc_sha256(block.transactions)

    @staticmethod
    def calculate_block_hash(block):
        """
        Returns hash of block information.
        :return:
        """
        data = str(block.index) \
               + str(block.prev_block_hash) \
               + str(block.date_created) \
               + Block.calculate_transactions_hash(block) \
               + str(block.difficulty) \
               + str(block.mined_by)
        return CryptoUtils.calc_sha256(data)

    @staticmethod
    def calculate_miner_hash(block):
        """
        Calculates miner hash taking into account nonce.
        :return:
        """
        return CryptoUtils.calc_miner_hash(Block.calculate_block_hash(block), block.nonce)

    @staticmethod
    def is_block_valid(new_block, previous_block):
        """
        Validates if new_block has valid index, hash and miner hash
        :param new_block: <Block> New block
        :param previous_block: <Block> Previous block
        :return: <bool>
        """
        if not previous_block.index + 1 == new_block.index:
            print("Invalid index.")
            return False
        if previous_block.miner_hash != new_block.prev_block_hash:
            print("Invalid previous hash.")
            return False
        if new_block.block_hash != Block.calculate_block_hash(new_block):
            print("Invalid block hash.")
            return False
        if new_block.miner_hash != Block.calculate_miner_hash(new_block):
            print("Invalid miner hash")
            return False
        return True




