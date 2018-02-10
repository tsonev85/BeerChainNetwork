class MiningJob:

    def __init__(self,
                 index,
                 transaction_hash,
                 prev_block_hash,
                 transactions,
                 exp_reward,
                 difficulty):
        """
        Constructor
        :param index: <int>
        :param transaction_hash: <hex>
        :param prev_block_hash: <hex>
        :param transactions: <dict[]> Transaction
        :param exp_reward: <int>
        :param difficulty: <int>
        """
        self.index = index
        self.transaction_hash = transaction_hash
        self.prev_block_hash = prev_block_hash
        self.transactions = transactions
        self.exp_reward = exp_reward
        self.difficulty = difficulty
