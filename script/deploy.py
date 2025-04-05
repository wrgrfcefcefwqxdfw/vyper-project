from src import buy_me_a_coffee
from script.deploy_mockpricefeed import deploy_feed
from moccasin.config import get_active_network
from moccasin.boa_tools import VyperContract

def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    print("Deploying....")
    coffee_contract: VyperContract = buy_me_a_coffee.deploy(price_feed)
    
    # Verification
    active_network = get_active_network()
    if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
        result = active_network.moccasin_verify(coffee_contract)
        result.wait_for_verification()
        
    return coffee_contract
    
    # How do we test this on a pyevm network
    # We are going to deploy the aggregatorv3 contracts ourselves

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    # This price_feed references the one inside the moccasin.toml file
    # This line is so that we dont need conditionals to detect if it is sepolia or not to use the real price feed address
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    # If it is on network sepolia, it will use the price feed address inside moccasin.toml
    print(f"On network {active_network.name}, using price feed at {price_feed.address}")
    
    return deploy_coffee(price_feed)

    # price_feed: VyperContract = deploy_feed()
    # coffee_contract = buy_me_a_coffee.deploy(price_feed)
    # print(f"Coffee contract deployed at {coffee_contract.address}")
