#!/usr/bin/env python2

import os

class FedpegConstants:
	# VARIOUS SETTINGS...
        user = os.environ["RPC_USER"]
        password = os.environ["RPC_PASS"]
        sidechain_url = "http://" + user + ":" + password + "@127.0.0.1:4250"
        bitcoin_url = "http://" + user + ":" + password + "@127.0.0.1:18332"

	redeem_script = "5221026484f5b5727af9a71b3641e6c8d778d655142b5a398131ee58f624c662d4ff5a21023c57fea991ff073c49b023ca167ceb355533f9a7ae633d3b75988bef6f74c21d52ae"
	redeem_script_address = "2MzEQ7ntgsLVs5EG84BEzJX31kE4j26F2XU"
	secondScriptPubKeyHash = "9eac001049d5c38ece8996485418421f4a01e2d7"
	secondScriptPubKey = "OP_DROP 144 OP_LESSTHANOREQUAL"
	blocksigning_private_key = os.environ["BLOCKSIGNING_PRIV_KEY"] 
	functionary_private_key = os.environ["FUNCTIONARY_PRIV_KEY"]

	bitcoin_tx_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../bitcoin-tx")
	contracthashtool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../contracthashtool/contracthashtool")
	is_testnet = 1

	#Bitcoin:
	bitcoin_genesis_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
	#Testnet:
	#bitcoin_genesis_hash = "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943"

	nodes =["TOM","CHRIS"]
	my_node = "173.31.39.168"

	# Set this to non-None if you're using a proxy (eg for Tor)
	# Note that this requires ZMQ 4.1
	socks_proxy = None
	#socks_proxy = "127.0.0.1:9050"

	def __init__(self):
		# Derived constants (dont touch)
		self.testnet_arg = ""
		if self.is_testnet == 1:
			self.cht_testnet_arg = "-t"
			self.btc_testnet_arg = "-testnet"
		else:
			self.cht_testnet_arg = ""
			self.btc_testnet_arg = ""

		self.sigs_required = int(self.redeem_script[:2], 16) - 0x50

		self.inverse_bitcoin_genesis_hash = "".join(reversed([self.bitcoin_genesis_hash[i:i+2] for i in range(0, len(self.bitcoin_genesis_hash), 2)]))
