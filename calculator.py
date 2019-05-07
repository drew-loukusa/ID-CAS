#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral(?) calculator.			   #
#																			   #
#==============================================================================#

from tree import NodeType, Copy, Node, DumpTree, PrintTree, check_node_type
check = check_node_type

from sys import stdout as std

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
	token_stream = foo.Lex(input_string)	
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
	PrintNormalizedExpression( root ) 
	print("\n")

	print(80*"-")
	print(Fore.GREEN+"Input Expression Tree:"+Style.RESET_ALL)
	PrintTree( root )
	print()
	
	#print(80*"=")
	#print("Tree Dump:\n")
	#DumpTree(root, 0)
	#print(80*"-")
	
	#return 0
	
	#======================== Derivative Calculating =========================#
	
	from calculator import diff, simplify, simplify_mult
	
	# Differentiate the expression:
	#-------------------------------------------------------------------------#
	result = diff( root )
	#-------------------------------------------------------------------------#

	print(80*"-")
	print(Fore.GREEN+"Derivative Result Tree:"+Style.RESET_ALL)
	PrintTree( result )

	#print("\nResult Tree Dump:")
	#DumpTree(result,0)
	
	print(80*"-")	
	print(Fore.GREEN+"Derivative Result Expression:"+Style.RESET_ALL)
	PrintNormalizedExpression( result )
	print("\n")
	
	# Simplify the result expression tree:
	#-------------------------------------------------------------------------#
	simp = simplify( result )
	#-------------------------------------------------------------------------#

	# Reduce coeffecients:
	#-------------------------------------------------------------------------#
	simp = simplify_mult( simp )
	simp = simplify( simp )
	#-------------------------------------------------------------------------#

	#simp = simplify( simp 	)			
	#simp = simplify( simp 	)			
	#simp = simplify( simp, direction=None, parent=None, debug=True	)			

	print(80*"-")		
	print(Fore.GREEN+"Simplified Derivative Result Tree:"+Style.RESET_ALL)
	PrintTree( simp )	
	print()
	
	print(80*"-")
	print(Fore.GREEN+"Simplified Derivative Result Expression:"+Style.RESET_ALL)
	PrintNormalizedExpression( simp )
	print("\n")

if __name__ == "__main__":
	