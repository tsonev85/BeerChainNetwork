from sbcapi.utils import *
import binascii
import threading


class Wallet(object):


    def __init__(self):
        """
        Constructor
        """
        cfg = json.load(open("wallet_config.json", "r"))
        self.addresses = {}
        self.node_address = cfg['node_url']
        self.faucet_address = cfg['faucet_url']
        self.semaphore = threading.BoundedSemaphore()


    def generate_address_randomKey(self):
        """
        Generates address with random key
        :return:
        """
        private_key = CryptoUtils.generate_random_private_key()
        self.generate_address(private_key)


    def generate_address(self, private_key):
        """
        Generates address from the provided private_key
        :param private_key: <str>
        """
        words, seed = CryptoUtils.create_mnemonic_key(private_key)
        private_key_to_hex = CryptoUtils.generate_private_key(seed)
        public_key = CryptoUtils.generate_public_key(private_key_to_hex)
        public_key_compressed = CryptoUtils.compress_public_key(public_key)
        address = CryptoUtils.generate_address(public_key)
        self.addresses[address] = {
            'owner_key': private_key,
            'private_key': private_key_to_hex,
            'mnemonic_words': words,
            'public_key': public_key,
            'public_key_compressed': public_key_compressed,
            'balance': 0
        }


    def get_coins_from_faucet(self, to_address):
        """
        Gets coins from the faucet to the provided address
        :param to_address: <str>
        """
        get_coins_from_faucet(self.faucet_address, to_address)


    def generate_transaction(self, from_address, to_address, value):
        """
        Generates transaction from the provided data
        :param from_address: <str>
        :param to_address: <str>
        :param value: <int>
        :return: <<bool>, <str>, <Transaction[]>>
        """
        self.semaphore.acquire(timeout=2)
        try:
            transactions = []
            reason = ""
            if not self.has_enough_balance(from_address, value):
                reason = "Insufficient balance. Transaction can not be completed."
                print(reason)
                return False, reason, transactions
            new_transaction = Transaction(from_address=str(from_address),
                                          to_address=str(to_address),
                                          value=int(value),
                                          sender_pub_key=self.addresses[from_address]['public_key'],
                                          sender_signature="",
                                          date_created=time.time())
            self.sign_transaction(new_transaction)
            transactions.append(new_transaction)
            return True, reason, transactions
        finally:
            self.semaphore.release()


    def sign_transaction(self, transaction):
        """
        Signs transaction using owner's private key
        :param transaction: <Transaction>
        """
        try:
            address = transaction.from_address
            private_key = self.addresses[address]['private_key']
            transaction.sign_transaction(private_key)
        except Exception as ex:
            print("Error signing transaction from address: " + address + " " + str(ex))


    def send_transactions(self, transactions):
        """
        Sends transactions to be added to pending transactions in the node
        :param peer: <str>
        :param transactions: <Transaction[]>
        :return: <<bool>, <str>>
        """
        result = send_transactions(self.node_address, transactions)
        if not result.get('successfullyAdded', []):
            return False, "Transaction unsuccessful."
        else:
            return True, result.get('successfullyAdded')[0].get('transaction_hash')


    def update_balances(self):
        """
        Retreives the last block in the block chain and updates the balances of all addresses
        in the wallet based on the current state of balances from retreived block
        """
        self.semaphore.acquire(timeout=2)
        try:
            last_block = get_last_block(self.node_address)
            for address in self.addresses.keys():
                self.addresses[address]['balance'] = \
                    last_block.current_state_balances.get(address, self.addresses[address]['balance'])
        finally:
            self.semaphore.release()


    def update_balances_job(self, update_every_seconds):
        """
        Updates balances in specified period of time
        :param peer: <int> update time
        """
        while True:
            self.update_balances()
            time.sleep(update_every_seconds)


    def has_enough_balance(self, address, value):
        """
        Checks if the provided address has sufficient funds
        :param address: <str> Address to check
        :param value: <int> Value to check
        :return: <bool> Result of operation
        """
        return int(self.addresses[address]['balance']) >= int(value)