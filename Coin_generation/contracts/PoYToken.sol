// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract PoYToken is ERC20 {
    constructor() public ERC20("PoY Token", "PoY") {
        _mint(msg.sender, 10 ** 24);
    }
}
