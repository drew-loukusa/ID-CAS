from build_tree_messy import NodeType

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
			
			# Apply Exponet Rule for differentiating:
			if is_leaf(root._Right): 
				pass



			result = str(root._Right._LitVal) + \
					 	 root._Left._Symbol   + "^"	+ \
					 	 str(root._Right._LitVal - 1)


def is_leaf(node):
	if node._Left == None and node._Right == None:
		return True
	else:
		return False


def intg(expression_tree):
	return None



if __name__ == "__main__":
	print("Main func tests:\n===========================")