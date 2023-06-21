// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract PoYToken is ERC20 {
    uint256 private supply = 10 ** 24;

    constructor() public ERC20("PoY Token", "PoY") {
        _mint(msg.sender, supply);
    }
}
