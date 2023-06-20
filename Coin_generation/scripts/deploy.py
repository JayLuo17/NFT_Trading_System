from scripts.help_scripts import get_account
from brownie import PoYToken, TokenTransfer


def deploy():
    account = get_account()
    PoY = PoYToken.deploy({"from": account})
    TT = TokenTransfer.deploy(PoY.address, {"from": account})
    print(f"PoY deployed at {PoY.address}")
    print(f"Transfer Contract deployed at {TT.address}")


def main():
    deploy()
