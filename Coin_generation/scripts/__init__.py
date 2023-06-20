import pytest
from web3 import Web3

# Replace these with your contract's ABI and Address
CONTRACT_ABI = '[...]'  # Contract ABI
CONTRACT_ADDRESS = '0xYourContractAddress'  # Contract address

# We'll use Ganache for our tests, make sure it's running on this port
GANACHE_URL = "HTTP://127.0.0.1:7545"

@pytest.fixture
def account_0():
    # Replace with one of your Ethereum accounts
    return "0xYourAccount0"

@pytest.fixture
def account_1():
    # Replace with one of your Ethereum accounts
    return "0xYourAccount1"

@pytest.fixture
def setup_contract():
    web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    # Check connection
    assert web3.isConnected()

    # Set default account
    web3.eth.defaultAccount = web3.eth.accounts[0]

    # Instantiate contract
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

    return web3, contract

def test_total_supply(setup_contract):
    web3, contract = setup_contract

    total_supply = contract.functions.totalSupply().call()
    print("Total Supply: ", total_supply)

    assert isinstance(total_supply, int)

def test_register_address(setup_contract, account_1):
    web3, contract = setup_contract

    tx_hash = contract.functions.registerAddress(account_1).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    assert tx_receipt.status == 1

    # Check registration
    is_registered = contract.functions.isRegistered(account_1).call()
    assert is_registered == True

def test_token_balance(setup_contract, account_1):
    web3, contract = setup_contract

    balance = contract.functions.myTokenBalance(account_1).call()
    print("Account Balance: ", balance)

    assert isinstance(balance, int)

# Repeat for each function you want to test
