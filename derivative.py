#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Derivative portion of my derivative and integral(?) calculator.			   #
#																			   #
#==============================================================================#



# TODO: Implement trig derivatives



from tree import NodeType, Copy, Node, dump_tree, print_tree, check_node_type
check = check_node_type

from sys import stdout as std

def diff(root):	
	
	if is_leaf(root):

		if str(root._Class) == str(NodeType.Identifier): 
			return Node( NodeType.Literal, str(1), 1 , None , None )

		elif str(root._Class) == str(NodeType.Literal):					
			return Node( NodeType.Literal, str(0), 0 , None , None )

	elif root._Symbol == "^":		
		if str(root._Right._Class) == str(NodeType.Literal):			
			
			""" Case for handling integer exponents: ( expr ) ^ n """
			
			#print("Dived an exponent")
			#print(root)
			#print(root._Right)
			#print(root._Left)
			
			# Copy the left sub-tree of root:
			copy = Copy(root._Left)		
			# Save the value of the exponent:
			coef = root._Right._LitVal

			# Subtract 1 from exponent: 
			root._Right._LitVal -= 1
			root._Right._Symbol = str(root._Right._LitVal)

			# Create new left child with coefficient:
			new_left = Node( NodeType.Literal, str(coef), coef , None , None )

			# Create new root node for applying exponent rule			
			new_root = Node( NodeType.Operator, "*", None, new_left , root)

			# Create another new NEW root node for applying the chain rule:
			new_NEW_root = Node( NodeType.Operator, "*", None, new_root , None)

			# Evaluate the derivative of the copied tree: 
			ddxu = diff( copy )
			#print("ddxu tree")
			#dump_tree(ddxu)

			# Set the right child to the evaluated tree.
			new_NEW_root._Right = ddxu

			return new_NEW_root
		else:
			raise Exception("Non-Supported Expression")

	elif root._Symbol == "*":		
		""" Case for applying the product rule. """

		u = Copy(root._Left)
		v = Copy(root._Right)

		ddu = diff(root._Left)
		ddv = diff(root._Right)

		left_mult = Node( NodeType.Operator, "*", None, ddu, v)
		right_mult = Node( NodeType.Operator, "*", None, ddv, u)

		return Node( NodeType.Operator, "+", None, left_mult, right_mult)

	if root._Symbol == "/":
		""" Case for handling the quotient rule. """

		# d/dx[u/v] = (v*du - u*dv)/(v^2)

		u = Copy(root._Left)
		v = Copy(root._Right)

		ddu = diff( root._Left )
		ddv = diff( root._Right )

		left_mult 	= 	Node( NodeType.Operator, "*", None, ddu, v)
		right_mult 	= 	Node( NodeType.Operator, "*", None, ddv, u)
		minus		=	Node( NodeType.Operator, "-", None, left_mult, right_mult)

		denom_v 	= 	Copy( v )
		denom_exp 	=	Node( NodeType.Literal, "2", 2, None, None)
		denom_pow 	= 	Node( NodeType.Operator, "^", None, denom_v, denom_exp)

		root._Right = 	denom_pow
		root._Left 	= 	minus

		return root

	if root._Symbol in "-+":
		""" Case for handling addition and subtraction. """		
		u = diff(root._Left)
		v = diff(root._Right)
		return Node( NodeType.Operator, root._Symbol, None, u, v )

	if root._Symbol == "sin":
		""" Case for the sin function. """

		# Make copy of expression inside sin function:
		u = Copy(root._Right)
		ddu = diff(u)

		# Change sin to cos:
		root._Symbol = "cos"

		# d/dx[sin(expr)] = cos(expr)* d/dx[expr] 

		return Node( NodeType.Operator, "*", None, root, ddu)

	if root._Symbol == "ln":
		""" Case for handling natural log. """

		# Make copy of expression inside natural log:
		u = Copy(root._Right)
		v = root

		ddu = diff(u)

		# d/dx[ln(expr)] = 1/expr * d/dx[expr] = d/dx[expr] / expr		
		div = Node( NodeType.Operator, "/", None, ddu, v._Right)

		return div

