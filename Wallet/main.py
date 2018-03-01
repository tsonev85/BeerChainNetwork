from Wallet.wallet import *
from Wallet.command_line_interface import *


if __name__ == '__main__':

    wallet = Wallet()

    # to enable background update of balances uncomment this
    # update_balance = \
    #     threading.Thread(name="Update_Balance_Thread", target=wallet.update_balances_job(update_every_seconds=7))
    # update_balance.setDaemon(True)
    # update_balance.start()

    command_prompt = threading.Thread(name="Beer_prompt_thread", target=BeerPrompt(wallet))
    command_prompt.setDaemon(True)
    command_prompt.start()
