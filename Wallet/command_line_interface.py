from cmd import Cmd
from pprint import pprint


class BeerPrompt(Cmd):


    def __init__(self, wallet):
        """
        Constructor
        :param wallet: <Wallet> wallet we are going to work with
        """
        super().__init__()
        self.wallet = wallet
        self.prompt = '> '
        self.cmdloop('Starting prompt...')


    def do_buy(self, args):
        """
        Gets coins from faucet to the provided address
        """
        if not self._check_args(args):
            return
        else:
            self.wallet.get_coins_from_faucet(args)

    def do_send(self, args):
        """
        Sends specified value from the specified address to the specified address
        """
        if not self._check_args(args):
            return
        else:
            params = args.split()
            result, reason, transactions = self.wallet.generate_transaction(from_address=params[0],
                                                            to_address=params[1],
                                                            value=params[2])
            if result:
                self.wallet.send_transactions(transactions)


    def do_generate(self, args):
        """
        Generates address by the provided private key.
        If no key is provided - generates address with random key.
        """
        if not len(args) == 0:
            self.wallet.generate_address(args)
        else:
            self.wallet.generate_address_randomKey()


    def do_balance(self, args):
        """
        Shows balance of the specified address
        """
        if not self._check_args(args):
            return
        else:
            self.wallet.update_balances()
            balance = self.wallet.addresses.get(args, -1)['balance']
            if balance == -1:
                print("Address not found.")
            else:
                print(balance)


    def do_address_info(self, args):
        """
        Prints address info
        """
        if not self._check_args(args):
            return
        else:
            pprint(self.wallet.addresses.get(str(args), "Not Found."))


    def do_addresses(self, args):
        """
        Prints all addresses in the wallet
        """
        pprint(self.wallet.addresses)


    def do_wallet_info(self, args):
        """
        Prints wallet information
        """
        pprint(vars(self.wallet))


    def _check_args(self, args):
        """
        Checks if parameters are provided.
        """
        if len(args) == 0:
            print("No parameters provided.")
            return False
        else:
            return True
