// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// The required functions:
// Record the user's address and the corresponding remaining amount
// Always need to approve the amount first and then let the smart contract move the fund.

contract TokenTransfer is Ownable {
    IERC20 public PoYToken;
    address[] public registeredUsers;
    uint256 public numUsers;
    uint256 public InitialSupply;

    // mapping token address -> staker address -> amount
    // The mapping to store the registartion status of addresses
    mapping(address => bool) public isRegistered;

    constructor(address _PoYAddress) public {
        PoYToken = IERC20(_PoYAddress);
        InitialSupply = 10 ** 3;
        numUsers = 0;
    }

    function registerAddress(
        address user_address
    ) public onlyOwner returns (bool) {
        // Check if the user is already registered.
        if (isRegistered[user_address]) {
            return false;
        } else {
            require(!isRegistered[user_address], "Address already registered");

            // Register the address
            isRegistered[user_address] = true;
            registeredUsers.push(user_address);
            numUsers = numUsers + 1;

            return true;
        }
    }

    function issueInitialFund(address receiver) public onlyOwner {
        require(isRegistered[receiver], "Recipient address not registered");
        PoYToken.transfer(receiver, InitialSupply);
    }

    function totalTokenSupply() external view returns (uint256) {
        return PoYToken.totalSupply();
    }

    function TokenBalance(address account) external view returns (uint256) {
        // Check if the address registered.
        // require(isRegistered[account], "Address doesn't registered");

        return PoYToken.balanceOf(account);
    }

    function issueFund(
        address receiver,
        uint256 amount
    ) external returns (bool) {
        // Check if the address registered.
        require(isRegistered[receiver], "Receiver address not registered");

        return PoYToken.transfer(receiver, amount);
    }
}