def simplify( root,  direction=None, parent=None, debug=False): 

	if root:
		#if tree_modified: simplify(root._Left, direction, root, debug)
		if not is_leaf(root._Left): simplify(root._Left,  "left", root, debug)	
		if not is_leaf(root._Right):simplify(root._Right, "right",root, debug)

	tree_modified = False

	# Debug prints:	
	if debug and root and root._Symbol == "*":
		print(root)
		print("\t"+str(root._Left))
		print("\t"+str(root._Right))

	#--------------------------- Simplifies x^1 -------------------------------#
	# If we have a multiplication and ONLY one of the children are leaf nodes:
	if 	root and root._Symbol == "^" and is_leaf(root._Right):
		if root._Right._LitVal == 0:
			int_node = Node( NodeType.Literal, "1", 1, None, None)
			set_child(parent, root, direction, int_node)
			

		if root._Right._LitVal == 1:
			set_child(parent, root, direction, root._Left)
			
		

	# --------------------- Simplifies x*1 and x*0 ----------------------------#
	# If we have a multiplication and ONLY one of the children are leaf nodes:
	if 	root and root._Symbol == "*" and (is_leaf(root._Left) or is_leaf(root._Right)):		
		if debug:
			print("Case: x*1 and x*0 ")
			print(root)
			print("\t"+str(root._Left))
			print("\t"+str(root._Right))

		if root._Left._LitVal == 0 or root._Right._LitVal == 0:			
			zeroed( root )	
				

		elif root._Left._LitVal == 1:
			if parent:
				if direction == "left":
					parent._Left = root._Right
				else: 
					parent._Right = root._Right
			else:
				root = root._Right
			

		elif root._Right._LitVal == 1:	
			if parent:
				if direction == "left":
					parent._Left = root._Left
				else: 
					parent._Right = root._Left
			else:
				root = root._Left
			

			#set_child(parent, root, direction, root._Left)
		

	# --------------------- Simplifies n * m ----------------------------------#
	if (root and root._Symbol == "*" and 
								(is_leaf(root._Left) and is_leaf(root._Right))):
		#print(root)
		#print(root._Left)
		#print(root._Right)
		if check(root._Left, "Literal") and check(root._Right, "Literal"):
			
			int_val = root._Left._LitVal * root._Right._LitVal
			
			int_node = Node( NodeType.Literal, str(int_val), int_val, None, None) 
			
			set_child(parent, root, direction, int_node)
		

	# --------------------- Simplifies n + m ----------------------------------#
	if (root and root._Symbol == "+" and 
								(is_leaf(root._Left) and is_leaf(root._Right))):
		
		if check(root._Left, "Literal") and check(root._Right, "Literal"):			
			int_val = root._Left._LitVal + root._Right._LitVal
			int_node = Node( NodeType.Literal, str(int_val), int_val, None, None) 
			set_child(parent, root, direction, int_node)
			
			if root._Symbol == "+": 
				root._Class = NodeType.Literal
				root._Symbol = str(int_val)
				root._LitVal = int_val
				root._Left = None
				root._Right = None
			

	# --------------------- Simplifies x + 0 	----------------------------#
	# If we have a addition of zero and ONLY one of the children are leaf nodes:
	if root and root._Symbol == "+" and (is_leaf(root._Left) or is_leaf(root._Right)):		
		if root._Left._LitVal == 0:
			root = set_child(parent, root, direction, root._Right)
			# if parent:
			# 	if direction == "left":
			# 		parent._Left = root._Right
			# 	else: 
			# 		parent._Right = root._Right
			# else:
			# 	root = root._Right		
					

		elif root._Right._LitVal == 0:				
			root = set_child(parent, root, direction, root._Left)			
			# if parent:	
			# 	if direction == "left":
			# 		parent._Left = root._Left
			# 	else: 
			# 		parent._Right = root._Left
			# else:
			# 	root = root._Left
		

	# --------------------- Simplifies 0 - x ----------------------------#
	if (root and root._Symbol == "-" and is_leaf(root._Left) 
									   and root._Left._Symbol == "0"):
		pass


	# --------------------- Simplifies x - 0 ----------------------------#
	if (root and root._Symbol == "-" and is_leaf(root._Right) 
									 and root._Right._Symbol == "0"):
		if debug:
			print("Case: x-0 ")
			print("parent", parent)
			print("root", root)
			print("\t"+str(root._Left))
			print("\t"+str(root._Right))

		root = set_child(parent, root, direction, root._Left)	

	return root
	
def set_child(parent, root, direction, new_child):
	if parent:
		if direction == "left":
			parent._Left = new_child
		else: 
			parent._Right = new_child
		return root 
	else:
		return new_child		

def simplify_mult( root ):
	""" 
		Combine coefficients in the expression tree pointed to by root	
		This is a recursive method which looks through the tree for linked
		multiplication nodes.

		If it finds linked multiplication nodes, it will call reduce_coefficents()
	"""

	if root and root._Symbol == "*" and (root._Left._Symbol == "*" or root._Right._Symbol == "*"):
		root = reduce_coefficents( root )

	else:
		if root and root._Left: simplify_mult(root._Left)
		if root and root._Right: simplify_mult(root._Right)

	return root

def reduce_coefficents( root ):	
	""" 
		Finds all coefficients in a given set of linked multiplication nodes
		and combines them into a single integer.
	"""
	nodes = []
	vals = []
	gather_coefficients( root, nodes )
	
	# Change every coefficient to '1':
	for node in nodes: 
		vals.append(node._LitVal)
		node._LitVal = 1
		node._Symbol ="1"
	
	coef = 1

	# Compute the new, singular coefficient:
	for val in vals: coef *= val

	# Apply that coefficient to to the leftmost node in our tree:	
	nodes[-1]._Symbol = str(coef)
	nodes[-1]._LitVal = coef

	# Because we changed every coefficient to '1', we call simplify again
	# to delete those nodes. 
	return simplify( root,  direction=None, parent=None, debug=False)

def gather_coefficients( root, coefs ):
	"""
		Grabs all coefficients in a set of linked multiplication nodes.
		The leftmost node will be in the LAST index of the list.
	"""
	if root._Symbol == "*": 			
		left =  is_leaf(root._Left)
		right = is_leaf(root._Right)
		
		if left and str(root._Left._Class) == str(NodeType.Literal):
			#print("Added a left coef")
			coefs.append(root._Left)

		elif right and str(root._Right._Class) == str(NodeType.Literal):
			#print("Added a right coef")
			coefs.append(root._Right)
	
		if not left and root._Left._Symbol == "*":
			gather_coefficients( root._Left, coefs)		
		
		if not right and root._Right._Symbol == "*":
			gather_coefficients( root._Right, coefs)
	
	return coefs

def xor( a , b ):
	if a and not b: return True
	if b and not a: return True
	if b and a: 	return False
	if b or a: 		return False

def zeroed( root ):	
	""" Zeroes out a node, and set's it's children to None."""
	root._Class = NodeType.Literal
	root._Symbol = "0"
	root._LitVal =  0	
	root._Left = None
	root._Right = None		

def is_leaf(node):
	if node and node._Left == None and node._Right == None:
		return True
	else:
		return False


def intg(expression_tree):
	return None



if __name__ == "__main__":
	print("Main func tests:\n===========================")
