class Transaction:

    def __init__(self,
                 from_address,
                 to_address,
                 value,
                 sender_pub_key,
                 sender_signature,
                 transaction_hash,
                 date_received,
                 mined_in_block_index,
                 paid):
        """
        Constructor
        :param from_address: <str>
        :param to_address: <str>
        :param value: <int>
        :param sender_pub_key: <hex>
        :param sender_signature: <hex>
        :param transaction_hash: <hex>
        :param date_received: <int>
        :param mined_in_block_index: <int>
        :param paid: <bool>
        """
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
        self.sender_pub_key = sender_pub_key
        self.sender_signature = sender_signature
        self.transaction_hash = transaction_hash
        self.date_received = date_received
        self.mined_in_block_index = mined_in_block_index
        self.paid = paid