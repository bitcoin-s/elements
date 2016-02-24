#!/usr/bin/env python2

import os

class FedpegConstants:
	# VARIOUS SETTINGS...
        user = os.environ["RPC_USER"]
        password = os.environ["RPC_PASS"]
        sidechain_url = "http://" + user + ":" + password + "@127.0.0.1:4250"
        bitcoin_url = "http://" + user + ":" + password + "@127.0.0.1:18332"

	redeem_script = "512103b6da3a5a16ef4fbd359979250e03bb5e97f6ab46935bd2cb9a1a12406801166451ae"
	redeem_script_address = "2N83SZg4MKSMm9x3wwGeaf3be5dKxFvohwW"
	secondScriptPubKeyHash = "9eac001049d5c38ece8996485418421f4a01e2d7"
	secondScriptPubKey = "OP_DROP 144 OP_LESSTHANOREQUAL"
	#blocksigning_private_key = os.environ["BLOCKSIGNING_PRIV_KEY"] 
	blocksigning_private_key = "cVoNKaEfKorPBokgiuZEN5XoASfyGCb9DDrPPYxuRGErBL1sZyBS"
	functionary_private_key = "cP47fFC8eQGtB1RV3JCvXSBo5jb3YzEoH1bEEJoP64vGan9YHsCm"	
	#functionary_private_key = os.environ["FUNCTIONARY_PRIV_KEY"]

	bitcoin_tx_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../bitcoin-tx")
	contracthashtool_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../contracthashtool/contracthashtool")
	is_testnet = 1

	#Bitcoin:
	bitcoin_genesis_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
	#Testnet:
	#bitcoin_genesis_hash = "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943"

	nodes =["WARREN", "GWILLEN", "LUKE-JR/WIZKID", "MAAKU", "APOELSTRA", "MATT", "GMAXWELL"]
	my_node = "FILL_ME_IN"

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
