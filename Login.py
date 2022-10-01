from kivy.uix.screenmanager import Screen

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.filemanager import MDFileManager
from kivy.utils import platform

from Rot13 import *

import json
import os
import re


class Login(Screen):
	def __init__(self, **kwargs):
		super(Login, self).__init__(**kwargs)

		global app
		app = MDApp.get_running_app()

		self.directory = MDFileManager(
			select_path=self.selectFileFromDirectory,
			exit_manager=self.exitFromDirectory,
		)


	def openDialog(self, title:str, text:str)->None:
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


	def selectFileFromDirectory(self, path):
		path = path.replace('\\', '/')
		#last = path.split('/')
		#last = last[len(last)-1]

		self.exitFromDirectory()
		self.ids.private_key_location.text = path


	def exitFromDirectory(self, *args):
		self.directory.close()


	def openDirectory(self):
		if platform == 'android':
			self.directory.show(primary_ext_storage)
		
		elif platform == 'win':
			self.directory.show('C:/Users')

		else:
			self.directory.show('/home/')


	def getCertificates(self):
		certs = os.listdir("Certificados/")

		return certs

	def checkPassword(self, username:str, n:int, passn:str):
		try:
			with open(f"Certificados/{username}/user.cert", "r") as f:
				content_file:str = f.read()

			content_file = content_file.replace("'", "\"")
			content_file = content_file.replace("b\"", "\"")

			data = json.loads(content_file)


			if n == 1:
				if data["normal"]["password_(1)"] == passn:
					password = True
				else:
					password = False

			if n == 2:
				if data["normal"]["password_(2)"] == passn:
					password = True
				else:
					password = False
		except:
			password = False

		return password


	def verifyData(self, name):
		folders = os.getdirs("Certificados")
		if name in folders:
			with open(f"Certificados/{name}/keys.key", "r") as f:
				data = f.read()
			data = data.replace("'", "\"")
			information = json.loads(data)
	

	def login(self, username, pass1, pass2, private_key_location) -> None:
		def emptyFields(username:str, pass1:str, pass2:str, private_key_location:str) -> bool:
			if username == "" and pass1 == "" and pass2 == "" and private_key_location == "":
				return True # one or more empties

			else:
				return False # Those have a content

		def userExist(username:str) -> bool:
			if username in os.listdir("Certificados/"):
				return True

		def passwordMatch(username:str, pass1:str, pass2:str):
			def correctPassword(username:str, n:int, passn:str):
				try:
					with open(f"Certificados/{username}/user.cert", "r") as f:
						content_file:str = f.read()

					content_file = content_file.replace("'", "\"")
					content_file = content_file.replace("b\"", "\"")

					data = json.loads(content_file)


					if n == 1:
						if data["normal"]["password_(1)"] == passn:
							return True
						else:
							return False

					if n == 2:
						if data["normal"]["password_(2)"] == passn:
							
							return True
						else:
							return False
				except:
					return False

			if correctPassword(username, 1, pass1) and correctPassword(username, 2, pass2):
				return True

			else:
				return False

		def getContentFile(path:str):
			try:
				with open(path, "rb") as f:
					data = f.read()

				encrypted_key = data[17:len(data)-2]

				print('GET CONTENT FILE')
				print(encrypted_key)

				return encrypted_key

			except:	
				return None

		def locate_key(path:str):
			try:
				get_encrypted_key = re.compile(r"'private_key': b'(.*?)+'")
				with open(path, "r") as f:
					data = f.read()
				
				get_encrypted_key = get_encrypted_key.search(str(data))

				encrypted_key = get_encrypted_key.group(0)
				encrypted_key = encrypted_key.encode()
				encrypted_key = encrypted_key[17:len(encrypted_key)-2]

				return encrypted_key
			except Exception as e:
				# print(e)
				
				return None

		def getMetamaskAccount(username:str):
			with open(f"Certificados/{username}/user.cert", "r") as f:
				content_file:str = f.read()

			content_file = content_file.replace("'", "\"")
			content_file = content_file.replace("b\"", "\"")

			data = json.loads(content_file)

			return data['normal']['metamask']
		###

		if not emptyFields(self.ids.username.text, self.ids.pass1.text, self.ids.pass2.text, self.ids.private_key_location.text):			
			if userExist(username.text):
				if passwordMatch(username.text, pass1.text, pass2.text):
					private_key_user:str = self.ids.private_key_location.text

					encrypted_key_user:str = getContentFile(private_key_user)
					decrypted_key_user:str = ""
					if encrypted_key_user != None:
						decrypted_key_user = desencriptar(encrypted_key_user, len(self.ids.pass2.text))
					
						# We repeat the "same"
						encrypted_key_cert:str = locate_key(f"{os.getcwd()}/Certificados/{self.ids.username.text}/keys.key")
						decrypted_key_cert:str = ""
						if encrypted_key_cert != None:
							decrypted_key_cert:str = desencriptar(encrypted_key_cert, len(self.ids.pass2.text))

							if decrypted_key_user != "" and decrypted_key_cert != "":
						
								if decrypted_key_user == decrypted_key_cert:
									app.root.current = 'en_de'
									app.resizeWindow(
										size=(1200, 650),
										left=1200,
										top=1
									)
									app.root.get_screen('en_de').ids.cuenta_eth.text = getMetamaskAccount(username.text)
									self.clear()

								else:
									self.openDialog(
										title='Son diferentes',
										text='Checalas'
									)
									print('dec_key_user', decrypted_key_user)
									print('dec_key_cert', decrypted_key_cert)

							else:
								self.openDialog(
									title='Error',
									text='Lo sentimos, a ocurrido un error al desencriptar las contraseñas.'
								)

						else:
							self.openDialog(
								title='Error',
								text='Lo sentimos, ha ocurrido un error con el certificado de nuestra base de datos.'
							)
					else:
						self.openDialog(
							title='Error',
							text='Lo sentimos, ha ocurrido un error con el archivo seleccionado.'
						)

				else:
					self.openDialog(
						title='Error.',
						text='La(s) contraseña(s) no coincide(n).'
					)
			else:
				self.openDialog(
					title='Error.',
					text='El usuario no existe. Por favor, verifique que los datos hayan sido agregados correctamente.'
				)

		else:
			self.openDialog(
				title='Atención',
				text='Debe de llenar todos los campos.'
			)
			

	def clear(self):
		self.ids.username.text = ""
		self.ids.pass1.text = ""
		self.ids.pass2.text = ""
		self.ids.private_key_location.text = ""

		self.ids.username.disabled = False
		self.ids.pass1.disabled = False
		self.ids.pass2.disabled = False
		self.ids.private_key_location.disabled = False

		self.ids.log_in.disabled = True