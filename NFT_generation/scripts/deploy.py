from scripts.help_scripts import get_account
from brownie import TitleToken


def deploy():
    account = get_account()
    title = TitleToken.deploy({"from": account})
    print(f"Contract deployed at {title.address}")


def main():
    deploy()
