from Wallet.wallet import *


if __name__ == '__main__':
    wallet = Wallet()

    update_balance = \
        threading.Thread(name="Update_Balance_Thread", target=wallet.update_balances_job(update_every_seconds=7))
    update_balance.start()

    # wallet_ui = threading.Thread(name="Wallet_UI_Thread", target=)
    # wallet_ui.start()