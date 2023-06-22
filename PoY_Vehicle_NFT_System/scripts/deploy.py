from scripts.help_scripts import get_account
from brownie import TitleToken, PoYToken, TokenTransfer
from web3 import Web3


def deploy():
    account = get_account()
    print(account)

    title = TitleToken.deploy({"from": account})
    print(f"Contract deployed at {title.address}")

    PoY = PoYToken.deploy({"from": account})

    TT = TokenTransfer.deploy(PoY.address, {"from": account})
    tx = PoY.transfer(TT.address, PoY.totalSupply() - 10**10, {"from": account})
    tx.wait(1)
    print(f"PoY deployed at {PoY.address}")
    print(f"Transfer Contract deployed at {TT.address}")


def main():
    deploy()
