import time
from sbcapi.utils import *

class Transaction:

    def __init__(self,
                 to_address,
                 value,
                 fee_percent,
                 sender_pub_key,
                 sender_signature,
                 mined_in_block_index,
                 date_added_to_block,
                 from_address=None,
                 date_created=time.time(),
                 paid=False):
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
        # from + to + value + sender_pub_key + date_created
        return 1

    def sign_transaction(self, private_key):
        return CryptoUtils.sign_transaction(private_key, self.transaction_hash)

    def is_signature_valid(self):
        pass

    def is_transaction_valid(self):
        self.is_signature_valid()
        # check if enough moneh
        pass
