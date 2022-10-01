import codecs


def desencriptar(texto, llave): # recibe el texto y la llve a utilizar
	# restamos los bits
	cadena_decifrada = []
	cadena_texto_plano = ''
	for i in texto:
		cadena_decifrada.append(chr((int(i) - int(llave)) % 256))

	for i in cadena_decifrada:
		cadena_texto_plano += i

	return cadena_texto_plano

def encriptar(texto, llave):
	cadena_cifrada = []
	cadena_cifrada_texto = ''

	for letra in texto:
		# hacemos la rotacion, convertimos a bytes y apendamos

		cadena_cifrada.append(((letra + llave)%256).to_bytes(1, byteorder='big')) # usar este en caso de manejar int
		#cadena_cifrada.append(((ord(letra) + 112)%256).to_bytes(1, byteorder='big')) # usar este en caso de manejar str

	#guardamos los bytes en un archivo llamado texto_cifrado.lock
	with open('texto_cifrado.lock', 'wb') as f:
		for letra in cadena_cifrada:
			f.write(letra)
	
	return cadena_cifrada

def encriptarString(texto, llave):
	cadena_cifrada = []
	cadena_cifrada_texto = ''

	for letra in texto:
			# hacemos la rotacion, convertimos a bytes y apendamos

			cadena_cifrada.append(((ord(letra) + 112)%256).to_bytes(1, byteorder='big')) # usar este en caso de manejar str
	
	for letra in cadena_cifrada:
		#cadena_cifrada_texto += str(letra)[1:] + ' '
		cadena_cifrada_texto += str(letra) + ' '
		#print(int.fromhex(letra[1:]))

	return cadena_cifrada_texto