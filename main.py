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



#from PIL import Image
#img = Image.open(f'{os.getcwd()}/images/hacker.png')
#img = img.resize((590, 640), Image.ANTIALIAS)
#img.save('images/hacker.png')


class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)


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
		
		#app.root.current = 'join'

		os.system('mkdir Certificados')
		app.resizeWindow(
			size=(1200, 680),
			left=100,
			top=1
		)
		
# PARA QUE FUNCIONE, SE REQUIERE TENER INSTALADA GANACHE #

###################################################
#                  P E N D I E N T E S            #
# +++++++++++++++++++++++++++++++++++++++++++++++ #
#              Agregar botones de ayuda           #
# ############################################### #
#                        H O M E                  #
# 1.                                              #
# ----------------------------------------------- #
#                        J O I N                  #
#                                                 #
# ----------------------------------------------- #
#                       L O G I N                 #
# 1.                                              #
# ----------------------------------------------- #
#                M E S S E N G E R                #
# 1.                                              #
###################################################

if __name__ == "__main__":
	main().run()