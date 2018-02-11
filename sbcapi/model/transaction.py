import time
from sbcapi.utils import *

class Transaction:

    def __init__(self,
                 to_address,
                 value,
                 sender_pub_key,
                 sender_signature,
                 mined_in_block_index,
                 date_added_to_block,
                 from_address=None,
                 date_created=time.time(),
                 paid=False,
                 fee_percent=0.05):
        """
        Constructor
        :param from_address: <str>
        :param to_address: <str>
        :param value: <int>
        :param fee_percent: <int>
        :param sender_pub_key: <hex>
        :param sender_signature: <hex>
        :param mined_in_block_index: <int>
        :param date_added_to_block: <int>
        :param date_created: <int>
        :param paid: <bool>
        """
        self.from_address = from_address
        self.to_address = to_address
        self.value = value - value*fee_percent
        self.fee_percent = fee_percent
        self.sender_pub_key = sender_pub_key
        self.sender_signature = sender_signature
        self.transaction_hash = self.calculate_transaction_hash()
        self.date_received = date_created
        self.mined_in_block_index = mined_in_block_index
        self.paid = paid
        self.date_added_to_block = date_added_to_block


    def calculate_transaction_hash(self):
        """
        Returns hash of transaction information.
        return:
        """
        data = str(self.from_address) \
               + str(self.to_address) \
               + str(self.value) \
               + self.sender_pub_key() \
               + str(self.sender_signature) \
               + str(self.date_received)
        return CryptoUtils.calc_sha256(data)

    def sign_transaction(self, private_key):
        """
        Sign transaction using owner's private and transaction data hash
        :param private_key: <str> Owner's private key
        :return: <tuple<int,int>>
        """
        return CryptoUtils.sign_transaction(private_key, self.transaction_hash)

    def is_transaction_valid(self):
        """
        Verifies transaction based on sender public key, transaction data hash
        and sender signature
        :return: <bool>
        """
        return CryptoUtils.verify_transaction(
            public_key=self.sender_pub_key,
            data=self.transaction_hash,
            signature=self.sender_signature)

    def has_enough_balance(self):
        self.is_transaction_valid()
        # check if enough money
        pass
