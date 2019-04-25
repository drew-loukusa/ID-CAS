
class Lexer:

	def __init__(self):
		self.x = 0
	
	def Lex(self, text):

		NUMS = "012345789"
		VAR = "x"
		OPS = "+*/-^"
		EOS = "$"

		#Add EOS char to string:
		text = text + "$"

		last = None	
		build_num = False
		cur_num = ""


		explicit_text = []

		# =============== Transform Text ============== #		
		for char in text:
			# ------------- Handle Multi Digit Numbers ------------- #
			if char in NUMS:
				print(last,char, build_num)
				
				# If the last char was a num -> Keep building num:				
				if last and (last in NUMS and char in NUMS):
					cur_num += char
					
				# If last NOT a num -> Start building the number:
				if cur_num == "": 
					cur_num = char
					build_num = True					

			# If we were building a multi-digit number and it ends,
			# Then add it to the list of tokens and reset the vars
			if (char in OPS or char in VAR or char in EOS) and build_num:
				build_num = False
				explicit_text.append(cur_num)	
				cur_num = ""
				

			# -------- Insert explicit multiplication symbols: --------- #

			# If we have a VAR and a NUM next to each other, insert a mult op:
			# 	This handles left and right associativity: "x5" and "5x"
			if last and ((char in NUMS and last in VAR) or
						 (char in VAR and last in NUMS)):			
				explicit_text.append("*")

			# Set cur char to last char to allow for multi-char tokens:
			last = char			

			# If we're building a number, then we don't
			# want to add it to the token list yet:
			if not build_num and char != EOS: 
				explicit_text.append(char)

		return explicit_text

	

if __name__ == "__main__":
	foo = Lexer()
	print(foo.Lex("x20*300"))