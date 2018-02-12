from flask.json import JSONEncoder
from sbcapi.model import *


class BeerChainJSONEncoder(JSONEncoder):
    def default(self, obj):
        """
        Serialize object to JSON
        :param obj: <object>
        :return:
        """
        if isinstance(obj, Block):
            return {
                'index': obj.index,
                'prev_block_hash': obj.prev_block_hash,
                'date_created': obj.date_created,
                'transactions': obj.transactions,
                'difficulty': obj.difficulty,
                'nonce': obj.nonce,
                'miner_name': obj.mined_by,
                'miner_address': obj.miner_address,
                'miner_hash': obj.miner_hash,
                'block_hash': obj.block_hash,
            }
        if isinstance(obj, Transaction):
            return {
                'from_address': obj.from_address,
                'to_address': obj.to_address,
                'value': obj.value,
                'fee_percent': obj.fee_percent,
                'sender_pub_key': obj.sender_pub_key,
                'sender_signature': obj.sender_signature,
                'date_received': obj.date_received,
                'mined_in_block_index': obj.mined_in_block_index,
                'paid': obj.paid,
                'date_added_to_block': obj.date_added_to_block,
                'date_created': obj.date_created,
                'transaction_hash': obj.transaction_hash,
            }
        return super(BeerChainJSONEncoder, self).default(obj)