import random
import math

range_low = pow(10, 14)
range_high = pow(10, 15)

bit_size = 8

def generate_random_number(a, b):
	return random.randrange(a, b)

def check_prime(random_number):
	if random_number < 2:
		return False

	if random_number == 2:
		return True

	if random_number % 2 == 0:
		return False

	for number in range(3, round(math.sqrt(random_number)) + 1, 2):
		if random_number % number == 0:
			return False

	return True

def check_prime_rabinmiller(random_number, k):
	if random_number < 2:
		return False

	if random_number == 2:
		return True

	if random_number % 2 == 0:
		return False

	n = random_number - 1

	count = 0
	while n % 2 == 0:
		n = n // 2
		count += 1

	d = n
	s = count

	for i in range(k):
		# 2 <= x <= num
		a = random.randrange(2, random_number - 1)

		x = pow(a, d, random_number)

		if x == 1 or x == random_number - 1:
			continue

		for j in range(s - 1):
			x = pow(x, 2, random_number)

			if x == random_number - 1:
				break
		else:
			return False
	return True

def multiply(p, q):
	return p * q

def over_gcd(n, i):
	return math.gcd(n, i) == 1

def euler(p, q):
	return (p - 1) * (q - 1)

def get_euler_e(phi):
	e = 65537

	if over_gcd(e, phi):
		return e

	while True:
		e = generate_random_number(2, phi)

		if over_gcd(e, phi):
			return e

def find_inverse(e, phi):
	return pow(e, -1, phi)

def encrypt(plain_text, public_key):
	n, e = public_key
	blocks = split_into_blocks(plain_text)

	ciphered_text = ""
	binary_text = ""
	for block in blocks:
		ascii_text = convert_to_ascii(block)
		binary_array = convert_ascii_to_binary(ascii_text)
		m = convert_binary_to_decimal(binary_array)
		binary_text += "".join(str(binary_array)) + " "
		ciphered_text += str(pow(m, e, n)) + " "


	if binary_text[-1] == " ":
		binary_text = binary_text[:-1]

	if ciphered_text[-1] == " ":
		ciphered_text = ciphered_text[:-1]

	return ciphered_text, binary_text

def generate_keys():
	p, q = 0, 0
	while p == 0 or q == 0:
		random_number = generate_random_number(range_low, range_high)
		if check_prime(random_number):
			if p == 0:
				p = random_number
			elif random_number != p:
				q = random_number

	n = multiply(p, q)
	phi = euler(p, q)
	e = get_euler_e(phi)
	d = find_inverse(e, phi)

	private_key = (n, d)
	public_key = (n, e)

	return private_key, public_key

def decrypt(cipher_text, private_key):
	n, d = private_key
	blocks = get_blocks(cipher_text)
	decrypted_text = ""
	for block in blocks:
		decrypted_block = decrypt_block(int(block), d, n)
		binary_text = convert_decimal_to_binary(decrypted_block).zfill(bit_size * bit_size)
		ascii_values = convert_binary_to_ascii(binary_text)
		decrypted_text += convert_ascii_to_text(ascii_values).lstrip("\x00") # odstran null character

	return decrypted_text


def split_into_blocks(plain_text):
	blocks = []
	index = 0
	count = 0
	new_text = ""
	while index < len(plain_text):
		if count < bit_size:
			new_text += plain_text[index]
			count += 1
			index += 1
		else:
			blocks.append(new_text)
			new_text = ""
			count = 0

	if new_text:
		blocks.append(new_text)

	return blocks

def convert_to_ascii(string):
	ascii_values = []
	for char in range(len(string)):
		ascii_values.append(ord(string[char]))

	return ascii_values

def convert_ascii_to_binary(ascii_values):
	string = ""
	new_string = ""
	for value in ascii_values:
		binary = format(value, '08b')
		string += binary

	if len(string) != bit_size*bit_size:
		l = bit_size*bit_size - len(string)

		new_string += "0" * l + string
	else:
		new_string = string

	return new_string

def convert_binary_to_decimal(binary):
	return int(binary, 2) # 2 <- znamena ze text je v bin forme

def convert_binary_to_ascii(binary):
	binary_values = []

	count = 0
	index = 0
	ascii_text = ""
	while index < len(binary):
		if count < bit_size:
			ascii_text += binary[index]
			count += 1
			index += 1
		else:
			binary_values.append(int(ascii_text, 2))
			ascii_text = ""
			count = 0

	if ascii_text:
		binary_values.append(int(ascii_text, 2))

	return binary_values

def convert_ascii_to_text(binary_values):
	text = ""

	for i in binary_values:
		text += chr(i)

	return text

def get_blocks(cipher_text):
	return cipher_text.split()

def decrypt_block(ciphered_block, d, n):
	return pow(ciphered_block, d, n)

def convert_decimal_to_binary(decimal):
	return format(decimal, 'b')

def normalize_text(text):
	text = text.replace("á", "a").replace("ä", "a")
	text = text.replace("č", "c").replace("ď", "d")
	text = text.replace("é", "e").replace("í", "i")
	text = text.replace("ĺ", "l").replace("ľ", "l")
	text = text.replace("ň", "n").replace("ó", "o")
	text = text.replace("ô", "o").replace("ŕ", "r")
	text = text.replace("š", "s").replace("ť", "t")
	text = text.replace("ú", "u").replace("ý", "y")
	text = text.replace("ž", "z")

	text = text.replace("Á", "A").replace("Ä", "A")
	text = text.replace("Č", "C").replace("Ď", "D")
	text = text.replace("É", "E").replace("Í", "I")
	text = text.replace("Ĺ", "L").replace("Ľ", "L")
	text = text.replace("Ň", "N").replace("Ó", "O")
	text = text.replace("Ô", "O").replace("Ŕ", "R")
	text = text.replace("Š", "S").replace("Ť", "T")
	text = text.replace("Ú", "U").replace("Ý", "Y")
	text = text.replace("Ž", "Z")

	ascii = "".join(chr(i) for i in range(32, 127))

	novy_text = ""
	for znak in text:
		if znak in ascii:
			novy_text += znak

	return novy_text