from brownie import accounts, network, config, MockV3Aggregator, Contract

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):

    # if index is passed:
    if index:
        return accounts[index]

    # if id is passed
    if id:
        return accounts.load(id)

    # nothing is passed
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


# maps the contract names to their type
contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config if defined, otherwise it will deploy a mock version of that contract, and return that mock contract.

    Args:
        contract_name (string)

    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract. This could be either a mock or the 'real' contract on a live network.
    """
    # it goes to the contract_to_mock mapping, and gets the contract type from it's name. Ex: for the name = "eth_usd_price_feed" the type is MockV3Aggregator
    contract_type = contract_to_mock[contract_name]
    # we only need to deploy a mock if we are in a local (development) blockchain
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # if no MockV3Aggregator has been deployed, let's deploy one
        # it's equivalent to doing MockV3Aggregator.length
        if len(contract_type) <= 0:
            deploy_mocks()
        # get the most recent contract deployed. It's the same as doing: MockV3Aggregator[-1]
        contract = contract_type[-1]
    # else, if we are on a testnet/mainnet (forked local environment) we don't need to deploy a mock
    else:

        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 2000 * 10**8


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print("Deployed!")
