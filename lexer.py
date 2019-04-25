
class Lexer:

	def __init__(self):
		self.x = 0
	
	def Lex(self, text):

		NUMS = "012345789"
		VAR = "x"
		OPS = "+*/-^"

		last = None	
		build_num = False
		cur_num = ""


		explicit_text = []

		# =============== Transform Text ============== #		
		for char in text:

			# ------------- Handle Multi Digit Numbers ------------- #
			if char in NUMS:
				
				# Last char was op or var:				
				if last and (last in NUMS and char in NUMS):
					cur_num += char
					
				if cur_num == "": 
					cur_num = char
					build_num = True					

			if char in OPS or char in VAR:
				build_num = False
				cur_num == ""
				explicit_text.append(cur_num)	
				

			# -------- Insert explicit multiplication symbols: --------- #

			# If have a VAR and a NUM next to each other, insert a mult op:
			if last and ((char in NUMS and last in VAR) or
						 (char in VAR and last in NUMS)):			
				explicit_text.append("*")




			last = char
			if not build_num: explicit_text.append(char)




		# =============== Transform Text ============== #



		return explicit_text

	

if __name__ == "__main__":
	foo = Lexer()
	print(foo.Lex("x20"))