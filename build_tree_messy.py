#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Code Adapted from a slide deck on a Symbolic Derivation program written in C #
#	 by PSU Instructor Herbert G. Mayer			   							   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Tree builder portion of my derivative and integral(?) calculator.		   	   #
#																			   #
#==============================================================================#





# TODO: Fix this breaking: (x) + (x)






from sys import stdout as std
from sys import argv
from enum import Enum
from math import ceil	

# Globals? 
#================================================================#
token_stream = []
NextToken = ""
NextTokenIndex = 0
MatchParenIndex = 0
Tab = 0
def GetNextToken():
	"""Advances NextToken to the next token in the token stream."""
	global NextToken
	global NextTokenIndex 
	global token_stream
	NextTokenIndex += 1
	#print("  "*Tab+"Index", NextTokenIndex, "stream length:", len(token_stream))
	if NextTokenIndex >= len(token_stream):
		#print("Returning false...")
		return False
	
	#print("CurrentToken",NextToken)
	NextToken = token_stream[ NextTokenIndex ]	
	#print("NextToken:",NextToken)
	return True

#================================ Tree Setup =================================#

def initilize(input_stream):
	""" Sets NextToken to the first token in 'input_stream' and
	 	sets token_stream = input_stream """
	global token_stream
	global NextToken
	token_stream = input_stream
	NextToken = token_stream[0]

class NodeType(Enum):
	Literal 	= 1
	Identifier	= 2	
	Operator	= 3
	Func 		= 4

def check_node_type( node, type ):
	""" Checks that 'node' is of NodeType 'type' """
		
	if type == "Literal": type = NodeType.Literal
	elif type == "Identifier": type = NodeType.Identifier
	elif type == "Operator": type = NodeType.Operator
	elif type == "Func": type = NodeType.Func
	
	if str(node._Class) == str(type): return True
	else: return False
	
class Node:
	def __init__(self, Class, Symbol, LitVal, Left, Right):
		self._Class	 = Class
		self._Symbol = Symbol
		self._LitVal = LitVal
		self._Left	 = Left
		self._Right  = Right
		self._Seen 	 = False 

	def __str__(self):
		return  ("<class 'Node' - Class: "  + str(self._Class) + 
				" Symbol: " +	str(self._Symbol) + 
				" LitVal "  + str(self._LitVal) + " >")			

def reset_seen( root ):
	""" Resets every nodes '_Seen' property. The '_Seen' property is used
		by the _ptrec() function to mark nodes that have already been printed"""
	if root: root._Seen = False
	if root._Left: reset_seen( root._Left )
	if root._Right: reset_seen( root._Right )

def count_nodes( root, count = [0]):
	if root: 
		count[0] += 1
		if root._Left: count_nodes( root._Left, count )
		if root._Left: count_nodes( root._Right, count )
	return count[0]

def Copy( root ):
	""" Returns a deep copy of the tree pointed to by 'root'. """
	if root is None: 
		return None
	else: 		
		return Node(root._Class, 
					root._Symbol, 
					root._LitVal, 
					Copy(root._Left), 
					Copy(root._Right)
					)

#================================ Tree Dumping ================================#

def PrintNormalizedExpression( root, Tab=0 ):	
	"""Prints a parenthesized expression of the tree pointed to by root"""	
	tab = Tab
	if root is not None:
		if root._Class == NodeType.Operator or root._Class == NodeType.Func:
			std.write("(")

		PrintNormalizedExpression( root._Left, tab + 1 )
		if root._Class == NodeType.Literal:
			std.write(str( root._LitVal ))
		else:
			if root._Symbol is tuple:
				std.write(str(root._Symbol[1]))
			else:
				std.write(str(root._Symbol))

		PrintNormalizedExpression( root._Right,  tab + 1  )
		if root._Class == NodeType.Operator or root._Class == NodeType.Func:
			std.write(")")
	
def all_nodes_seen( root ):
	""" Boolean function which returns true if all nodes in the tree have been
		seen. """
	if root._Seen:
		a, b = True, True
		if root._Left: a = all_nodes_seen( root._Left )
		if root._Right: b = all_nodes_seen( root._Right )
		return a and b
	else: 
		return False

