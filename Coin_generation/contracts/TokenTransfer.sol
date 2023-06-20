// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// The required functions:
// Record the user's address and the corresponding remaining amount
// Always need to approve the amount first and then let the smart contract move the fund.

contract TokenTransfer is Ownable {
    IERC20 public PoYToken;
    uint256 public InitialSupply = 10 ** 3;

    constructor(address _PoYAddress) public {
        PoYToken = IERC20(_PoYAddress);
    }

    // mapping token address -> staker address -> amount
    // The mapping to store the registartion status of addresses
    mapping(address => bool) public isRegistered;

    function registerAddress(address user_address) public returns (bool) {
        // Check if the user is already registered.
        if (!isRegistered[user_address]) {
            return false;
        } else {
            require(!isRegistered[user_address], "Address already registered");

            // Register the address
            isRegistered[user_address] = true;

            // Give initial amount
            PoYToken.transfer(user_address, InitialSupply);
            return true;
        }
    }

    function totalTokenSupply() external view returns (uint256) {
        return PoYToken.totalSupply();
    }

    function TokenBalance(address account) external view returns (uint256) {
        // Check if the address registered.
        require(!isRegistered[account], "Address already registered");

        return PoYToken.balanceOf(account);
    }

    function transferTokens(
        address recipient,
        uint256 amount
    ) external returns (bool) {
        // Check if the address registered.
        require(isRegistered[msg.sender], "Sender address not registered");
        require(isRegistered[recipient], "Recipient address not registered");

        // Ensure the function caller has enough tokens.
        require(PoYToken.balanceOf(msg.sender) >= amount, "Not enough tokens");
        return PoYToken.transfer(recipient, amount);
    }

    function checkAllowance(
        address owner,
        address spender
    ) external view returns (uint256) {
        // Check if the addresses are registered.
        require(isRegistered[owner], "Owner address not registered");
        require(isRegistered[spender], "Spender address not registered");

        return PoYToken.allowance(owner, spender);
    }

    function approveSpender(
        address spender,
        uint256 amount
    ) external returns (bool) {
        // Check if the addresses are registered.
        require(isRegistered[msg.sender], "Address not registered");
        require(isRegistered[spender], "Spender address not registered");

        // This is typically called from the address that owns token and wants to approve a spender.
        return PoYToken.approve(spender, amount);
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool) {
        // Check if the user is registered
        require(isRegistered[sender], "Sender address not registered");
        if (!isRegistered[recipient]) {
            registerAddress(recipient);
        }

        // This should be called from the address that was approved to spend tokens.
        // Ensure the owner of the tokens has approved for at least `amount` tokens to be spent.
        require(
            PoYToken.allowance(sender, msg.sender) >= amount,
            "Not approved amount"
        );
        return PoYToken.transferFrom(sender, recipient, amount);
    }
}
