from scripts.help_scripts import get_account, get_test_account1, get_test_account2

from brownie import accounts, TitleToken, PoYToken, TokenTransfer, PoYCoin


def deploy_NFT():
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


def deploy_Coin():
    account = get_account()
    print(account)

    coin = PoYCoin.deploy({"from": account})
    coin.wait(1)
    print(f"PoY Contract deployed at {coin.address}")


def main():
    deploy_Coin()
