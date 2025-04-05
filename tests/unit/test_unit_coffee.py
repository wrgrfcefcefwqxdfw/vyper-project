from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE

# Generate a non owner user to test only owner can do certain functions
RANDOM_USER = boa.env.generate_address("non-owner")

def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0
    
def test_price_feed_is_correct(coffee, eth_usd):
    # Remember eth_usd returns a vypercontract
    assert coffee.PRICE_FEED() == eth_usd.address
    
def test_starting_values(coffee, default_account):
    # This is cause in our contract it is in we put 18 zeros after 5, so convert to wei
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == default_account.address

# testing for reverts, since if we dont supply enough eth it will revert due to the assert in the vyper contract
def test_fund_fails_if_not_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()
        
def test_fund_with_money(coffee, default_account):
    # Set the ETH balance of the default account to SEND_VALUE (1 ETH) in the simulated Boa environment
    # This simulates giving the account ETH before making a transaction    
    boa.env.set_balance(default_account.address, SEND_VALUE)
    coffee.fund(value=SEND_VALUE)
    funder = coffee.funders(0)
    assert funder == default_account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE
    
def test_non_owner_cannot_withdraw(fund_coffee):
    # Give the default account ETH in the test environment to fund the contract
    # boa.env.set_balance(default_account.address, SEND_VALUE)
    # coffee.fund(value=SEND_VALUE)
    
    # Use `boa.prank()` to impersonate the RANDOM_USER address for this block of code
    # This allows us to test what happens when a non-owner tries to call `withdraw()`
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            fund_coffee.withdraw()


def test_owner_can_withdraw(fund_coffee):
    with boa.env.prank(fund_coffee.OWNER()):
        fund_coffee.withdraw()
        
    assert boa.env.get_balance(fund_coffee.address) == 0
    

def test_multiple_funding(coffee):
    for i in range(10):
        USER = boa.env.generate_address(i)
        boa.env.set_balance(USER, SEND_VALUE)
        with boa.env.prank(USER):
            coffee.fund(value=SEND_VALUE)
            
    starting_fund_balance = boa.env.get_balance(coffee.address)        
    starting_owner_balance = boa.env.get_balance(coffee.OWNER())
    assert boa.env.get_balance(coffee.address) == to_wei(10, "ether")
    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()
                
    assert boa.env.get_balance(coffee.address) == 0
    assert starting_fund_balance + starting_owner_balance == boa.env.get_balance(coffee.OWNER())

# def test_withdraw_from_multiple_funders(fund_coffee):
#     number_of_funders = 10
#     for i in range(number_of_funders):
#         user = boa.env.generate_address(i)
#         boa.env.set_balance(user, SEND_VALUE * 2)
#         with boa.env.prank(user):
#             fund_coffee.fund(value=SEND_VALUE)
#     starting_fund_me_balance = boa.env.get_balance(fund_coffee.address)
#     starting_owner_balance = boa.env.get_balance(fund_coffee.OWNER())
#     assert "openis" == 'pp'

#     with boa.env.prank(fund_coffee.OWNER()):
#         fund_coffee.withdraw()

#     assert boa.env.get_balance(fund_coffee.address) == 0
#     assert starting_fund_me_balance + starting_owner_balance == boa.env.get_balance(
#         fund_coffee.OWNER()
#     )