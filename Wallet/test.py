from Wallet.wallet import *

w = Wallet()

def test_receive_send(w):
    w.generate_address_randomKey()
    w.generate_address("umpalumpa")
    it = iter(w.addresses)
    from_address, to_address = next(it), next(it)
    w.get_coins_from_faucet(from_address)
    # transaction has to be mined before update of balances
    w.update_balances()
    result, reason, transactions = w.generate_transaction(from_address, to_address, 5)
    if result:
        send_result, transaction_hash = w.send_transactions(transactions)
        if send_result:
            print(transaction_hash)
    # transaction has to be mined before update of balances
    w.update_balances()
    print("success")


def test_generate():
    w.generate_address("umpalumpa")

def test_generate_random():
    w.generate_address_randomKey()


if __name__ == '__main__':
    # test_generate()
    # test_generate_random()
    test_receive_send(w)
    print(w.addresses[next(iter(w.addresses))])
