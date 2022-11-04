from kivy.uix.screenmanager import Screen
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from nacl.signing import SigningKey

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import hashlib

from Rot13 import *

import os
import re


class Join(Screen):
	def __init__(self, **kwargs):
		super(Join, self).__init__(**kwargs)
		global app
		app = MDApp.get_running_app()


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


	def validate(self, username, metamask, password, password2): # gen_keys
		def userExist(username):
			if username in os.listdir('Certificados/'):
				return True
			else:
				return False

		def validMetamaskAccount(account:str):
			if account == '':
				return None
			else:
				if len(account) == 42:
					if re.compile(r'0x([A-Z]|[a-z]|[0-9])+').fullmatch(account):
						return True
					else:
						self.openDialog(
							title='Atención',
							text='Fórmato de cuenta invalido.'
						)
						return False
				else:
					self.openDialog(
						title='Atención',
						text='Longitud de la cuenta invalido, por favor corrobore que sea correcta.'
					)
					return False

		if userExist(username.text) or username.text == '':
			
			if username.text == '':	
				self.openDialog(
					title='Atención',
					text='Campo \'Nombre de Usuario\' vacío.'
				)

			elif userExist(username.text):
				self.openDialog(
					title='Atemción',
					text='Este usuario ya existe.'
				)

		else:
			if validMetamaskAccount(metamask.text) == False:
				pass

			elif validMetamaskAccount(metamask.text) == None:
				self.openDialog(
					title='Atención',
					text='Campo \'Metamask\' vacío.'
				)
			else:
				if password.text == "":
					self.openDialog(
						title='Atención',
						text='Campo \'Primera Contraseña (8 - 27 caracteres)\' vacío.'
					)
				else:
					if password2.text == "":
						self.openDialog(
							title='Atención',
							text='Campo \'Segunda Contraseña (8 - 27 caracteres)\' vacío.'
						)
					else:
						if (len(password.text) > 7 and len(password.text) < 28) and (len(password2.text) > 7 and len(password2.text) < 28):
							#text_inputs:list = [
							#	username.text,
							#	metamask.text,
							#	password.text
							#]
							
							# RSA (keys)
							self.private_key = RSA.generate(1024)
							self.public_key = self.private_key.publickey()

							#####
							# Buttons
							self.ids.gen_keys.disabled = True
							self.ids.empty.disabled = False
							self.ids.save.disabled = False
							# disabled
							# TextInputs
							username.disabled = True
							metamask.disabled = True
							password.disabled = True
							password2.disabled = True

							self.ids.cert_information.hint_text = ''

							# SHOW INFORMATION
							username = f"Nombre de Usuario: {username.text}"
							metamask = f"Cuenta: {metamask.text}"
							password = f"Contraseñas: ********** & **********"
							pub_key = f"Clave Publica: **********"
							priv_key = f"Clave Privada: **********"
																																																		  #
							self.ids.cert_information.text = f"{username}\n{metamask}\n{password}\n{pub_key}\n{priv_key}\n\n*Se guardara un documento con su llave privada\n  y otro con su llave publica en el escritorio"
						else:
							self.openDialog(
								title='Atención',
								text='La contraseña debe de tener entre 8 y 27 caracteres.'
							)		

	def empty(self, username, metamask, password, password2, cert_information):
		# empty
		username.text = ""
		metamask.text = ""
		password.text = ""
		password2.text = ""
		cert_information.text = ""
		
		# hint_texts
		#username.hint_text = "Nombre de Usuario"
		#metamask.hint_text = "Correo de Ethereum"
		#password.hint_text = "Contraseña de Ethereum"
		#password2.hint_text = "Contraseña (8 - 27 caracteres)"
		#cert_information.hint_text = 'Información del Usuario'
		
		# disabled	
		username.disabled = False
		metamask.disabled = False
		password.disabled = False
		password2.disabled = False
		
		self.ids.empty.disabled = True
		self.ids.gen_keys.disabled = False
		self.ids.save.disabled = True

	
	def save(self, username:str, metamask:str, password, password2): # save information
		def genKeys() -> tuple:
			encr_pub_key:list = encriptar(self.public_key.export_key(), len(self.ids.password2.text))
			encr_pub_key:bytes = b"".join(encr_pub_key)
			#encr_pub_key:str = encr_pub_key.decode()
			#print(encr_pub_key)

			encr_priv_key:str = encriptar(self.private_key.export_key(), len(self.ids.password2.text))
			encr_priv_key:bytes = b"".join(encr_priv_key)
			#encr_priv_key:str = encr_priv_key.decode()

			return encr_pub_key, encr_priv_key

		def getPathOS(path:list) -> str:
			if platform == 'android':
				# Android
				path:str = '/storage/'

			else:
				if platform == 'win':
					# Windows
					path:str = f'C:/Users/{path[2]}/Desktop/'

				elif platform == 'linux' or platform.upper() == 'MAC':
					# GNU/Linux
					path:str = f'/home/{path[2]}/Desktop/'

				if os.popen(f'dir {path}').close() == 512: # 512 means the directory not exist
					path = path.replace('/Desktop/', '/Escritorio/')

			return path

		def getValidNameForTheFiles(path:str):
			files = os.listdir(path)

			n = 1
			while True:
				if (not 'private.key' in files) and (not 'public.key' in files):
					return 'public.key', 'private.key'
					break

				elif (not f'private_({n}).key' in files) and (not f'public_({n}).key' in files):
					return f'public_({n}).key', f'private_({n}).key'
					break

				else:
					pass

				n += 1

		def genCert(info, normal_info:dict) -> tuple:
			# E N C R Y P T
			encrypted_info:dict = {}
			encrypted_info["user"] = info.encrypt(normal_info["user"].encode()).hex()
			encrypted_info["metamask"] = info.encrypt(normal_info["metamask"].encode()).hex()
			encrypted_info["password_(1)"] = info.encrypt(normal_info["password_(1)"].encode()).hex()
			encrypted_info["password_(2)"] = info.encrypt(normal_info["password_(2)"].encode()).hex()
			
			# H A S H
			hashed_info:dict = {}
			hashed_info["user"] = hashlib.sha224(normal_info["user"].encode()).hexdigest()
			hashed_info["metamask"] = hashlib.sha224(normal_info["metamask"].encode()).hexdigest()
			hashed_info["password_(1)"] = hashlib.sha224(normal_info["password_(1)"].encode()).hexdigest()
			hashed_info["password_(2)"] = hashlib.sha224(normal_info["password_(2)"].encode()).hexdigest()
			
			# S I G N
			signer = SigningKey.generate()
			signed_info:dict = {}
			signed_info["user"] = signer.sign(hashed_info["user"].encode())
			signed_info["user"] = signed_info["user"].signature.hex()

			signed_info["metamask"] = signer.sign(hashed_info["metamask"].encode())
			signed_info["metamask"] = signed_info["metamask"].signature.hex()

			signed_info["password_(1)"] = signer.sign(hashed_info["password_(1)"].encode())
			signed_info["password_(1)"] = signed_info["password_(1)"].signature.hex()

			signed_info["password_(2)"] = signer.sign(hashed_info["password_(2)"].encode())
			signed_info["password_(2)"] = signed_info["password_(2)"].signature.hex()

			return normal_info, encrypted_info, hashed_info, signed_info

		#cipher = PKCS1_OAEP.new (key=public_key)
		#cipher_text = cipher.encrypt(mensaje)
		#decrypt = PKCS1_OAEP.new (key=self.private_key)
		#dec_mnsj = decrypt.decrypt(cipher_text)

		# We continue to gen & save the certificates and information...
		os.system(f'mkdir "Certificados/{username}"')
		
		# Save the keys encrypted
		path = os.getcwd().replace('\\', '/')
		encrypted_keys:dict = {"public_key":genKeys()[0], "private_key":genKeys()[1]}
		with open(f"{path}/Certificados/{username}/keys.key", "w") as f:
			f.write(str(encrypted_keys))

		# We save a copy of the ecnrypted keys for the user in the desktop
		path = getPathOS(os.getcwd().replace('\\', '/').split('/'))
		name = getValidNameForTheFiles(path)
		with open(f"{path}/{name[0]}", "w") as f:
			f.write(f"'public_key': {self.public_key}")

		with open(f"{path}/{name[1]}", "w") as f:
			f.write(f"'private_key': {encrypted_keys['private_key']}")	
		##
		normal_info:dict = {
			"user": username,
			"metamask": metamask,
			"password_(1)": password,
			"password_(2)": password2
		}

		info = PKCS1_OAEP.new (key=self.public_key)

		cert = genCert(info, normal_info)

		info:dict = {
			"normal":cert[0],
			"cifrado":cert[1],
			"hash":cert[2],
			"sign":cert[3]
		}

		# Creating certificate
		with open(f"Certificados/{username}/user.cert", "w") as f:
			f.write(str(info))
		
		self.empty(self.ids.username, self.ids.metamask, self.ids.password, self.ids.password2, self.ids.cert_information) # Vacia los campos de la ventana
		app.root.current = 'home'
		#
	