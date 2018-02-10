class Node:

    def __init__(self,
                 peers,
                 blocks,
                 pending_transactions,
                 balances,
                 difficulty,
                 mining_jobs):
        """
        Constructor
        :param peers: <str[]>
        :param blocks: <dict[]> Block
        :param pending_transactions: <dict[]> Transaction
        :param balances: <dict> address => number
        :param difficulty: <int>
        :param mining_jobs: <dict> address => Block
        """
        self.peers = peers
        self.blocks = blocks
        self.pending_transactions = pending_transactions
        self.balances = balances
        self.difficulty = difficulty
        self.mining_jobs = mining_jobs
