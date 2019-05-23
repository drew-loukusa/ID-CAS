#!/usr/bin/python3
#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral(?) calculator.			   #
#																			   #
#==============================================================================#

import argparse
from sys import stdout as std, argv
from colorama import Fore, Back, Style 	

# Setup and parse args:
INPUT_EXPRESSION = None
INTERACTIVE_MODE = False
DEBUG = False
p = argparse.ArgumentParser()
add = p.add_argument
add('-expr', dest='input_expression', default=INPUT_EXPRESSION, help="Runs calculator with the given input expression")
add('-d', dest='debug', action="store_true", help="Displays debug info: Token stream, expression tree...")
args = p.parse_args()

def main(input_expression=INPUT_EXPRESSION, debug=DEBUG):	
	#================================== Header ===============================#
	print(Fore.BLUE+"┌"+78*"-"+"┐")	
	std.write("|"+Fore.RED+"Derivative Calculator".center(78, " ")+Fore.BLUE+"|\n")	
	print("└"+78*"-"+"┘")
	print(Style.RESET_ALL) 		
	
	# Run in interactive mode if no expression given on startup 
	if input_expression is None:
		run = True
		while run:			
			run = calculate(None, interactive_mode=True, debug=debug)
	else:
		calculate(input_expression, interactive_mode=False, debug=debug)

def calculate(input_string, interactive_mode=False, debug=False):
	if interactive_mode: 
		print("Enter an expression to differentiate: (Type 'quit' to quit)")
		input_string = input(">>> ")

	if input_string == "quit":
		quit()

	#====================== Input Info + Preprocessing =======================#
	print(Fore.GREEN+"Input Information:"+Style.RESET_ALL)
	print(80*"-")
	print(Fore.GREEN+"Input String:"+Style.RESET_ALL,input_string)
	
	# Lex the input string into tokens:
	#-------------------------------------------------------------------------#
	from lexer import Lexer 
	foo = Lexer()
	token_stream = foo.lex(input_string)	
	if not token_stream: quit()
	#-------------------------------------------------------------------------#
	
	if debug:
		print(Fore.GREEN+"\nToken Stream:"+Style.RESET_ALL)
		
		# Print the token stream: 
		cur_line_length = 0
		for token in token_stream:
			s = str(token)
			if len(s) + cur_line_length > 80:
				std.write("\n")	
				cur_line_length = 0
			std.write(s+", ")
			cur_line_length += len(s)

	
	#print("Input String Length:", len(args[1]))	
	
	# Build The Expression Tree: 
	#-------------------------------------------------------------------------#
	from tree import Expression, initilize, print_tree, reset_seen, print_normalized_expression 
	initilize(token_stream)
	root = Expression(debug=False)
	#-------------------------------------------------------------------------#

	#print(Fore.GREEN+"\nNumber of nodes:"+Style.RESET_ALL, count_nodes( root ))
	reset_seen( root )
	
	if debug:
		print(Fore.GREEN+"\nNormalized input string:"+Style.RESET_ALL	)
		print_normalized_expression( root ) 
		print("\n")

		print(80*"-")
		print(Fore.GREEN+"Input Expression Tree:"+Style.RESET_ALL)
		print_tree( root )
		print()
		
		#print(80*"=")
		#print("Tree Dump:\n")
		#dump_tree(root, 0)
		#print(80*"-")
		
		#return 0
	
	#======================== Derivative Calculating =========================#
	
	from derivative import find_derivative, find_integral, simplify, simplify_mult
	
	# Differentiate the expression:
	#-------------------------------------------------------------------------#
	result = find_derivative( root )
	#result = find_integral( root )
	#-------------------------------------------------------------------------#

	if debug:
		print(80*"-")
		print(Fore.GREEN+"Derivative Result Tree:"+Style.RESET_ALL)
		print_tree( result )

		# print("\nResult Tree Dump:")
		# dump_tree(result,0)
		
		print(80*"-")	
		print(Fore.GREEN+"Derivative Result Expression:"+Style.RESET_ALL)
		print_normalized_expression( result )
		print("\n")
	
	# Simplify the result expression tree:
	#-------------------------------------------------------------------------#
	simp = simplify( result )
	#-------------------------------------------------------------------------#

	# Reduce coeffecients:
	#-------------------------------------------------------------------------#
	simp = simplify_mult( simp )
	simp = simplify( simp ) #, direction=None, parent=None, debug=True)
	#-------------------------------------------------------------------------#

	if debug:
		print(80*"-")		
		print(Fore.GREEN+"Simplified Derivative Result Tree:"+Style.RESET_ALL)
		print_tree( simp )	
		print()
	
		print(80*"-")
		print(Fore.GREEN+"Simplified Derivative Result Expression:"+Style.RESET_ALL)
		print_normalized_expression( simp )
		print("\n")
	else:
		print("Result:")
		print_normalized_expression( simp )
		print("\n")

	return True


if __name__ == "__main__":
	main(input_expression=args.input_expression, debug=args.debug)