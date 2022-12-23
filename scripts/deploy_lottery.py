from brownie import Lottery, network, config
from scripts.helpful_scripts import get_account, get_contract


def deploy_lottery():
    account = get_account()
    # we add the .address at the end to return the address, otherwise it would return the whole contract
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        {"from": account},
        # get verify key from config. if it doesn't exist, return false
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery has started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1 * 10**8
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    # time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
