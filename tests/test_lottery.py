from brownie import Lottery, accounts, config, network
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    # expected about 0.041 ETH at current prices
    # 41000000000000000
    assert lottery.getEntranceFee() > 40000000000000000
    assert lottery.getEntranceFee() < 42000000000000000
    # OR
    assert lottery.getEntranceFee() > Web3.toWei(0.040, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.042, "ether")
