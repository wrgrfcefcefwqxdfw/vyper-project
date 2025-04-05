import pytest
from moccasin.config import get_active_network
import boa
from script.deploy import deploy_coffee
from tests.conftest import SEND_VALUE

# Mark this test to only run on staging or live environments (not local unit tests)
@pytest.mark.staging
@pytest.mark.ignore_isolation
def test_can_fund_and_withdraw_live():
    # 🔷 Get the active network configuration (e.g. rpc, deployed contracts, addresses)
    active_network = get_active_network()
    
    # 🔷 Get the address or mock for the price feed contract from the network manifest
    price_feed = active_network.manifest_named("price_feed")
    
    # 🔷 Deploy the Coffee contract using the given price feed
    # This function is defined in your deploy script and handles deployment logic
    coffee = deploy_coffee(price_feed)
    
    # 🔷 Call the fund() function on the deployed contract, sending SEND_VALUE worth of ETH
    coffee.fund(value=SEND_VALUE)
    
    # 🔷 After funding, check how much the current account (boa.env.eoa) has funded
    amount_funded = coffee.address_to_amount_funded(boa.env.eoa)
    
    # 🔷 Assert that the amount funded matches the value we sent in
    assert amount_funded == SEND_VALUE

    # 🔷 Call withdraw() to remove all funds from the contract to the owner's account
    coffee.withdraw()
    
    # 🔷 After withdrawal, assert that the contract balance is now 0
    assert boa.env.get_balance(coffee.address) == 0