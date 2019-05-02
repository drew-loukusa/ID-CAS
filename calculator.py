from build_tree_messy import NodeType, Copy, Node

#==============================================================================#
#																			   #
# Author: Drew Loukusa														   #
# Email: dlwerd@gmail.com													   #
# Date: 4/30/19																   #
#																			   #
# Calculator portion of my derivative and integral calculator.				   #
#																			   #
#==============================================================================#

def diff(root):	
		
	if root._Symbol == "^":			
		if str(root._Left._Class) == str(NodeType.Identifier) and \
		   str(root._Right._Class) == str(NodeType.Literal):			
			
			
			# Copy the left sub-tree of root:
			copy = Copy(root._Left)

			# Save the value of the exponet:
			coef = root._Right._LitVal

			# Subtract 1 from exponet: 
			root._Right._LitVal -= 1
			root._Right._Symbol = str(root._Right._LitVal)

			# Create new left child with coefficiant:
			new_left = Node( NodeType.Operator, str(coef), coef , None , None )
			
			# Create new root node for applying exponet rule			
			new_root = Node( NodeType.Operator, "*", 0, new_left , root)

			# Create another new root node:

				# Left child is the above expression tree
				# Right child is the expression tree INSIDE this expression
				# 	if any exists. Think chain rule:
				#		
				#	d/dx[(x)^2] -> 2*(x)^1 * d/dx[x] -> 2*(x)^1*1
				#	
			return new_root
			


def is_leaf(node):
	if node._Left == None and node._Right == None:
		return True
	else:
		return False


def intg(expression_tree):
	return None



if __name__ == "__main__":
	print("Main func tests:\n===========================")