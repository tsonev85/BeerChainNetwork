from sbcapi.model import *

class Node:

    def __init__(self,
                 node_identifier,
                 peers=None,
                 balances=None,
                 block_chain=None,
                 mining_jobs=None):
        """
        Constructor
        :param peers: <str[]>
        :param block_chain: <dict> BlockChain
        :param balances: <dict> address => number
        :param mining_jobs: <dict> address => Block
        :param new_block: <dict> Block
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
        self.balances = balances
        self.mining_jobs = mining_jobs
        self.new_block = self.get_new_block()

    def add_peer(self, peer):
        self.peers.append(peer)

    def add_transaction(self, transaction):
        if not transaction.is_transaction_valid():
            print("Transaction is not valid.")
            return False
        if not self.new_block:
            self.new_block = self.get_new_block()
        self.new_block.transactions.append(transaction)
        return True

    def remove_transaction(self):
        # TODO
        pass

    def update_balance(self):
        # TODO
        pass

    def get_mining_job(self, miner_address):
        """
        Returns job for the miner hash, difficulty
        :param miner_address: <str> Address of miner
        :return: <tuple<str><int>>
        """
        tmp_block = self.new_block
        tmp_block.mined_by = miner_address
        self.mining_jobs[miner_address] = tmp_block
        return tmp_block.calculate_block_hash(), tmp_block.difficulty

    def mined_hash(self, mined_hash, miner_address):
        # TODO
        # validate
        mined_block = self.mining_jobs[miner_address]
        mined_block.miner_hash = mined_hash
        self.block_chain.add_to_blockchain(mined_block)
        # broadcast to peers
        pass

    def replace_chain(self, new_chain):
        self.block_chain.replace_chain(new_chain)

    def get_new_block(self):
        return Block(index=len(self.block_chain.blocks),
                     prev_block_hash=self.block_chain.blocks[len(self.block_chain.blocks) - 1],
                     date_created=time.time(),
                     mined_by="",
                     difficulty=self.block_chain.difficulty)
