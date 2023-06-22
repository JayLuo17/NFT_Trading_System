import pytest
from brownie import network, PoYToken, TokenTransfer
from scripts.deploy import deploy
from scripts.transfer import register, addFund, transferFund
from scripts.help_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_test_account1, get_test_account2

def test_transfer():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing...")

    deploy()
    owner = get_account()
    receiver1 = get_test_account1()
    receiver2 = get_test_account2()

    # Get the latest deployment
    TokenContract = TokenTransfer[-1]
    PoY = PoYToken[-1]

    # Register both accounts
    register(receiver1, TokenContract, owner)
    register(receiver2, TokenContract, owner)

    # Test fund function
    fund_Amount = 7
    original_amount = TokenContract.TokenBalance(receiver1.address)
    addFund(receiver1, TokenContract, owner, fund_Amount)
    afterFund_amount = TokenContract.TokenBalance(receiver1.address)

    assert(original_amount + fund_Amount == afterFund_amount)
    assert(TokenContract.TokenBalance(receiver1.address) - fund_Amount == TokenContract.TokenBalance(receiver2.address))

    # Test transfer function
    transfer_Amount = 3
    original_amount1 = TokenContract.TokenBalance(receiver1.address)
    original_amount2 = TokenContract.TokenBalance(receiver2.address)
    transferFund(TokenContract, PoY, receiver1, receiver2, transfer_Amount)
    afterTransfer_amount1 = TokenContract.TokenBalance(receiver1.address)
    afterTransfer_amount2 = TokenContract.TokenBalance(receiver2.address)
    
    assert(original_amount1 - transfer_Amount == afterTransfer_amount1)
    assert(original_amount2 + transfer_Amount == afterTransfer_amount2)
    assert(TokenContract.TokenBalance(receiver1.address) - fund_Amount + 2*transfer_Amount == TokenContract.TokenBalance(receiver2.address))

    
