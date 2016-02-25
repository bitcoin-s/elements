##Building A New Sidechain with Elements

This is a basic step-by-step to building your own sidechain and setting up a fedpeg. 

####Elements
Please look over the [Elements Project](https://github.com/ElementsProject/elements) if you haven't already. Also read [Alpha README](https://github.com/ElementsProject/elements/blob/alpha/alpha-README.md) for building dependencies and to follow along. The instructions for building the dependencies are pretty cut and clear, however, the building of a new fedpeg isn't as detailed. Keep the Elements Project's Alpha-README open in a separate tab for reference. 

####Prerequisites
1. Linux. Building with Windows is possble - publish a guide if you know how as there isn't one publicly available! :)
2. All dependencies for Elements-Alpha. [Build Notes](https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md)

####Build
Try to follow this order to avoid unneccessary recompilations. This is an extension of the instructions to "Run a fedpeg operator" in the Element's alpha README.

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

Checkout `alpha`. Make sure it is up-to-date with the Elements repo alpha branch:
```
git checkout alpha
```

With bitcoin testnet, generate an address and obtain the private/public key.
```
bitcoin-cli -testnet getnewaddress //returns some address
bitcoin-cli -testnet validateaddress [address] //returns JSON object. Copy the public key.
bitcoin-cli -testnet dumpprivkey [address] //returns private key. Save this - we'll need it later.
```
You should be on your sidechain branch (alpha). This is the part where we uniquely create your sidechain with the public keys of each functionary/blocksigner. Open `src/chainparams.cpp` and edit the public keys, ports, and seeds. Line 132 has the public keys for each functionary/blocksigner: 
```
scriptDestination = CScript() << OP_5 << ParseHex("027d5d62861df77fc9a37dbe901a579d686d1423be5f56d6fc50bb9de3480871d1") << ParseHex("03b41ea6ba73b94c901fdd43e782aaf70016cc124b72a086e77f6e9f4f942ca9bb") << ParseHex("02be643c3350bade7c96f6f28d1750af2ef507bc1f08dd38f82749214ab90d9037") << ParseHex("021df31471281d4478df85bfce08a10aab82601dca949a79950f8ddf7002bd915a") << ParseHex("0320ea4fcf77b63e89094e681a5bd50355900bf961c10c9c82876cb3238979c0ed") << ParseHex("021c4c92c8380659eb567b497b936b274424662909e1ffebc603672ed8433f4aa1") << ParseHex("027841250cfadc06c603da8bc58f6cd91e62f369826c8718eb6bd114601dd0c5ac") << OP_7 << OP_CHECKMULTISIG;
```
For simplicity, let's replace with current 5-of-7 with a 1-of-1. Change to: 
```
scriptDestination = CScript() << OP_1 << ParseHex("[paste public key]") << OP_1 << OP_CHECKMULTISIG;
```
Line 139 has the DNS seeds. You'll need to create one of your own in order to communicate on your port. Replace the current 5 seeds with your own. Also delete the testnet seed on line 198. 

Still in `src/chainparams.cpp`, change the testnet port number on L182 - this is the unique channel of communication for your sidechain so don't just increase/decrease it by one. This is one of two ports we'll change. Call this one the protocol port. Keep a side note of this protocol port - we'll need it later.

You need to duplicate what you did on L132 of `src/chainparams.cpp` on L1451 of `src/script/interpreter.cpp`. Also in `src/script/interpreter.cpp`, change L1469 using [Instagibbs' fix](https://github.com/instagibbs/elements/commit/d390521215f1b47f8d46e8af728c5d353e1db4bf).

Open `src/chainparamsbase.cpp`, change the port on L43. This is the RPC port - keep it different from the protocol port (i.e. alpha's ports are 4250 and 4251). On L44, you can change the name of the data directory for your sidechain (where your blocks, .dat files, etc. will be stored). 

At this point, you can compile your sidechain in the same way we compiled the mainchain earlier. There are a few help/console string messages you can change in `main.cpp, init.cpp, bitcoind.cpp`, but it's not necessary for functional purposes. 

```
./autogen.sh && ./configure && make
```

If there's a error in your compilation, go back to the file the compilation failed on and fix the error. Make sure to run `make clean` before compilating again. You'll only need to recompile your sidechain branch, not the bitcoin testnet `mainchain` branch.

Upon successful compilation:
```
mv src/alpha{d,-cli,-tx} ../
./alphad -rpcuser=$RPC_USER -rpcpassword=$RPC_PASS -testnet -rpcconnect=127.0.0.1 -rpcconnectport=18332 -tracksidechain=all -txindex -blindtrust=false -daemon
```
