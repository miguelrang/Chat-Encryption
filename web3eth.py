from web3 import Web3


def transaccionEth(url, cuenta1, cuenta2, private_key1):
	#url = "HTTP://127.0.0.1:7545"
	tostring = ""
	web3 = Web3(Web3.HTTPProvider(url))
	print(web3.isConnected())

	#cuenta1 = "0xDC95e5477e1d2A788Fc14fF5C167405A46443956"
	#cuenta2 = "0xFcA94112C00021C12746e0ba6A682a07b1112fcF"

	#private_key1 = "d6957a6b8608a07f58b90f4b0b8bbc1f35124a30a64bdf8c7cfbce2df9fd7bdd"

	nonce = web3.eth.getTransactionCount(cuenta1)

	print('balance cuenta 1: ', web3.eth.getBalance(cuenta1))

	tx = {
		'nonce': nonce,
		'to': cuenta2,
		'value': web3.toWei(1, 'ether'),
		'gas': 2000000,
		'gasPrice': web3.toWei('50', 'gwei')
	}

	signed_tx = web3.eth.account.signTransaction(tx, private_key1)
	tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	tostring += "balance de cuenta: " + str(web3.fromWei(web3.eth.getBalance(cuenta1), 'ether')) + " | hash de transaccion (primeros 10): " + str(web3.toHex(tx_hash))[:10]

	return tostring
