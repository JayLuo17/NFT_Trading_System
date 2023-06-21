# NFT Trading System
This is the official implementation of the NFT trading system @ [A&amp;C Technology](https://www.linkedin.com/company/a-c-technology-inc)

- Aurthor: _[Jiayi](https://github.com/JayLuo17/) and [Hanhua](https://github.com/HenryJiang97)_


## Deployment
- Deploy on sepolia testnet
```
brownie run scripts/deploy.py --network sepolia
```

- Deploy on ganache (local); Need to add the ganache to the network configuration
```
brownie run scripts/deploy.py --network ganache
```

## NFT Generation
The basic implementation of issuing new NFT tokens (vechile title) based on the use's input

- Test on sepolia testnet
```
brownie run scripts/create_title.py --network sepolia
```

- Test on ganache (local)
```
brownie run scripts/create_title.py --network ganache
```
## Coin Generation
The basic implementation of issuing new PoY coin for rewarding

- Test on sepolia testnet
```
brownie run scripts/transfer.py --network sepolia
```

- Test on ganache (local)
```
brownie run scripts/transfer.py --network ganache
```

- Note that the transfer.py has several APIs for external usage.
```
register; addFund; transferFund
```

3. Before issuing new title NFT, need to add the vehicle information in `./input/user_inputs.py`. Please follow the sentax in the `./metadata/metadata_sample.py`

3. Notes:
- Need install brownie, recommend using the following `pipx` command; do not use `pipx install eth-brownie`
```
python3 -m pipx install eth-brownie
```
- Currently, all the NFT token records are hosted on ipfs using local point, need to migrate to public network using public service like [`pinata`](https://www.pinata.cloud/).
- Need to add sepolia testnet to brownie, which is the PoS eth-based network. Use the follwoing architecture & command:
```
   sepolia
    ├─id: sepolia
    ├─chainid: 11155111
    └─host: https://sepolia.infura.io/v3/XXX

brownie networks add Ethereum sepolia host=https://sepolia.infura.io/v3/XXX chainid=11155111
```

- Need to add ganache local testnet to brownie,  Use the follwoing architecture & command:
```
   ganache
    ├─id: ganache
    ├─chainid: 5777
    └─host: http://127.0.0.1:7545

brownie networks add Ethereum ganache host=http://127.0.0.1:7545 chainid=5777
```

## Update

- **06/19/2023**:

    - Initial commit to add the implementation of `NFT_generation`

- **06/21/2023**: 
    
    - Merge the `NFT_generation` and `Coin_generation` into one folder `PoY_Vehicle_NFT_System` to have a consistent testing environment

## TODOs
- [ ] Write the test functions
- [ ] Add other functions
- [x] Write the `Coin_generation` for PoY coin generation - already merged into the single working directory
