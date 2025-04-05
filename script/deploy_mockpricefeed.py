# This file will deploy the mock price feed
from src.mocks import mock_v3_aggregator
from moccasin.boa_tools import VyperContract

STARTING_DECIMAL = 8
STARTING_PRICE = int(2000e8)


def deploy_feed() -> VyperContract:
    return mock_v3_aggregator.deploy(STARTING_DECIMAL, STARTING_PRICE)

# This returns vypercontract as the moccasin config need it.
# It will use what this function returns as the contract if it is not on sepolia
def moccasin_main() -> VyperContract:
    return deploy_feed()