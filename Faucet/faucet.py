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
        self.sent_transactions = {}


    def send_coins(self, to_address, amount=None):
        """
        Sends configurable amount of coins to the provided address
        :param to_address:
        :return:
        """
        from_address = self.faucet_address
        if amount is None:
            amount = self.config['coins_to_send']
        transactions = self.generate_transaction(from_address, to_address, amount)
        send_result, msg = self.wallet.send_transactions(transactions)
        if send_result:
            return True, msg
        else:
            return False, msg


    def generate_transaction(self, from_address, to_address, value):
        """
        Generates transaction from the provided data
        :param from_address: <str>
        :param to_address: <str>
        :param value: <int>
        :return: <Transaction[]>
        """
        transactions = []
        reason = ""
        new_transaction = Transaction(from_address=from_address,
                                      to_address=to_address,
                                      value=value,
                                      sender_pub_key=self.wallet.addresses[from_address]['public_key'],
                                      sender_signature="",
                                      date_created=time.time(),
                                      faucet_transaction=True)
        self.sign_transaction(new_transaction)
        transactions.append(new_transaction)
        self.sent_transactions[new_transaction.transaction_hash]
        return transactions


    def sign_transaction(self, transaction):
        """
        Signs transaction using owner's private key
        :param transaction: <Transaction>
        """
        try:
            address = transaction.from_address
            private_key = self.wallet.addresses[address]['private_key']
            transaction.sign_transaction(private_key)
        except Exception as ex:
            print("Error signing transaction from address: " + address + " " + str(ex))


    def validate_transaction(self, pub_key, transaction_hash, signature):
        """
        Validates if transactions data is valid and if it exist in already sent transactions,
        if it does it removes it and returns result
        :param pub_key: <tuple<int,int>>
        :param transaction_hash: <int>
        :param signature: <tuple<int,int>>
        :return:
        """
        if not CryptoUtils.verify_transaction(pub_key, transaction_hash, signature):
            return False
        if transaction_hash not in self.sent_transactions:
            return False
        del self.sent_transactions[transaction_hash]
        return True

