from flask.json import JSONEncoder
from sbcapi.model import *


class BeerChainJSONEncoder(JSONEncoder):
    def default(self, obj):
        """
        Serialize object to JSON
        :param obj: <object>
        :return: <json object>
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
                'current_state_balances': obj.current_state_balances,
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


def json_block_decoder(obj):
    """
    Deserialize json object to Block object
    :param obj: <json object>
    :return: <Block>
    """
    if 'block_hash' in obj and 'miner_hash' in obj:
        transactions = []
        for transaction in obj['transactions']:
            transactions.append(json_transaction_decoder(transaction))
        # TODO check if cast needs to be done just in case
        return Block(index=obj['index'],
                     prev_block_hash=obj['prev_block_hash'],
                     date_created=obj['date_created'],
                     transactions=transactions,
                     difficulty=obj['difficulty'],
                     nonce=obj['nonce'],
                     miner_name=obj['miner_name'],
                     miner_address=obj['miner_address'],
                     miner_hash=obj['miner_hash'],
                     block_hash=obj['block_hash'],
                     current_state_balances=obj['current_state_balances'])
    return obj


def json_transaction_decoder(obj):
    """
    Deserialize json object to Transaction object
    :param obj: <json object>
    :return: <Transaction>
    """
    if 'to_address' in obj and 'value' in obj:
        return Transaction(from_address=obj['from_address'],
                           to_address=obj['to_address'],
                           value=int(obj['value']),
                           fee_percent=obj['fee_percent'],
                           sender_pub_key=tuple(int(x) for x in obj['sender_pub_key']),
                           sender_signature=tuple(int(x) for x in obj['sender_signature']),
                           date_received=float(obj['date_received']),
                           mined_in_block_index=obj['mined_in_block_index'],
                           paid=obj['paid'],
                           date_added_to_block=obj['date_added_to_block'],
                           date_created=obj['date_created'],
                           transaction_hash=obj['transaction_hash'])
    return obj
