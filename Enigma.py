import re


def rotorOne()->list:
	rotor:str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	subrotor:str = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
	return [list(rotor), list(subrotor)]


def rotorTwo()->list:
	rotor:str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	subrotor:str = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
	return [list(rotor), list(subrotor)]


def rotorThree()->list:
	rotor:str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	subrotor:str = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
	return [list(rotor), list(subrotor)]


def verifyMsg(msg:str)->str:
	re_expression = re.compile(r"[A-Z]+")
	if re_expression.fullmatch(msg):
		msg:str = msg
	else:
		msg:str = ""

	return str(msg)


def verifyKey(key:str)->str:
	re_expression = re.compile(r"[A-Z]{3}")
	if re_expression.fullmatch(key):
		key:str = key
	else:
		key:str = ""

	return str(key)


def verifyRotors(rotors_position:str)->list:
	re_expression = re.compile(r"(1 2 3|1 3 2|2 1 3|2 3 1|3 1 2|3 2 1)")
	if re_expression.fullmatch(rotors_position):
		rotors_position:list = list(rotors_position)
		rotors_position.remove(" ")
		rotors_position.remove(" ")
		for i in range(3):
			if rotors_position[i] == "1":
				rotors_position[i] = rotorOne()

			elif rotors_position[i] == "2":
				rotors_position[i] = rotorTwo()

			elif rotors_position[i] == "3":
				rotors_position[i] = rotorThree()

	else:
		rotors_position:list = []

	return list(rotors_position)


def scrollAlphabet(alphabet:list)->list:
	for i in range(len(alphabet)):
		if i < len(alphabet)-1:
			(alphabet[i], alphabet[i+1]) = (alphabet[i+1], alphabet[i])
		else:
			break
	
	return list(alphabet)


def setRotorPosition(rotor:list, key:str)->list:
	while rotor[0][0] != key:
		rotor[0] = scrollAlphabet(rotor[0])
		rotor[1] = scrollAlphabet(rotor[1])

	return list(rotor)


def movingUsToTheReflector(letter:str, reflector:list, left_rotor:list, 
	middle_rotor:list, right_rotor:list,input_output:list)->str:
	# We find the position of our letter
	pos_first_letter:int = input_output.index(letter)

	# We move to right rotor
	letter_right_1:str = right_rotor[1][pos_first_letter]
	
	# We look for its equal
	pos_letter_right_2:int = right_rotor[0].index(letter_right_1)
	letter_right_2:str = right_rotor[0][pos_letter_right_2]
	
	# We move to middle rotor
	pos_letter_middle_1:int = pos_letter_right_2
	letter_middle_1:str = middle_rotor[1][pos_letter_middle_1]
	
	# We look for its equal
	pos_letter_middle_2:int = middle_rotor[0].index(letter_middle_1)
	letter_middle_2:str = middle_rotor[0][pos_letter_middle_2]
	
	# We move to left rotor
	pos_letter_left_1:int = pos_letter_middle_2
	letter_left_1:str = left_rotor[1][pos_letter_left_1]
	
	# We look for its equal
	pos_letter_left_2:int = left_rotor[0].index(letter_left_1)
	letter_left_2:str = left_rotor[0][pos_letter_left_2]
	
	# We move to reflector
	letter_reflector_1:int = reflector[pos_letter_left_2]
	
	# We search for its equal
	for j in range(len(reflector)):
		if reflector[j] == letter_reflector_1 and j != pos_letter_left_2:
			pos_letter_reflector_2:int = j
			break
	letter_reflector_2:str = reflector[j]
	
	return [letter_reflector_2, pos_letter_reflector_2]


def movingUsToTheOutput(letter:str, reflector:list, pos_reflector:int, 
	left_rotor:list, middle_rotor:list, right_rotor:list, input_output:list):
	# We move to left rotor 
	pos_letter_left_2:int = pos_reflector
	letter_left_2:str = left_rotor[0][pos_letter_left_2]
	
	# We search for its equal
	pos_letter_left_1:int = left_rotor[1].index(letter_left_2)
	letter_left_1:str = left_rotor[1][pos_letter_left_1]
	
	# We move to middle rotor
	pos_letter_middle_2:int = pos_letter_left_1
	letter_middle_2:str = middle_rotor[0][pos_letter_middle_2]
	
	# We search for its equal
	pos_letter_middle_1:int = middle_rotor[1].index(letter_middle_2)
	letter_middle_1:str = middle_rotor[1][pos_letter_middle_1]
	
	# We move to right rotor
	pos_letter_right_2:int = pos_letter_middle_1
	letter_right_2:str = right_rotor[0][pos_letter_right_2]
	
	# We search for its equal
	pos_letter_right_1:int = right_rotor[1].index(letter_right_2)
	letter_right_1:str = right_rotor[1][pos_letter_right_1]
	
	# We move to output
	output:str = input_output[pos_letter_right_1]
	
	return output


def enigma(msg:str, key:str, rotor_position:str)->str:
	msg:str = verifyMsg(msg)
	key:str = verifyKey(key)
	rotors_position:list = verifyRotors(rotor_position)
	reflector:list = list("ABCDEFGDIJKGMKMIEBFTCVVJAT")
	input_output:list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	final_msg:str = ""

	if msg != "" and key != "" and rotors_position != []:
		left_rotor:list = setRotorPosition(rotors_position[0], key[0])
		count_left_rotor:int = 0

		middle_rotor:list = setRotorPosition(rotors_position[1], key[1])
		count_middle_rotor:int = 0

		right_rotor:list = setRotorPosition(rotors_position[2], key[2])
		count_right_rotor:int = 0

		for i in range(len(msg)):
			count_right_rotor += 1
			right_rotor[0] = scrollAlphabet(right_rotor[0])
			right_rotor[1] = scrollAlphabet(right_rotor[1])
			
			if count_right_rotor == 26:
				count_right_rotor = 0

				count_middle_rotor += 1
				middle_rotor[0] = scrollAlphabet(middle_rotor[0])
				middle_rotor[1] = scrollAlphabet(middle_rotor[1])
				
				if count_middle_rotor == 26:
					count_middle_rotor = 0

					count_left_rotor += 1
					left_rotor[0] = scrollAlphabet(left_rotor[0])
					left_rotor[1] = scrollAlphabet(left_rotor[1])

					if count_left_rotor == 26:
						count_left_rotor = 0
			
			going:list = movingUsToTheReflector(msg[i], reflector, left_rotor, 
				middle_rotor, right_rotor, input_output)
			comming_back:str = movingUsToTheOutput(going[0], reflector, going[1], left_rotor,
				middle_rotor, right_rotor, input_output)
			final_msg = final_msg + comming_back

	print(msg, key, rotors_position)
	return final_msg