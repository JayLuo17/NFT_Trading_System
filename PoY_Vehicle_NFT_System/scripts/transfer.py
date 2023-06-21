from brownie import PoYToken, TokenTransfer, TitleToken, network
from scripts.help_scripts import get_account, get_test_account1, get_test_account2
from web3 import Web3


def register(account, contract, owner):
    if not contract.isRegistered(account.address):
        tx = contract.registerAddress(account.address, {"from": owner})
        tx.wait(1)
        tx = contract.issueInitialFund(account.address, {"from": owner})
        tx.wait(1)
        print(f"Successfully registered {account.address}...")
    else:
        print(f"Account {account.address} already registered...")

def addFund(account, contract, owner, amount):
    tx = contract.issueFund(account.address, amount, {"from": owner.address})
    tx.wait(1)
    print(f"Successfully add fund = {amount} to {account.address}...")

def transferFund(contract, coin, sender, receiver, amount):
    if contract.TokenBalance(sender.address) < amount:
        print(contract.TokenBalance(sender.address))
        print("Insufficient fund in sender!")
    else:
        coin.approve(sender.address, amount, {"from": sender})
        coin.transferFrom(sender.address, receiver.address, amount, {"from": sender})

def main():
    owner = get_account()
    receiver1 = get_test_account1()
    receiver2 = get_test_account2()

    # Get the latest deployment
    TokenContract = TokenTransfer[-1]
    PoY = PoYToken[-1]
    print(f"The initial supply for each user is: {TokenContract.InitialSupply()}")

    # Register both accounts
    register(receiver1, TokenContract, owner)
    register(receiver2, TokenContract, owner)

    # Run add fund and transfer fund functions
    addFund(receiver1, TokenContract, owner, 7)
    transferFund(TokenContract, PoY, receiver1, receiver2, 3)
    
    # Print out the necessary results
    owner_amount = TokenContract.TokenBalance(owner.address)
    sender_amount = TokenContract.TokenBalance(receiver1.address)
    receiver_amount = TokenContract.TokenBalance(receiver2.address)
    contract_amount = TokenContract.TokenBalance(TokenContract.address)
    PoY_amount = TokenContract.TokenBalance(PoY.address)
    print(
        f"PoY has: {PoY_amount}; Transfer Contract has {contract_amount};\
        Owner has {owner_amount} Sender has {sender_amount}; Receiver has {receiver_amount}"
    )

