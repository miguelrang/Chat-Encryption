#!/usr/bin/env python3
from kivy.config import Config
Config.set("graphics", "resizable", False)

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window

from nacl.signing import SigningKey
#from nacl.hash import blake2b

import hashlib
import random
import json
import os
import re

from Home import Home
from Login import Login
from Join import Join
from Messenger import Messenger


class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)

# AQUI ES DONDE TOMAMOS EL ARCHIVO Y LO MANIPULAMOS
class FChooser(Screen):
	def __init__(self, **kwargs):
		super(FChooser, self).__init__(**kwargs)
		self.file_data = "" # bloquea y desbloquea el boton de agregar archivo dependiendo de su contenido
		

	def selected(self, file:list):

		try: 
			global direccion # marcamos como global la variable para guardar la direccion del archivo
			global contenido # marcamos como global la variable donde guardamos el contenido
			self.file_data = file[0]
			
			direccion = file[0]
			with open(direccion, 'rb') as f:
				
				for byte in f.read(): # guardamos el contenido en una variable
					contenido.append(byte)
				
			
			
		except:
			self.file_data = ""

		if self.file_data != "":
			self.ids.adding.disabled = False

		else:
			self.ids.adding.disabled = True


class main(MDApp):
	def build(self):
		#self.icon = "images/logo.png"
		self.title = "Cifrado de Mensajes"	
		
		kv = ScreenManager()

		kv.add_widget(Builder.load_file("Home.kv"))
		kv.add_widget(Builder.load_file("Join.kv"))
		kv.add_widget(Builder.load_file("Login.kv"))
		kv.add_widget(Builder.load_file("Messenger.kv"))

		return kv


	def resizeWindow(self, size:tuple, left:int, top:int):
		Window.size = size
		Window.left = left
		Window.top = top


	def on_start(self):
		app = MDApp.get_running_app()
		
		app.root.current = 'home'

		os.system('mkdir Certificados')
		self.resizeWindow(
			size=(500, 600),
			left=400,
			top=2
		)
		

###################################################
#                  P E N D I E N T E S            #
# +++++++++++++++++++++++++++++++++++++++++++++++ #
#              Agregar botones de ayuda           #
# ############################################### #
#                        H O M E                  #
# 1.                                              #
# ----------------------------------------------- #
#                        J O I N                  #
# 1. Validar que el usuario o cuenta ya haya sido #
#    registrada.                                  #
# 2. Validar si ya existe un archivo private.key o#
#    public.key en el escritorio.                 #
# 3. Agregar una expresión regular que valide que #
#    se haya agregado una cuenta de metamask y su #
#    contraseña.
# ----------------------------------------------- #
#                       L O G I N                 #
# 1. Importar primary external storage.           #
# 2. Solucionar error al presionar login.         #
# 3. Agregar el nombre de usuario luego de login. #
# ----------------------------------------------- #
#                M E S S E N G E R                #
# 1.                                              #
###################################################

if __name__ == "__main__":
	# variables globales para guardar los datos
	global normal_info
	normal_info = {}
	direccion = '' # aqui guardamos la direccion
	contenido = [] # aqui guardamos el contenido del archivo
	main().run()