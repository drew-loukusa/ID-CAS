from build_tree_messy import NodeType, Copy, Node

#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral(?) calculator.				   #
#																			   #
#==============================================================================#

def diff(root):	
	
	if is_leaf(root):
		#print("Found a leaf node!")
		if str(root._Class) == str(NodeType.Identifier): 
			#print("Returning 1")
			return Node( NodeType.Operator, str(1), 1 , None , None )
		elif str(root._Class) == str(NodeType.Literal):
			#print("Returning 0")			
			return Node( NodeType.Operator, str(0), 0 , None , None )

	if root._Symbol == "^":		
		if str(root._Left._Class) == str(NodeType.Identifier) and \
		   str(root._Right._Class) == str(NodeType.Literal):			
			
			"""Case for handling integer exponents: ( expr ) ^ n """
			
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
			new_root = Node( NodeType.Operator, "*", 0, new_left , root)

			# Create another new NEW root node for applying the chain rule:
			new_NEW_root = Node( NodeType.Operator, "*", 0, new_root , None)

			# Evaluate the derivative of the copied tree: 
			ddxu = diff( copy )

			# Set the right child to the evaluated tree.
			new_NEW_root._Right = ddxu
				
			return new_NEW_root
			
	if root._Symbol == "*":
		if not is_leaf(root._Left) and not is_leaf(root._Right):
		"""Case for applying the product rule."""
			
		u = Copy(root._Left)
		v = Copy(root._Right)
		
		ddu = diff(root._Left)
		ddv = diff(root._Right)
		
		left_mult = Node( NodeType.Operator, "*", 0, ddu, v)
		right_mult = Node( NodeType.Operator, "*", 0, ddv, u)
		
		new_root = Node( NodeType.Operator, "*", 0, left_mult, right_mult)
	
	if root._Symbol == "ln":
		
		# Make copy of expression inside natural log:
		u = Copy(root._Right)
		v = root
		
		
		
		

def is_leaf(node):
	if node._Left == None and node._Right == None:
		return True
	else:
		return False


def intg(expression_tree):
	return None



if __name__ == "__main__":
	print("Main func tests:\n===========================")