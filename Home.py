from kivy.uix.screenmanager import Screen

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton


class Home(Screen):
	def __init__(self, **kwargs):
		super(Home, self).__init__(**kwargs)


	def openDialog(self, title:str, text:str):
		self.dialog = MDDialog(
			title=title,
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text='Aceptar',
					on_press=self.closeDialog
				)
			]
		)
		self.dialog.open()

	def closeDialog(self, *args):
		self.dialog.dismiss()