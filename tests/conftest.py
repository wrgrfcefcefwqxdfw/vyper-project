import pytest
from script.deploy import deploy_coffee
from script.deploy_mockpricefeed import deploy_feed
from moccasin.config import get_active_network
from eth_utils import to_wei
import boa

# Set send value to 1 ether
SEND_VALUE = to_wei(1, "ether")

# Get default account of the active network to know who is the one deploying the contract
@pytest.fixture(scope="session")
def default_account():
    return get_active_network().get_default_account()

# This one is not as important so we can run it just once
@pytest.fixture(scope="session")
def eth_usd():
    return deploy_feed()

# This is because the deploy_coffee function needs a price feed in order to run
# For unit test, we want keep coffee as function as we want to test the contract from scratch between test runs
@pytest.fixture(scope="function")
def coffee(eth_usd):
    return deploy_coffee(eth_usd)

# funding the coffee contract as OWNER or the default account which is owner
@pytest.fixture(scope="function")
def fund_coffee(coffee, default_account):
    boa.env.set_balance(default_account.address, SEND_VALUE)
    with boa.env.prank(default_account.address):
        coffee.fund(value=SEND_VALUE)
    
    return coffee
    

