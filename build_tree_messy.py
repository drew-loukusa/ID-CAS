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
	global NextToken
	global NextTokenIndex 
	global token_stream
	NextTokenIndex += 1
	print("  "*Tab+"Index", NextTokenIndex, "stream length:", len(token_stream))
	if NextTokenIndex >= len(token_stream):
		print("Returning false...")
		return False

	NextToken = token_stream[ NextTokenIndex ]	
	return True

#================================ Tree Setup =================================#

def initilize(input_stream):
	global token_stream
	global NextToken
	token_stream = input_stream
	NextToken = token_stream[0]

class NodeType(Enum):
	Literal 	= 1
	Identifier	= 2	
	Operator	= 3
	Trig 		= 4
	
class Node:
	def __init__(self, Class, Symbol, LitVal, Left, Right):
		std.write("Creating node...")
		self._Class	 = Class
		self._Symbol = Symbol
		self._LitVal = LitVal
		self._Left	 = Left
		self._Right  = Right
		self._Seen 	 = False 

def reset_seen( root ):
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
	"""Prints a parenthisized version of the input string."""
	tab = Tab
	if root is not None:
		if root._Class == NodeType.Operator or root._Class == NodeType.Trig:
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
		if root._Class == NodeType.Operator or root._Class == NodeType.Trig:
			std.write(")")

def all_nodes_seen( root ):
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
		character but this works for now."""
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
	# Puts nodes from tree into queue to be printed by level
	# Each level is a list
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
	if not root._Seen and recursion_depth > 0: 
		nlist.append( root )	
		root._Seen = True	

	recursion_depth -= 1

	if root._Left: _qnrec( root._Left, recursion_depth, nlist )
	if root._Right: _qnrec( root._Right, recursion_depth, nlist )
	return 

def DumpTree( root , indent):

	if root._Class: 	print("  "*indent + str(root._Class))
	if root._Symbol: 	print("  "*indent + str(root._Symbol))	
	if root._Left: 		DumpTree(root._Left, indent + 1)
	if root._Right: 	DumpTree(root._Right, indent + 1)

#================================ Tree Building ===============================#

def Expression():
	global Tab
	global NextToken
	std.write("  "*Tab+"EX:->\n")
	Tab += 1
	Op = None

	Left = Term()
	while NextToken[0] == 'PLUS_OP':
		print("  "*Tab+NextToken[1])
		Op = NextToken[1]
		GetNextToken()
		Left = Node( NodeType.Operator, Op, 0, Left, Term() )

	Tab -= 1
	std.write("\n"+"  "*Tab+"<-:EX- ")
	return Left 

def Term():
	global Tab
	global NextToken
	std.write("  "*Tab+"TM:->\n")
	Tab += 1
	Op = None

	Left = Factor()
	while NextToken[0] == 'MULT_OP':
		print(NextToken)
		Op = NextToken[1]
		GetNextToken()
		Left = Node( NodeType.Operator, Op, 0, Left, Factor() )

	Tab -= 1
	std.write("\n"+"  "*Tab+"<-:TM- ")
	return Left

def Factor():
	global Tab
	global NextToken
	std.write("  "*Tab+"FR:->\n")
	Tab += 1

	Left = Primary()
	while NextToken[0] == 'EXP_OP':
		print("  "*Tab+NextToken[1])
		GetNextToken()
		Left = Node( NodeType.Operator, '^', 0, Left, Primary() )

	Tab -= 1
	std.write("\n"+"  "*Tab+"<-:FR- ")
	return Left

def Primary():
	global NextToken
	global Tab
	std.write("  "*Tab+"PR:->\n")
	Tab += 1
	print("  "*Tab+NextToken[1])
	Symbol = NextToken
	Temp = None
	if not GetNextToken():
		print("REACHED END OF Expression")
		std.write("\n"+"  "*Tab+"<-:PR- ")
		Tab -= 1
		return Node( NodeType.Operator, '$', 0, None, None )

	if Symbol[0] == "NUM":		
		std.write("  "*Tab+"IsNum")		
		Tab -= 1
		std.write("\n"+"  "*Tab+"<-:PR- ")
		Symbol = Symbol[1]
		return Node( NodeType.Literal, Symbol, int(Symbol), None, None)

	elif Symbol[0] == "IDENT":
		print("  "*Tab+"IsIdent")
		Tab -= 1
		std.write("\n"+"  "*Tab+"<-:PR- ")
		Symbol = Symbol[1]
		return Node( NodeType.Identifier, Symbol.lower(), 0, None, None)

	elif Symbol[0] == "TRIG":
		print("  "*Tab+"IsTrig")
		GetNextToken()
		Temp = Expression()
		Tab -= 1		
		#Must_Be( ')' )
		std.write("\n"+"  "*Tab+"<-:PR- ")
		Symbol = Symbol[1]
		return Node( NodeType.Trig, Symbol.lower(), 0, None, Temp)

	elif Symbol[1] == '(':
		#print("  "*Tab+"(")
		print("  "*Tab+NextToken[1])		
		Temp = Expression()
		Tab -= 1
		Must_Be( ')' )
		std.write("\n"+"  "*Tab+"<-:PR")
		return Temp

	elif Symbol[0] == 'EOS':
		print("Found &")
		Tab -= 1
		std.write("\n"+"  "*Tab+"<-:PR- ")
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
	global Tab
	global NextToken
	global NextTokenIndex
	global MatchParenIndex
	global token_stream

	index = NextTokenIndex
	if MatchParenIndex > NextTokenIndex: 
		index = MatchParenIndex

	for i in range(index, len(token_stream)):
		if token_stream[i] == c: 
			MatchParenIndex = i
			std.write("Found closing paren")
			return True 

	raise Exception("Missing closing ')'")

def main(args):

	from lexer import Lexer 
	foo = Lexer()

	#token_stream = foo.Lex(args[1])

	token_stream = foo.Lex("4x^2+45*sin(x)")	
	print(token_stream)

	initilize(token_stream)
	#print("Input String Length:", len(args[1]))	
	root = Expression()

	print()
	print("Number of nodes:", count_nodes( root ))

	reset_seen( root )
	PrintNormalizedExpression( root ) 
	
	print()

	PrintTree( root )
	# nodes = queue_nodes(root)
	# for nlist in nodes:
	# 	width = int(40/len(nlist))
	# 	for node in nlist:
	# 		std.write(node._Symbol.center(width)+" ")
	# 	print()
	DumpTree(root, 0)

if __name__ == "__main__":
	main(argv)
