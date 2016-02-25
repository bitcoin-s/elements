##Building A New Sidechain with Elements

This is a basic step-by-step to building your own sidechain and setting up a fedpeg. 

####Elements
Please look over the [Elements Project](https://github.com/ElementsProject/elements) if you haven't already. Also read [Alpha README](https://github.com/ElementsProject/elements/blob/alpha/alpha-README.md) for building dependencies and to follow along. The instructions for building the dependencies are pretty cut and clear, however, the building of a new fedpeg isn't as detailed. Keep the Elements Project's Alpha-README open in a separate tab for reference. 

####Prerequisites
1. Linux. Building with Windows is possble - publish a guide if you know how as there isn't one publicly available! :)
2. All dependencies for Elements-Alpha. [Build Notes](https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md)

####Build
Try to follow this order to avoid unneccessary compilations.

Edit your `.bashrc`. We'll come back to this file later:
```
RPC_USER=your_username_here
RPC_PASSWORD=your_super_random_long_password_here
export RPC_USER
export RPC_PASS
```

Bitcoin testnet (mainchain):
```
git clone https://github.com/ElementsProject/elements
cd elements
git checkout mainchain
./autogen.sh && ./configure && make
mv src/bitcoin{d,-cli,-tx} ../
```

Run testnet. If you get an error asking to rebuild the blockchain, replace `-txindex` with `-reindex`. If you have to rebuild it, continue these instructions while it syncs:
```
./bitcoind -rpcuser=$RPC_USER -rpcpassword=$RPC_PASS -testnet -txindex -daemon
```

Clone `alpha`. Make sure it is up-to-date with the Elements repo:
```
git checkout alpha
./autogen.sh && ./configure && make
mv src/alpha{d,-cli,-tx} ../
```

With bitcoin testnet, generate an address and obtain the private/public key.
```
bitcoin-cli -testnet getnewaddress //returns some address
bitcoin-cli -testnet validateaddress [address] //returns JSON object. Copy the public key.
bitcoin-cli -testnet dumpprivkey [address] //returns private key. Save this - we'll need it later.
```
You should be on your sidechain branch (alpha). This is the part where we uniquely create your sidechain. Open `src/chainparams.cpp` and edit the public keys, ports, and seeds. 
Line 132 has the public keys for each functionary/blocksigner: 
```
scriptDestination = CScript() << OP_5 << ParseHex("027d5d62861df77fc9a37dbe901a579d686d1423be5f56d6fc50bb9de3480871d1") << ParseHex("03b41ea6ba73b94c901fdd43e782aaf70016cc124b72a086e77f6e9f4f942ca9bb") << ParseHex("02be643c3350bade7c96f6f28d1750af2ef507bc1f08dd38f82749214ab90d9037") << ParseHex("021df31471281d4478df85bfce08a10aab82601dca949a79950f8ddf7002bd915a") << ParseHex("0320ea4fcf77b63e89094e681a5bd50355900bf961c10c9c82876cb3238979c0ed") << ParseHex("021c4c92c8380659eb567b497b936b274424662909e1ffebc603672ed8433f4aa1") << ParseHex("027841250cfadc06c603da8bc58f6cd91e62f369826c8718eb6bd114601dd0c5ac") << OP_7 << OP_CHECKMULTISIG;
```
For simplicity, let's replace with current 5-of-7 with a 1-of-1. Change to: 
```
scriptDestination = CScript() << OP_1 << ParseHex("[paste public key]") << OP_1 << OP_CHECKMULTISIG;
```
