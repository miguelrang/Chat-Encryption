from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.metrics import dp

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from functools import partial
from web3 import Web3

import random
import os

from Enigma import *
from Rot13 import *
import web3 # para las cripto


class Messenger(Screen):
	def __init__(self, **kwargs):
		super(Messenger, self).__init__(**kwargs)

		Clock.schedule_once(self.runFirstTime, .1)
		Clock.schedule_once(self.runAnimation, 5)
		Clock.schedule_interval(self.runAnimation, 15)
		self.user = ''
		

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


	# CALL FUNCTION WHEN YOU PRESS --> 'Cifrar'
	def runEncryption(self, method:bool, msg:id, chat_box:id, url_eth:str, sender:str, addressee:str, private_key_from_eth:str):
		def transaccionEth(url:str, sender:str, addressee:str, private_key1:str):
			#url_eth = "http://127.0.0.1:7545"
			tostring = ""
			web3 = Web3(Web3.HTTPProvider(url))
			
			print(web3.isConnected())

			#sender = "0xDC95e5477e1d2A788Fc14fF5C167405A46443956"
			#addressee = "0xFcA94112C00021C12746e0ba6A682a07b1112fcF"

			#private_key1 = "d6957a6b8608a07f58b90f4b0b8bbc1f35124a30a64bdf8c7cfbce2df9fd7bdd"

			tx = {
				'nonce': web3.eth.getTransactionCount(sender),
				'to': addressee,
				'value': web3.toWei(1, 'ether'),
				'gas': 2000000,
				'gasPrice': web3.toWei('50', 'gwei') # 
			}
			
			signed_tx = web3.eth.account.signTransaction(tx, private_key1)
			tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
			tostring += "balance de cuenta: " + str(web3.fromWei(web3.eth.getBalance(sender), 'ether')) + " | hash de transaccion (primeros 10): " + str(web3.toHex(tx_hash))[:10]

			return tostring

		try:
			# WE RUN THE TRANSACTION
			succesful_transaction:bool = True
			self.ids.remaining_eth.text = transaccionEth(
				url_eth,
				sender,
				addressee,
				private_key_from_eth
			)
		except Exception as e:
			succesful_transaction:bool = False
			self.openDialog(
				title='Lo sentimos',
				text='A ocurrido un error con la transacción, por favor verifique que los datos esten correctos o que tenga suficientes monedas.'
			)
			print(e)
		
		if succesful_transaction:
			# WE CONTINUE TO EXECUTE THE ENCRYPTION
			#textoEnEnteros = ''
			rotors = [
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
			elected_rotors = random.choice(rotors)
			
			elected_keys = random.choice(keys) + random.choice(keys) + random.choice(keys)
			
			# We concatenate the rotors
			rotor_pos += str(elected_rotors[0]) + ' ' + str(elected_rotors[1]) + ' ' + str(elected_rotors[2])

			if method == True: # -> Enigma
				# We delete the spaces because the space did not exist the space between words
				msg.text = msg.text.replace(" ", "")
				
				# We show the result on the board
				chat_box.text += f"\nSu mensaje cifrado (rotors: {rotor_pos}, llave: {elected_keys}) {enigma(msg.text.upper(), elected_keys, rotor_pos)}"

			else: # -> Rot 13
				# We show the result on the board
				chat_box.text += f"\nSu mensaje cifrado (key: 13): {encriptarString(msg.text, 112)}"  


	# CALL FUNCTION WHEN YOU PRESS --> 'x' <-- BUTTON
	def endSeasson(self, sender, private_key_from_eth, url_eth, chat_box, msg):
		sender.text = ''
		#private_key_from_eth.text = ''
		#url_eth.text = ''
		chatBox.text = ''
		msg.text = ''
		app.root.current = 'home'


	# ************ THIS FUNCTION IS NOT YET TESTED ***************
	def saveChat(self, sender:str, chat_box:str):
		path = f'{os.getcwd()}/Certificados/{sender}'

		with open(f"{path}/chat.txt", 'a') as f:
			f.write(f"{chat_box}\n\n\n")

		self.endSeasson()