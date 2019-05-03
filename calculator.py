#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral(?) calculator.			   #
#																			   #
#==============================================================================#

from build_tree_messy import NodeType, Copy, Node, DumpTree, PrintTree

def diff(root):	
	
	if is_leaf(root):

		if str(root._Class) == str(NodeType.Identifier): 
			return Node( NodeType.Operator, str(1), 1 , None , None )

		elif str(root._Class) == str(NodeType.Literal):					
			return Node( NodeType.Operator, str(0), 0 , None , None )

	elif root._Symbol == "^":		
		if str(root._Left._Class) == str(NodeType.Identifier) and \
		   str(root._Right._Class) == str(NodeType.Literal):			
			
			""" Case for handling integer exponents: ( expr ) ^ n """
			
			# Copy the left sub-tree of root:
			copy = Copy(root._Left)

			# Save the value of the exponent:
			coef = root._Right._LitVal

			# Subtract 1 from exponent: 
			root._Right._LitVal -= 1

			root._Right._Symbol = str(root._Right._LitVal)

			# Create new left child with coefficient:
			new_left = Node( NodeType.Operator, str(coef), coef , None , None )
			
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
		

	if root._Symbol == "ln":
		""" Case for handeling natural log. """

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
	# If we have a multiplcation and ONLY one of the children are leaf nodes:
	if 	root and root._Symbol == "^" and is_leaf(root._Right):
		if root._Right._LitVal == 0:
			root = Node( NodeType.Operator, "1", 1, None, None)

		if root._Right._LitVal == 1:
			if parent:	
				if direction == "left":
					parent._Left = root._Left				
				else: 
					parent._Right = root._Left
			else:
				root = root._Left
			
			
	# --------------------- Simplifies x*1 and x*0 ----------------------------#
	# If we have a multiplcation and ONLY one of the children are leaf nodes:
	if 	root and root._Symbol == "*" and \
		xor(is_leaf(root._Left), is_leaf(root._Right)):

		# print(root)
		# print(root._Left)
		# print(root._Right)

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

	# --------------------- Simplifies x + 0 	----------------------------#
	# If we have a addition of zero and ONLY one of the children are leaf nodes:
	elif root and root._Symbol == "+" and \
		 xor(is_leaf(root._Left), is_leaf(root._Right)):

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

	if root:
		if not is_leaf(root._Left): simplify(root._Left,  "left", root)	
		if not is_leaf(root._Right):simplify(root._Right, "right",root)

	return root


def xor( a , b ):
	if a and not b: return True
	if b and not a: return True
	if b and a: 	return False
	if b or a: 		return False

def zeroed( root ):
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
