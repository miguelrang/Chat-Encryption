from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from functools import partial

from Enigma import *
from Rot13 import *
from web3eth import * # para las cripto


class Messenger(Screen):
	def __init__(self, **kwargs):
		super(Messenger, self).__init__(**kwargs)
		self.checks_cypher = [] # guardamos el cifrado a usar
		
		Clock.schedule_once(self.runFirstTime, .1)
		Clock.schedule_once(self.runAnimation, 5)
		Clock.schedule_interval(self.runAnimation, 15)
		

	def runFirstTime(self, *args):
		animation = Animation(user_font_size=dp(70), duration=.1)
		animation.start(self.ids.anim_msg_central)


	def runAnimation(self, *args):
		def Animation1(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .5, 'center_y': .25}, duration=5)
			first_2 = Animation(text_color=(0, 0, 0, 0), duration=5)
			central_1 = Animation(user_font_size=dp(size), duration=5)
			central_1.on_complete(Animation2(size=110, n='anim_msg_2'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation2(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .5, 'center_y': .25}, duration=5)
			first_2 = Animation(text_color=(0, 0, 0, 0), duration=5)
			central_1 = Animation(user_font_size=dp(size), duration=5)
			central_1.on_complete(Animation3(size=130, n='anim_msg_3'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation3(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .5, 'center_y': .25}, duration=5)
			first_2 = Animation(text_color=(0, 0, 0, 0), duration=5)
			central_1 = Animation(user_font_size=dp(size), duration=5)
			central_1.on_complete(Animation4(size=150, n='anim_msg_4'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation4(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .5, 'center_y': .25}, duration=5)
			first_2 = Animation(text_color=(0, 0, 0, 0), duration=5)
			central_1 = Animation(user_font_size=dp(size), duration=5)
			#central_1.on_complete(Animation5(size=150, n='anim_msg_4'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation5(size:int, n:str, *largs):
			first_1 = Animation(pos_hint={'center_x': .9, 'center_y': .4}, duration=1)
			first_2 = Animation(text_color=(1, 1, 1, 1), duration=1.4)
			central_1 = Animation(user_font_size=dp(size), duration=1)
			central_1.on_complete(Animation6(size=110, n='anim_msg_3'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation6(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .9, 'center_y': .1}, duration=1)
			first_2 = Animation(text_color=(1, 1, 1, 1), duration=1.4)
			central_1 = Animation(user_font_size=dp(size), duration=1.7)
			central_1.on_complete(Animation7(size=90, n='anim_msg_2'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation7(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .1, 'center_y': .1}, duration=1)
			first_2 = Animation(text_color=(1, 1, 1, 1), duration=1.4)
			central_1 = Animation(user_font_size=dp(size), duration=1.7)
			central_1.on_complete(Animation8(size=70, n='anim_msg_1'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)

		def Animation8(size:int, n:str):
			first_1 = Animation(pos_hint={'center_x': .1, 'center_y': .4}, duration=1)
			first_2 = Animation(text_color=(1, 1, 1, 1), duration=1.4)
			central_1 = Animation(user_font_size=dp(size), duration=1.7)
			#central_1.on_complete(Animation8(size=70, n='anim_msg_1'))
			first_1.start(self.ids[n]), first_2.start(self.ids[n]), central_1.start(self.ids.anim_msg_central)
		
		Animation1(size=90, n='anim_msg_1')
		Clock.schedule_once(partial(Animation5, 150, 'anim_msg_4'), 5)
		

	def openDialog(self, title, text):
		def closeDialog(*args):
			self.dialog.dismiss()

		self.dialog = MDDialog(
			title=title,
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=closeDialog
				)
			]
		)
		self.dialog.open()


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

		if metodo == 'Enigma':
			contenido = contenido.replace(" ", "")
			self.ids.chatBox.text += f"\nsu mensaje cifrado (rotores: {rotor_pos}, llave: {elected_keys}) {enigma(contenido.upper(), elected_keys, rotor_pos)}"

		if metodo == 'Rot 13':
			self.ids.chatBox.text += f"\nsu mensaje cifrado: {encriptarString(contenido, 112)}"  

		
		# hacemos la transaccion
		self.ids.cantidad_eth.text = transaccionEth(
			self.ids.url_eth.text,
			self.ids.cuenta_eth.text,
			self.ids.cuenta_destino_eth.text,
			self.ids.clave_privada_eth.text
		)