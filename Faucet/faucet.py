from Wallet.wallet import *


class Faucet:

    def __init__(self):
        """
        Constructor
        """
        self.config = json.load(open("faucet_config.json", "r"))
        # Init wallet containing address and keys
        self.wallet = Wallet()
        self.wallet.generate_address_randomKey()
        it = iter(self.wallet.addresses)
        self.faucet_address = next(it)
        # set balance
        self.wallet.addresses[self.faucet_address]['balance'] = self.config['max_avail']


    def send_coins(self, to_address, amount=None):
        """
        Sends configurable amount of coins to the provided address
        :param to_address:
        :return:
        """
        from_address = self.faucet_address
        if amount is None:
            amount = self.config['coins_to_send']
        result, reason, transactions = self.wallet.generate_transaction(from_address, to_address, amount)
        if result:
            send_result, transaction_hash = self.wallet.send_transactions(transactions)
            if send_result:
                return True, transaction_hash
            else:
                return False, transaction_hash
        else:
            print("Transaction can not be completed: " + reason)
            return False