VAR = "x"
EOS = "$"
NUMS = "012345789"
OPS = "+*/-^"
TRIG = "sct"

class Lexer:

	def __init__(self):		
		pass
		
	def Lex(self, text):
	
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
				
			# Add any single char as necessary:
			elif char in VAR + OPS: 
				token = char		
			#print(last,char)		
			
			if char != EOS: explicit_text.append(token)
			
			last = char			
			i += 1

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
			build_num = True
		
		return cur_num
				
	def _parse_trig(self, text, index):
		'''Parses trig functions returns a string'''		
		cur_trig = ""
		i = index
		char = text[i]
		
		while char in NUMS:
			cur_num += char		
			i += 1		
			char = text[i]
			build_num = True
		
		return cur_num

def test(result, expect):	
	try:
		assert result == expect		
	except AssertionError as e:
		print("Test failed...")
		print("  Expected:\t" + str(expect))
		print("  Received:\t"+str(result))
	

if __name__ == "__main__":
	foo = Lexer()
	test(foo.Lex("20x*300"),	  ['20','*','x','*','300'])
	test(foo.Lex("20x*300+45-2"), ['20','*','x','*','300','+','45','-','2'])
