from kivy.uix.screenmanager import Screen

from Enigma import *
from Rot13 import *
from web3eth import * # para las cripto


class Messenger(Screen):
	def __init__(self, **kwargs):
		super(Encrypt_Decrypt, self).__init__(**kwargs)
		self.checks_cypher = [] # guardamos el cifrado a usar
		#self.checks_method = [] # guardamos el metodo a usar

	def onClickListener(self, instance, value, group, cypher):
		'''
		instance: es el valor en memoria del checkbox, no nos sirve pero es enviado como parametro automaticamente
		value: True or False dependiendo si esta marcado o desmarcado
		group: a que grupo pertenece, si es un cifrado o es un metodo (cifrar o decifrar)
		cypher: el valor que le enviamos, puede ser: rot, rsa, enigma o si hablamos de metodos: cifrado o decifrado
		'''
		
		# if's para verificar que los checkboxes esten marcados, muestran el texto marcado en un label
		if value == True:
			if group == 'cypher':
				self.checks_cypher.append(cypher)
				#self.ids.info.text = f'Usando cifrado: {self.checks_cypher[0]}'


			# if group == 'method':
			# 	self.checks_method.append(cypher)
				#self.ids.info.text = f'Usando metodo: {self.checks_method[0]}'


		else: # si desmarcamos un checkbox, este se quita de la lista
			if group == 'cypher':
				self.checks_cypher.remove(cypher)
				

		#print(self.checks_cypher)
		if direccion != '': # si direccion contiene la direccion de un archivo, lo muestra en el input
			self.ids.directory.text = direccion
			
			self.ids.info.text = '' # cuando desmarcamos algo, se quita el texto a mostrar

		# desbloqueamos el boton de ejecutar una vez tengamos un tipo de cifrado, metodo y direccion del archivo
		if len(self.checks_cypher) == 1:
			self.ids.execute.disabled = False

		else:
			self.ids.execute.disabled = True

	def getCuentaEth(self):
		try:
			with open(f"Certificados/{username}/user.cert", "r") as f:
				content_file:str = f.read()

			content_file = content_file.replace("'", "\"")
			content_file = content_file.replace("b\"", "\"")

			data = json.loads(content_file)
			account = data["normal"]["email"]
			print(account, type(account))

			return account
		except:
			pass

	def getPrivateKey(self):
		try:
			with open(f"Certificados/{username}/user.cert", "r") as f:
				content_file:str = f.read()

			content_file = content_file.replace("'", "\"")
			content_file = content_file.replace("b\"", "\"")

			data = json.loads(content_file)
			eth_key = data["normal"]["password_(1)"]

			return eth_key
		except:
			pass

	# Cuando se preciona ejecutar, llegamos a esta funcion
	def ejecutarCifrado(self):
		#print(self.checks_cypher)
		metodo = self.checks_cypher[0] # le damos a metodo el valor del cifrado que vamos a usar
		contenido = self.ids.messageBox.text
		textoEnEnteros = ''
		rotores = [
			[1, 2, 3],
			[1, 3, 2],
			[2, 1, 3],
			[2, 3, 1],
			[3, 1, 2],
			[3, 2, 1]
		]
		keys = ['A', 'B', 'C', 'D', 'E', 'F',
		'G', 'H', 'I', 'J', 'K', 'L', 'M',
		'N', 'O', 'P', 'Q', 'R', 'S', 'T',
		'U', 'V', 'W', 'X', 'Y', 'Z']
		rotor_pos = ''
		elected_rotors = random.choice(rotores)
		#elected_keys = random.choice(keys) + " " + random.choice(keys) + " " + random.choice(keys)
		elected_keys = random.choice(keys) + random.choice(keys) + random.choice(keys)
		
		# concatenamos los rotores

		rotor_pos += str(elected_rotors[0]) + ' ' + str(elected_rotors[1]) + ' ' + str(elected_rotors[2])



		#encriptacion = self.checks_method[0] # le damos un valor sobre el metodo que usaremos
		
		# if metodo == 'RSA':

		# 	if encriptacion == 'Cypher':
		# 		print('cifrar RSA') # remover print una vez tengamos el modulo

		# 	if encriptacion == 'Decypher':
		# 		print('decifrar RSA') # remover print una vez tengamos el modulo

		if metodo == 'Enigma':
			contenido = contenido.replace(" ", "")
			self.ids.chatBox.text += f"\nsu mensaje cifrado (rotores: {rotor_pos}, llave: {elected_keys}) {enigma(contenido.upper(), elected_keys, rotor_pos)}"

		# 	if encriptacion == 'Cypher':
		# 		print('cifrar Enigma') # remover print una vez tengamos el modulo

		# 	if encriptacion == 'Decypher':
		# 		print('decifrar Enigma') # remover print una vez tengamos el modulo

		if metodo == 'Rot 13':
			self.ids.chatBox.text += f"\nsu mensaje cifrado: {encriptarString(contenido, 112)}"  

			# if encriptacion == 'Cypher':
			# 	encriptar(contenido, 112)

			# if encriptacion == 'Decypher':
			# 	# print(desencriptar(contenido, 112)) # descomentar para ver el decifrado en la terminal
			# 	with open('Rot 13.unlocked', 'w') as f:
			# 		f.write(desencriptar(contenido, 112))

			# 	self.ids.info.text = 'Cifrado terminado'
		

		# hacemos la transaccion
		self.ids.cantidad_eth.text = transaccionEth(
			self.ids.url_eth.text,
			self.ids.cuenta_eth.text,
			self.ids.cuenta_destino_eth.text,
			self.ids.clave_privada_eth.text
		)