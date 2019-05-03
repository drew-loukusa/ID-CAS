VAR = "x"
EOS = "$"
NUMS = "012345789"
OPS = "+*/-^"
TRIG = "sct"

# TODO: Add support for natural log, and the other trig functions

class Lexer:

	def __init__(self):		
		pass

	def Lex(self, text):
		tokens = self._split_text(text)
		tokens = self._apply_ids(tokens)
		return tokens

	def _apply_ids(self, tokens):
		tokens_and_ids = []

		for token in tokens:

			token_id = ""

			if token in "+-":
				token_id = "PLUS_OP"

			elif token in "*/":
				token_id = "MULT_OP"

			elif token == "^": 
				token_id = "EXP_OP"

			elif token == VAR:
				token_id = "IDENT"				

			elif self._is_number(token):
				token_id = "NUM"			

			elif token == "ln":
				token_id = "LN"	

			elif self._is_trig(token):
				token_id = "TRIG"

			elif token in "()":
				token_id = "PAREN"

			elif token == '$':
				token_id = "EOS"
		
			tokens_and_ids.append((token_id,token))
	
		return tokens_and_ids		

	def _split_text(self, text):
	
		#Add EOS char to string:
		text = text + "$"
	
		# Insert explicit multiplication symbols: 
		text = self._insert_explicit_mult(text)
		#print(text)

		char = ""
		last = None	
		cur_num = ""		
		explicit_text = []

		# ==================== Split Text into Tokens: ====================== #
		i = 0
		token = ""
		while i < len(text):
			char = text[i]			
			#print(last,char, i)		

			# ------------- Handle Multi Digit Numbers ------------- #
			if char in NUMS:
				token = self._parse_num(text, i)		
				#print("\t",i, token)
				i += len(token) - 1
				#print("\t",i)				
				char = text[i]
				
			# ------------- Handle Trig Functions ------------------ #
			elif char in TRIG:
				token = self._parse_trig(text, i)		
				i += len(token) - 1
				#print("\t",i)				
				char = text[i]
			
			elif char in "ln":
				token = "ln"
				i += 1
				char = text[i]
				
			# Add any single char as necessary:
			elif char in VAR + OPS + "()": 
				token = char		
			#print(last,char)		
			
			if char != EOS: explicit_text.append(token)
			
			last = char			
			i += 1

		explicit_text.append("$")
		return explicit_text

	def _insert_explicit_mult(self, text):
		i = 0
		char = text[i]
		last = None
		text = list(text)
		while char != "$":					

			# If we have a VAR and a NUM next to each other, insert a mult op:
			# 	This handles left and right associativity: "x5" and "5x"
			if last and ((char in NUMS and last in VAR) or
						 (char in VAR and last in NUMS)):			
				text.insert(i, "*")		

			# Handle left and right associativity on parens and nums:
			if last and ((char in NUMS and last in ")") or
						 (char in "(" and last in NUMS)):			
				text.insert(i, "*")	

			# Handle left and right associativity on parens and vars:
			if last and ((char in VAR and last in ")") or
						 (char in "(" and last in VAR)):						
				text.insert(i, "*")	

			i += 1
			last = char
			char = text[i]
		textstr = ""
		for char in text: textstr+=char
		return textstr

	def _parse_num(self, text, index):
		'''Parses multi-digit numbers and returns them'''		
		cur_num = ""
		i = index
		char = text[i]
		
		while char in NUMS:
			cur_num += char		
			i += 1		
			char = text[i]			
		
		return cur_num
		
	def _parse_trig(self, text, index):
		'''Parses trig functions returns a string'''		
		cur_trig = ""
		i = index
		char = text[i]
		j = 0
		while j < 3:
			cur_trig += char		
			i += 1		
			j += 1
			char = text[i]			
		
		return cur_trig

	def _is_number(self, string):
		try:
			float(string)
			return True
		except ValueError:
			return False

	def _is_trig(self, string):
		if string in ["sin", "cos", "tan"]: 
			return True
		else: 
			return False

def test(result, expect):	
	try:
		assert result == expect		
	except AssertionError as e:
		print("Test failed...")
		print("  Expected:\t" + str(expect))
		print("  Received:\t"+str(result))
	

if __name__ == "__main__":
	foo = Lexer()
	print(foo.Lex("20x*300+45-2"))
	print(foo.Lex("20x*300+45-2sin(x)"))

	#test(foo.Lex("20x*300*sin(x)"), ['20','*','x','*','300','*','sin','(','x',')','$'])
	#test(foo.Lex("20x*300+45-2"), ['20','*','x','*','300','+','45','-','2'])	