def PrintTree( root ):	
	""" Prints out the expression tree as a tree. May not work properly.
		Probably need to redo this and calculate the per line index of each
		character but this works for now.

		This method works by printing out one level of the tree at a time. 
		The root is level 0, the children of the root are level 1 and the 
		children of the children are level 2, etc, etc. 

		We go down one more level each time, marking each node that we see.
		We DON'T print nodes we've already seen so this way, when we 
		recurse down the tree multiple times, we don't print out nodes multiple 
		times. 

		Location to print nodes is determined by 'width' and if we go "left" or
		"right". If we go to a left child, then our location is the 
		ceiling(width/2). 

		Since I'm using std.write(), and I have empty leaf nodes still print
		a blank space, I don't have to do any adjusting, just divide width by 2.

		
	"""

	if root is None: return	
	cur = root 
	rec_depth = 1
	width = 80
	copy_width = 40
	num_nodes = count_nodes( root )

	while not all_nodes_seen(root):		
		_ptrec( root, rec_depth, width)
		#std.write("".center(width, "-"))
		rec_depth += 1
		print()

	reset_seen( root )	

def _ptrec( root, recursion_depth, width ):
	""" Recursive function called by the setup function PrintTree().
		
		See PrintTree for a descripton of the algorithm.

	"""
	if recursion_depth <= 0:
		return 

	if root == None: 
		std.write("".center(width))	
		return 

	if not root._Seen and recursion_depth > 0: 
		text = "(" + str(root._Symbol) + ")"
		text = root._Symbol
		if text is tuple:
			text = text[1]
		std.write(text.center(width))		
		root._Seen = True	

	recursion_depth -= 1		

	_ptrec( root._Left, recursion_depth, ceil(width/2) )
	_ptrec( root._Right, recursion_depth, ceil(width/2) )

def queue_nodes( root ):
	"""	Puts nodes from tree into queue to be printed by level
	   	Each level is a list. 

	   	Currently Not in use.
	"""
	queue = []
	if root is None: return
	np = [0]
	cur = root 
	rec_depth = 1
	num_nodes = count_nodes( root )

	while not all_nodes_seen(root):	
		nlist = []
		_qnrec( root, rec_depth, nlist )
		queue.append( nlist )
		rec_depth += 1
		print()

	reset_seen( root )
	return queue

def _qnrec( root, recursion_depth, nlist ):
	""" Not is use currently """
	if not root._Seen and recursion_depth > 0: 
		nlist.append( root )	
		root._Seen = True	

	recursion_depth -= 1

	if root._Left: _qnrec( root._Left, recursion_depth, nlist )
	if root._Right: _qnrec( root._Right, recursion_depth, nlist )
	return 

def DumpTree( root , indent=0):
	""" Line by line dump of tree pointed to by root using indentation """
	
	#if root._Class: 	print("  "*indent + str(root._Class))
	if root._Symbol: 	print("--"*indent + str(root._Symbol))	
	if root._Left: 		DumpTree(root._Left, indent + 1)
	if root._Right: 	DumpTree(root._Right, indent + 1)

#================================ Tree Building ===============================#

def Expression(debug=False):
	""" """
	global Tab
	global NextToken
	
	if debug: std.write("  "*Tab+"EX:->\n")
	Tab += 1
	Op = None
	Left = Term(debug)

	if NextToken[1] == ')': 
		GetNextToken()

		if debug: std.write("\n"+str(NextToken))

		# if NextToken[0] != 'PLUS_OP':
		if debug: std.write("\n"+"  "*Tab+"<-:EX- ")
		return Left

	#print("\nAfter Left:",NextToken)

	while NextToken[0] == 'PLUS_OP':
		if debug: print("  "*Tab+NextToken[1])
		Op = NextToken[1]
		GetNextToken()
		Left = Node( NodeType.Operator, Op, None, Left, Term(debug) )

	Tab -= 1
	if debug: std.write("\n"+"  "*Tab+"<-:EX- ")
	return Left 

def Term(debug=False):
	global Tab
	global NextToken
	if debug: std.write("  "*Tab+"TM:->\n")
	Tab += 1
	Op = None

	Left = Factor(debug)
	while NextToken[0] == 'MULT_OP':
		if debug: print(NextToken)
		Op = NextToken[1]
		GetNextToken()
		Left = Node( NodeType.Operator, Op, None, Left, Factor(debug) )

	Tab -= 1
	if debug: std.write("\n"+"  "*Tab+"<-:TM- ")
	return Left

