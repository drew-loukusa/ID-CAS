#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral(?) calculator.			   #
#																			   #
#==============================================================================#

from tree import *
from sys import stdout as std, argv

def main(args):	
	from colorama import Fore, Back, Style 	
	if len(args) < 2:
		print("No input expression")
		print(	"  Usage:\n"+
				"     python3 build_tree_messy.py [expression]" )
		return 0
	#================================== Header ===============================#
	print(Fore.BLUE+"┌"+78*"-"+"┐")	
	std.write("|"+Fore.RED+"Derivative Calculator".center(78, " ")+Fore.BLUE+"|\n")	
	print("└"+78*"-"+"┘")
	print(Style.RESET_ALL) 		
		
	#====================== Input Info + Preprocessing =======================#
		
	input_string = args[1]
	
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
	
	print(Fore.GREEN+"\nToken Stream:"+Style.RESET_ALL)
	print(token_stream)

	initilize(token_stream)
	#print("Input String Length:", len(args[1]))	
	
	# Build The Expression Tree: 
	#-------------------------------------------------------------------------#
	root = Expression(debug=False)
	#-------------------------------------------------------------------------#

	#print(Fore.GREEN+"\nNumber of nodes:"+Style.RESET_ALL, count_nodes( root ))
	reset_seen( root )
	
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

	print(80*"-")		
	print(Fore.GREEN+"Simplified Derivative Result Tree:"+Style.RESET_ALL)
	print_tree( simp )	
	print()
	
	print(80*"-")
	print(Fore.GREEN+"Simplified Derivative Result Expression:"+Style.RESET_ALL)
	print_normalized_expression( simp )
	print("\n")

if __name__ == "__main__":
	main(argv)