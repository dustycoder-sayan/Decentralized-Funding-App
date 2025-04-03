from brownie import accounts, network, config, MockV3Aggregator

DEVELOPMENT_ENVIRONMENTS = [
    "development",
    "ganache-local"
]

FORKED_ENVIRONMENTS = [
    "mainnet-fork-dev"
]

AGGREGATOR_DECIMALS = 8
AGGREGATOR_STARTING_ANSWER = 20_000_000_000

def get_account():
    if network.show_active() in DEVELOPMENT_ENVIRONMENTS or network.show_active() in FORKED_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

def get_pricefeed_address():
    if network.show_active() not in DEVELOPMENT_ENVIRONMENTS:
        return config["networks"][network.show_active()]["pricefeed"]
    return deploy_mocks()

def deploy_mocks():
    if len(MockV3Aggregator) > 0:
        return MockV3Aggregator[-1]
    return MockV3Aggregator.deploy(
        AGGREGATOR_DECIMALS, AGGREGATOR_STARTING_ANSWER, 
        {
            "from": get_account()
        }
    )

def get_verify_value():
    return config["networks"][network.show_active()]["verify"]