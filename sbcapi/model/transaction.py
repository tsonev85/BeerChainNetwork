import time
from sbcapi.utils import *


class Transaction(object):

    def __init__(self,
                 to_address,
                 value,
                 sender_pub_key,
                 sender_signature,
                 date_created,
                 mined_in_block_index=None,
                 from_address=None,
                 paid=False,
                 fee_percent=5,
                 date_received=None,
                 date_added_to_block = None,
                 transaction_hash=None):
        """
        Constructor
        :param to_address: <str>
        :param value: <int>
        :param sender_pub_key: <tuple<int><int>>
        :param sender_signature: <tuple<int><int>>
        :param date_created: <float>
        :param mined_in_block_index: <int>
        :param from_address: <str>
        :param paid: <bool>
        :param fee_percent: <int>
        :param date_received: <float>
        :param date_added_to_block: <float>
        :param transaction_hash: <float>
        """
        if from_address is None:
            from_address = CryptoUtils.generate_address(sender_pub_key)
        self.from_address = from_address
        self.to_address = to_address
        # TODO add value -= value*fee_percent
        self.value = value
        self.fee_percent = fee_percent
        self.sender_pub_key = sender_pub_key
        self.sender_signature = sender_signature
        if date_received is None:
            date_received = time.time()
        self.date_received = date_received
        self.mined_in_block_index = mined_in_block_index
        self.paid = paid
        self.date_added_to_block = date_added_to_block
        self.date_created = date_created
        if transaction_hash is None:
            transaction_hash = self.calculate_transaction_hash()
        self.transaction_hash = transaction_hash

    def calculate_transaction_hash(self):
        """
        Returns hash of transaction information.
        return: <str>
        """
        data = str(self.from_address) \
               + str(self.to_address) \
               + str(self.value) \
               + str(self.sender_pub_key) \
               + str(self.date_created)
        return CryptoUtils.keccak_hash(data)

    def sign_transaction(self, private_key):
        """
        Sign transaction using owner's private and transaction data hash
        :param private_key: <str> Owner's private key
        """
        self.sender_pub_key = CryptoUtils.sign_transaction(private_key, self.transaction_hash)

    def is_transaction_valid(self):
        """
        Verifies transaction based on sender public key, transaction data hash
        and sender signature
        :return: <bool>
        """
        return CryptoUtils.verify_transaction(
            public_key=self.sender_pub_key,
            hashed_data=self.transaction_hash,
            signature=self.sender_signature)

    def has_enough_balance(self):
        self.is_transaction_valid()
        # TODO
        # check if enough money
        pass
