import pytest
import random
from brownie import network, PoYToken, TokenTransfer, PoYCoin
from scripts.deploy import deploy_NFT, deploy_Coin
from scripts.transfer import register, addFund, transferFund
from scripts.help_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_test_account1,
    get_test_account2,
)


def test_coinGen():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing...")
    deploy_Coin()
    owner = get_account()
    receiver = get_test_account1()
    pool = get_test_account2()

    coin = PoYCoin[-1]

    # Test the segment generate function
    imgNums = [random.randint(1, 1000) for _ in range(random.randint(50, 100))]
    parts = random.randint(1, 20)

    # The length of each segment is the ceil of the division
    segLen = (
        len(imgNums) // parts
        if len(imgNums) % parts == 0
        else len(imgNums) // parts + 1
    )

    segments = coin.divideImageNums(imgNums, parts)  # Expect the length to be three
    assert len(segments[0]) == segLen
    assert len(segments) == parts

    # Test the base calculation function
    coinNum = random.randint(50, 100000)
    base = random.randint(2, 20)
    coeff = coin.toBaseY(coinNum, base)

    totalSum = 0
    for i, c in enumerate(coeff):
        totalSum += c * (base**i)
    assert totalSum == coinNum

    # Test the mintCoin function
    coin.mintCoin(receiver, [0, 0, 0], 1, {"from": owner})
    assert coin.coinIds(0) == 1
    assert coin.coinAds(0) == receiver

    coinCount = random.randint(1, 20)
    for i in range(coinCount):
        coin.mintCoin(pool, [0, 0, i], i, {"from": owner})
        assert coin.coinIds(i + 1) == i


def test_coinGen_all():
    deploy_Coin()
    owner = get_account()
    receiver = get_test_account1()
    pool = get_test_account2()
    coin = PoYCoin[-1]

    # Test the mint function, can't be too large for local pc
    imgNums = [random.randint(1, 1000) for _ in range(random.randint(50, 100))]
    X, Y = 3, 2
    supply = 6
    coin.mint(receiver, pool, imgNums, supply, X, Y, {"from": owner})
    assert coin._coinIdCounter() <= X**Y - 1
    assert coin._totalVal() == X**Y - 1


def test_transfer():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing...")

    deploy_NFT()
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

    assert original_amount + fund_Amount == afterFund_amount
    assert TokenContract.TokenBalance(
        receiver1.address
    ) - fund_Amount == TokenContract.TokenBalance(receiver2.address)

    # Test transfer function
    transfer_Amount = 3
    original_amount1 = TokenContract.TokenBalance(receiver1.address)
    original_amount2 = TokenContract.TokenBalance(receiver2.address)
    transferFund(TokenContract, PoY, receiver1, receiver2, transfer_Amount)
    afterTransfer_amount1 = TokenContract.TokenBalance(receiver1.address)
    afterTransfer_amount2 = TokenContract.TokenBalance(receiver2.address)

    assert original_amount1 - transfer_Amount == afterTransfer_amount1
    assert original_amount2 + transfer_Amount == afterTransfer_amount2
    assert TokenContract.TokenBalance(
        receiver1.address
    ) - fund_Amount + 2 * transfer_Amount == TokenContract.TokenBalance(
        receiver2.address
    )
