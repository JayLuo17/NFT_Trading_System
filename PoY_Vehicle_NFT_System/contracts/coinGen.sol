// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract PoYCoin is ERC721Enumerable {
    using Counters for Counters.Counter;
    Counters.Counter private _CoinIdCounter;
    uint[] public _faceVals;

    // TODO: Mapping from token ID to token metadata (e.g., a JSON string or IPFS hash)
    mapping(uint256 => string) private _tokenURIs;

    constructor() ERC721("PoYCoin", "POY") {
        _faceVals = [100, 10, 5, 1];
    }

    struct CoinData {
        uint[] code;
        uint value;
    }

    mapping(uint256 => CoinData) public _coinData;
    uint256[] public coinIds;
    address[] public coinAds;

    function getCoinNum() public view returns (uint256) {
        return coinIds.length;
    }

    function mintCoin(
        address recipient,
        uint[] memory code,
        uint val
    ) public returns (uint256) {
        _CoinIdCounter.increment();
        uint256 newCoinId = _CoinIdCounter.current();
        _safeMint(recipient, newCoinId);

        _coinData[newCoinId] = CoinData({code: code, value: val});
        coinIds.push(val);
        coinAds.push(recipient);

        return newCoinId;
    }

    function mint(
        address recipient,
        address pool,
        uint[] memory imageNums,
        uint supply,
        uint X, // number of digit
        uint Y // base, total supply is X**Y
    ) public {
        require(supply <= X ** Y);
        // ============== First to recipient ========== //
        // Derive the count data for each coin face value
        // costs is the same length of the _faceVals
        uint[] memory counts = minCoins(_faceVals, supply);

        // Derive the code list based on the imageBytes and base Y
        // segments is of length Y, reprensents the byte code for each image segment
        // Derive the code for each coin
        uint[][] memory codes = deriveCodes(
            divideImageNums(imageNums, Y),
            X,
            Y
        );
        uint codeLength = codes[0].length;

        uint curr_ptr = 0;
        for (uint i = 0; i < counts.length; i++) {
            uint faceVal = _faceVals[i];
            for (uint j = 0; j < counts[i]; j++) {
                uint[] memory finalCode = new uint[](codeLength);
                for (uint m = curr_ptr; m < curr_ptr + faceVal; m++) {
                    finalCode = sumArrays(finalCode, codes[m]);
                }
                // mint a new coin to the recipient
                mintCoin(recipient, finalCode, faceVal);
                curr_ptr += faceVal;
            }
        }

        // ============== Second to owner ========== //
        uint[] memory newCounts = minCoins(_faceVals, X ** Y - supply);

        for (uint i = 0; i < newCounts.length; i++) {
            uint faceVal = _faceVals[i];
            for (uint j = 0; j < newCounts[i]; j++) {
                uint[] memory finalCode = new uint[](codeLength);
                for (uint m = curr_ptr; m < curr_ptr + faceVal; m++) {
                    finalCode = sumArrays(finalCode, codes[m]);
                }
                // mint a new coin to the recipient
                mintCoin(pool, finalCode, faceVal);
                curr_ptr += faceVal;
            }
        }
    }

    function coinVal(uint256 coinID) public view returns (uint) {
        require(_exists(coinID), "Coin does not exist");
        return _coinData[coinID].value;
    }

    function coinCode(uint256 coinID) public view returns (uint[] memory) {
        require(_exists(coinID), "Coin does not exist");
        return _coinData[coinID].code;
    }

    function sumArrays(
        uint[] memory arr1,
        uint[] memory arr2
    ) public pure returns (uint[] memory) {
        require(arr1.length == arr2.length, "Arrays must have the same length");

        uint[] memory result = new uint[](arr1.length);

        for (uint i = 0; i < arr1.length; i++) {
            result[i] = arr1[i] + arr2[i];
        }

        return result;
    }

    function multiplyWithConstant(
        uint[] memory arr,
        uint c
    ) public pure returns (uint[] memory) {
        uint[] memory result = new uint[](arr.length);

        for (uint i = 0; i < arr.length; i++) {
            result[i] = arr[i] * c;
        }

        return result;
    }

    // change to internal during production
    function divideImageNums(
        uint[] memory imageNums,
        uint Y
    ) public pure returns (uint[][] memory) {
        uint length = imageNums.length;
        uint remainder = length % Y;

        if (remainder != 0) {
            uint paddingLength = Y - remainder;
            uint[] memory paddedImageNums = new uint[](length + paddingLength);
            for (uint i = 0; i < length; i++) {
                paddedImageNums[i] = imageNums[i];
            }
            for (uint i = 0; i < paddingLength; i++) {
                paddedImageNums[length + i] = 0; // Padding with minimum value 0
            }
            imageNums = paddedImageNums;
        }

        uint partLength = imageNums.length / Y;
        uint[][] memory segments = new uint[][](Y);
        for (uint i = 0; i < Y; i++) {
            segments[i] = slice(imageNums, i * partLength, partLength);
        }
        return segments;
    }

    function slice(
        uint[] memory _nums,
        uint _start,
        uint _length
    ) internal pure returns (uint[] memory) {
        uint[] memory tempNums = new uint[](_length);
        for (uint i = 0; i < _length; i++) {
            tempNums[i] = _nums[_start + i];
        }
        return tempNums;
    }

    // change to internal during production
    function deriveCodes(
        uint[][] memory segments,
        uint X,
        uint Y
    ) public pure returns (uint[][] memory) {
        require(segments.length == Y);
        uint codeLength = segments[0].length;
        uint total = X ** Y - 1;
        uint[][] memory codes = new uint[][](total); // Need to check the dimension
        for (uint i = 0; i < total; i++) {
            codes[i] = new uint[](codeLength);
        }

        for (uint i = 0; i < total; i++) {
            uint[] memory coeffs = toBaseY(i + 1, X);
            uint[] memory tmp = new uint[](codeLength);
            for (uint j = 0; j < coeffs.length; j++) {
                tmp = sumArrays(
                    tmp,
                    multiplyWithConstant(segments[j], coeffs[j])
                );
            }
            codes[i] = tmp;
        }
        return codes;
    }

    // change to internal during production
    function toBaseY(
        uint256 number,
        uint256 y
    ) public pure returns (uint[] memory) {
        require(y > 1, "Base y should be greater than 1");

        if (number == 0) {
            uint[] memory ret = new uint[](1);
            ret[0] = 0;
            return ret;
        }

        uint256 length = 0;
        uint256 tempNumber = number;
        while (tempNumber > 0) {
            length++;
            tempNumber /= y;
        }

        uint[] memory representation = new uint[](length);
        uint256 index = 0;
        while (number > 0) {
            representation[index] = number % y;
            number /= y;
            index++;
        }

        return representation;
    }

    function reverse(uint[] memory arr) public pure returns (uint[] memory) {
        uint length = arr.length;
        uint[] memory reversedArr = new uint[](length);

        for (uint i = 0; i < length; i++) {
            reversedArr[i] = arr[length - i - 1];
        }

        return reversedArr;
    }

    function minCoins(
        uint[] memory faceValues,
        uint total
    ) public pure returns (uint[] memory) {
        uint[] memory counts = new uint[](faceValues.length);
        uint remaining = total;

        for (uint i = 0; i < faceValues.length; i++) {
            while (remaining >= faceValues[i]) {
                remaining -= faceValues[i];
                counts[i]++;
            }
        }

        // If the total couldn't be reached using the given face values
        if (remaining != 0) {
            // Return empty arrays to indicate it's not possible
            return new uint[](0);
        }

        return counts;
    }
}
