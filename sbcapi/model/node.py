from sbcapi.model import *
from sbcapi.utils.ArgParser import *
import copy


class Node(object):

    def __init__(self,
                 node_identifier,
                 peers=None,
                 block_chain=None,
                 mining_jobs=None):
        """
        Constructor
        :param peers: <str[]>
        :param block_chain: <BlockChain>
        :param mining_jobs: <dict> address => Block
        """
        if block_chain is None:
            block_chain = BlockChain()
        if not mining_jobs:
            mining_jobs = {}
        if not peers:
            peers = []
        self.node_identifier = node_identifier
        self.peers = peers
        self.block_chain = block_chain
        self.mining_jobs = mining_jobs
        self.new_block = self.get_new_block()

    def add_peer(self, peer):
        """
        Adds new peer
        :param peer: <str> new peer
        """
        # TODO add validation of peer format
        self.peers.append(peer)

    def add_to_pending_transactions(self, transaction):
        """
        Validates transaction and adds it to pending transaction of self.new_block
        :param transaction: <Transaction> Transaction to be added to pending
        :return: <bool> Result of action
        """

        if ArgParser.get_args().debug:
            self.new_block.transactions.append(transaction)
            return True

        if not bool(transaction):
            "Transactions is empty"
            return False
        if not transaction.is_transaction_valid():
            print("Transaction is not valid.")
            return False
        if not self.check_balance(transaction.from_address, transaction.value):
            return False
        if not self.new_block:
            self.new_block = self.get_new_block()
        self.new_block.transactions.append(transaction)
        return True

    def add_new_block(self, new_block):
        """
        Validates and adds new block to block chain
        :param new_block: <Block> New block
        :return: <bool> result of operation
        """
        if not Block.is_block_valid(new_block, self.block_chain.blocks[-1]):
            print("New block is not valid")
            return False
        self.confirm_mined_transactions(new_block)
        self.update_balance(new_block)
        self.block_chain.blocks.append(new_block)
        if not BlockChain.valid_chain(self.block_chain):
            print("Blockchain became invalid after add of new block")
            return False
        future_block = self.get_new_block(self.new_block.transactions)
        self.new_block = future_block
        return True

    def add_block_from_miner(self, mined_block):
        """
        Validates and adds new mined block from miner to block chain
        :param mined_block: <Block>
        :return: <bool> Result of operation
        """
        job_block = self.mining_jobs[mined_block['miner_address']]
        if not ArgParser.get_args().debug:
            if job_block is None:
                print("Mining job not found.")
                return False
            if job_block.block_hash != mined_block['original_hash']:
                print("Original hash mismatch")
                return False
            if job_block.difficulty != mined_block['difficulty']:
                print("Difficulty mismatch")
                return False
        job_block.mined_by = mined_block['miner_name']
        job_block.miner_address = mined_block['miner_address']
        job_block.miner_hash = mined_block['mined_hash']
        job_block.nonce = mined_block['nonce']
        if not self.add_new_block(job_block):
            print("Mined block validation failed")
            return False
        return True

    def confirm_mined_transactions(self, block):
        """
        Receives a block that is to be added to the blockchain, loops through its transactions(at this point,
        these transaction should be from mined block and they should be paid(mined)) and removes them, if present,
        from the pending transactions of the template block(self.new_block)
        :param block:
        :return:
        """
        for transaction in block.transactions:
            for unpaid_transaction in self.new_block.transactions:
                if unpaid_transaction.transaction_hash == transaction.transaction_hash:
                    self.new_block.transactions.remove(unpaid_transaction)
                    transaction.paid = True

    def remove_transaction(self):
        # TODO
        pass

    def update_balance(self, new_block):
        """
        Updates the current state of balances inside new_block
        based on passed and validated transactions in new_block
        :param new_block: <block>
        """
        for transaction in new_block.transactions:
            sender_address = transaction.from_address
            receiver_address = transaction.to_address
            value = transaction.value
            # we assume all validation and balance checks have been passed since this is already mined block
            new_block.current_state_balances[receiver_address] = \
                new_block.current_state_balances.get(receiver_address, 0) + value
            new_block.current_state_balances[sender_address] = \
                new_block.current_state_balances.get(sender_address, 0) - value

    def check_balance(self, address, value):
        """
        Checks if the provided account has sufficient funds.
        :param address: <str>
        :param value: <int>
        :return: <bool>
        """
        if not self.block_chain.blocks[-1].current_state_balances.get(address, 0) >= value:
            print("Address " + address + " does not have enough balance.")
            return False
        return True

    def get_mining_job(self, data):
        """
        Returns job for the miner hash, difficulty
        :param data: <dict> Data
        :return: <tuple<str><int>>
        """
        tmp_block = copy.deepcopy(self.new_block)
        tmp_block.mined_by = data['miner_name']
        tmp_block.miner_address = data['minerAddress']
        tmp_block.block_hash = Block.calculate_block_hash(tmp_block)
        self.mining_jobs[data['minerAddress']] = tmp_block
        return tmp_block.block_hash, tmp_block.difficulty

    def replace_chain(self, new_chain):
        """
        Replaces node block chain with new one
        :param new_chain: <BlockChain>
        :return: <bool>
        """
        return self.block_chain.replace_chain(new_chain.blocks)

    def get_new_block(self, transactions=None):
        """
        Returns a new block to be mined,
        all pending transactions will be added to this block
        :return:
        """
        return Block(index=len(self.block_chain.blocks),
                     prev_block_hash=self.block_chain.blocks[len(self.block_chain.blocks) - 1].miner_hash,
                     transactions=transactions,
                     date_created=time.time(),
                     miner_name="",
                     miner_address="",
                     difficulty=self.block_chain.difficulty)

    def broadcast_to_peers(self):
        pass
