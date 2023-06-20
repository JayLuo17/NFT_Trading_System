# NFT Trading System
This is the official implementation of the NFT trading system @ [A&amp;C Technology](https://www.linkedin.com/company/a-c-technology-inc)

- Aurthor: _[Jiayi](https://github.com/JayLuo17/) and [Hanhua](https://github.com/HenryJiang97)_


## NFT Generation
1. The basic implementation of deploying a smart contract - test on sepolia testnet
```
brownie run scripts/deploy.py --network sepolia
```

2. The basic implementation of issuing new NFT tokens (vechile title) based on the use's input
```
brownie run scripts/create_title.py --network sepolia
```

3. Before issuing new title NFT, need to add the vehicle information in `./input/user_inputs.py`. Please follow the sentax in the `./metadata/metadata_sample.py`

3. Notes:
- Need install brownie, recommend using the following `pipx` command; do not use `pipx install eth-brownie`
```
python3 -m pipx install eth-brownie
```
- Currently, all the NFT token records are hosted on ipfs using local point, need to migrate to public network using public service like [`pinata`](https://www.pinata.cloud/).
- Need to add sepolia testnet to brownie, which is the PoS eth-based network. Use the follwoing architecture:
```
   sepolia
    ├─id: sepolia
    ├─chainid: 11155111
    └─host: https://sepolia.infura.io/v3/XXX
```

## Coin Generation

- Under implementation... :yum:

## TODOs
- [ ] Write the test functions for `NFT_generation`
- [ ] Add other functions to the 
- [ ] Write the `Coin_generation` for PoY coin generation
