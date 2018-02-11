import time
from sbcapi.utils import *


class Transaction(dict):

    def __init__(self,
                 to_address,
                 value,
                 sender_pub_key,
                 sender_signature,
                 date_created,
                 mined_in_block_index=None,
                 from_address=None,
                 paid=False,
                 fee_percent=5):
        """
        Constructor
        :param from_address: <str>
        :param to_address: <str>
        :param value: <int>
        :param fee_percent: <int>
        :param sender_pub_key: <hex>
        :param sender_signature: <tuple<hex><hex>>
        :param mined_in_block_index: <int>
        :param date_added_to_block: <int>
        :param date_created: <float>
        :param paid: <bool>
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
        self.date_received = time.time()
        self.mined_in_block_index = mined_in_block_index
        self.paid = paid
        self.date_added_to_block = None
        self.date_created = date_created
        self.transaction_hash = self.calculate_transaction_hash()
        # Added to be json serializable
        dict.__init__(self,
                      from_address=self.from_address,
                      to_address=self.to_address,
                      value=self.value,
                      fee_percent=self.fee_percent,
                      sender_pub_key=self.sender_pub_key,
                      sender_signature=self.sender_signature,
                      date_received=self.date_received,
                      mined_in_block_index=self.mined_in_block_index,
                      paid=self.paid,
                      date_added_to_block=self.date_added_to_block,
                      transaction_hash=self.transaction_hash,
                      date_created=self.date_created)

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
            hashed_data=self.transaction_hash,
            signature=self.sender_signature)

    def has_enough_balance(self):
        self.is_transaction_valid()
        # TODO
        # check if enough money
        pass
