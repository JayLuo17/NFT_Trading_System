// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract TitleToken is ERC721URIStorage {
    uint256 public Counter;

    mapping(uint256 => string) public tokenIdToURI; // Record the id and the corresponding type

    constructor() public ERC721("VehicleTitle", "VT") {
        Counter = 0;
    }

    function createNewTitle(string memory tokenURI) public returns (uint256) {
        uint256 newTitleId = Counter;
        _safeMint(msg.sender, newTitleId);
        _setTokenURI(newTitleId, tokenURI);
        tokenIdToURI[Counter] = tokenURI;
        Counter = Counter + 1;
        return newTitleId;
    }

    function setTokenURI(uint256 titleId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), titleId),
            "Caller is not owner no approved!"
        );
        _setTokenURI(titleId, _tokenURI);
    }
}
