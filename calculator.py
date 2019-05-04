#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral(?) calculator.			   #
#																			   #
#==============================================================================#

from build_tree_messy import NodeType, Copy, Node, DumpTree, PrintTree, check_node_type
check = check_node_type

def diff(root):	
	
	if is_leaf(root):

		if str(root._Class) == str(NodeType.Identifier): 
			return Node( NodeType.Literal, str(1), 1 , None , None )

		elif str(root._Class) == str(NodeType.Literal):					
			return Node( NodeType.Literal, str(0), 0 , None , None )

	elif root._Symbol == "^":		
		if str(root._Left._Class) == str(NodeType.Identifier) and \
		   str(root._Right._Class) == str(NodeType.Literal):			
			
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
			#DumpTree(ddxu)

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

	if root._Symbol == "ln":
		""" Case for handling natural log. """

		# Make copy of expression inside natural log:
		u = Copy(root._Right)
		v = root

		ddu = diff(u)

		# d/dx[ln(expr)] = 1/expr * d/dx[expr] 
		one = Node( NodeType.Literal, "1", 1, None, None)
		div = Node( NodeType.Operator, "/", None, one, v._Right)

		return Node( NodeType.Operator, "*", None, div, ddu)
		
		
def simplify( root,  direction=None, parent=None ): 

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
		#print(root)
		#print(root._Left)
		#print(root._Right)

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
			set_child(parent, root, direction, root._Left)
			
			
		
	# --------------------- Simplifies n * m ----------------------------------#
	elif (root and root._Symbol == "*" and 
								(is_leaf(root._Left) and is_leaf(root._Right))):
		if check(root._Left, "Literal") and check(root._Right, "Literal"):
			
			int_val = root._Left._LitVal * root._Right._LitVal
			
			int_node = Node( NodeType.Literal, str(int_val), int_val, None, None) 
			
			set_child(parent, root, direction, int_node)

			
		
	# --------------------- Simplifies n + m ----------------------------------#
	elif (root and root._Symbol == "+" and 
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
	elif root and root._Symbol == "+" and (is_leaf(root._Left) or is_leaf(root._Right)):		
		if root._Left._LitVal == 0:
			if parent:
				if direction == "left":
					parent._Left = root._Right
				else: 
					parent._Right = root._Right
			else:
				root = root._Right				

		elif root._Right._LitVal == 0:		
			if parent:	
				if direction == "left":
					parent._Left = root._Left
				else: 
					parent._Right = root._Left
			else:
				root = root._Left
				
	
	# --------------------- Simplifies 0 - x ----------------------------#
	elif (root and root._Symbol == "-" and is_leaf(root._Left) 
									   and root._Left._Symbol == "0"):
		pass

	# --------------------- Simplifies x - 0 ----------------------------#
	if (root and root._Symbol == "-" and is_leaf(root._Right) 
									 and root._Right._Symbol == "0"):
		if parent:
			if direction == "left":
				parent._Left = root._Left
			else: 
				parent._Right = root._Left
		else:			
			root = root._Left
	
	if root:
		if not is_leaf(root._Left): simplify(root._Left,  "left", root)	
		if not is_leaf(root._Right):simplify(root._Right, "right",root)

	return root
	
def set_child(parent, root, direction, new_child):
	if parent:
		if direction == "left":
			parent._Left = new_child
		else: 
			parent._Right = new_child
	else:
		root = new_child

def simplify_mult( root, coefs=[]): # direction=None, parent = None):
	""" 
		Combine coefficients in the expression tree pointed to by root
		
		Temporarily making this it's own method because this might use a 
		different algorithm than the normal simplification process. 
		
	"""
	if root._Symbol == "*": 	
		
		right = is_leaf(root._Right)
		left =  is_leaf(root._Left)
		
		if right and str(root._Right._Class) == str(NodeType.Literal):
			#print("Added a right coef")
			coefs.append(root._Right._LitVal)
		
		elif left and str(root._Left._Class) == str(NodeType.Literal):
			#print("Added a left coef")
			coefs.append(root._Left._LitVal)
		
		if not right and root._Right._Symbol == "*":
			simplify_mult( root._Right, coefs)
	
		if not left and root._Left._Symbol == "*":
			simplify_mult( root._Left, coefs)

		
	return coefs

def xor( a , b ):
	if a and not b: return True
	if b and not a: return True
	if b and a: 	return False
	if b or a: 		return False

def zeroed( root ):	
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