def Factor(debug=False):
	global Tab
	global NextToken
	if debug: std.write("  "*Tab+"FR:->\n")
	Tab += 1

	Left = Primary(debug)	
	while NextToken[0] == 'EXP_OP':
		if debug: print("  "*Tab+NextToken[1])
		GetNextToken()
		Left = Node( NodeType.Operator, '^', None, Left, Primary(debug) )

	Tab -= 1
	if debug: std.write("\n"+"  "*Tab+"<-:FR- ")
	return Left

def Primary(debug=False):
	global NextToken
	global Tab
	if debug: std.write("  "*Tab+"PR:->\n")
	Tab += 1
	if debug: print("  "*Tab+NextToken[1])
	Symbol = NextToken
	Temp = None
	
	if not GetNextToken():
		if debug: print("REACHED END OF Expression")
		if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
		Tab -= 1
		return Node( NodeType.Operator, '$', 0, None, None )
	
	if Symbol[0] == "NUM":		
		if debug: std.write("  "*Tab+"IsNum")		
		Tab -= 1
		if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
		Symbol = Symbol[1]
		return Node( NodeType.Literal, Symbol, int(Symbol), None, None)

	elif Symbol[0] == "IDENT":
		if debug: print("  "*Tab+"IsIdent")
		Tab -= 1
		if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
		Symbol = Symbol[1]
		return Node( NodeType.Identifier, Symbol.lower(), None, None, None)

	elif Symbol[0] == "TRIG":
		if debug: print("  "*Tab+"IsTrig")
		GetNextToken()
		Temp = Expression(debug)
		Tab -= 1		
		#Must_Be( ')' )
		if debug: std.write("\n"+"  "*Tab+"<-:PR- ")

		Symbol = Symbol[1]
		return Node( NodeType.Func, Symbol.lower(), None, None, Temp)
	
	elif Symbol[0] == "LN":
		if debug: print("  "*Tab+"IsLN")
		GetNextToken()
		Temp = Expression(debug)
		Tab -= 1		
		#Must_Be( ')' )
		if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
		Symbol = Symbol[1]
		return Node( NodeType.Func, Symbol.lower(), None, None, Temp)


	elif Symbol[1] == '(':
		#print("  "*Tab+"(")
		if debug: print("  "*Tab+NextToken[1])		

		#print("NTI",NextTokenIndex)
		Temp = Expression(debug)
		#print("NTI",NextTokenIndex)

		Tab -= 1
		#Must_Be( ')' )
		if debug: std.write("\n"+"  "*Tab+"<-:PR")
		return Temp
		
	# elif Symbol[1] == ')':				
	# 	Tab -= 1				
	# 	if debug: print("  "*Tab+NextToken[1])		
	# 	GetNextToken()
	# 	return Temp

	elif Symbol[0] == 'EOS':
		if debug: print("Found &")
		Tab -= 1
		if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
		return Node( NodeType.Operator, '&', 0, None, Primary() )

	else:
		print( "Illegal Character:", Symbol )

#================================ Misc and Main ===============================#

def IsDigit(c): 
	if c[0] == "NUM":
		return True
	else:
		return False

def IsLetter(c): 
	if c[1] in "abcdefghijklmnopqrstuvwxyz":
		return True
	else:
		return False

def Must_Be(c): 
	""" Mostly used to ensure if there is an opening brace, then there is 
		a matching closing brace somewhere in the expression. 

		This function also saves the location of the last found closing brace
		into MatchParenIndex. If we start looking for another closing brace, 
		then we start looking from MatchParenIndex.
	"""
	global Tab
	global NextToken
	global NextTokenIndex
	global MatchParenIndex
	global token_stream
	
	#print("MatchParenIndex",MatchParenIndex)

	index = NextTokenIndex
	if MatchParenIndex > NextTokenIndex: 
		index = MatchParenIndex

	#print("* NextToken",NextToken)
	#print("* NextTokenIndex", NextTokenIndex)
	#print("* Index", index)

	for i in range(index, len(token_stream)):
		if token_stream[i][1] == c: 
			MatchParenIndex = i
			#GetNextToken()
			#std.write("Found closing paren")
			#print("* NextToken",NextToken)
			#print("* NextTokenIndex", NextTokenIndex)
			#print("* Index", index)

			return True 


	raise Exception("Missing closing '{}'".format(c))

def main(args):	
	from colorama import Fore, Back, Style 
	# print(Fore.RED + 'some red text') 
	# print(Back.GREEN + 'and with a green background') 
	# print(Style.DIM + 'and in dim text') 
	# print(Style.RESET_ALL) 
	# print('back to normal now') 
	
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
	main(argv)