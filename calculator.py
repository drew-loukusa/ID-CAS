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
	Left = is_leaf(root._Left)
	Right = is_leaf(root._Right) 

	#if not Left: diff(root._Left)
	#if not Right: diff(root._Right)

	if Left and Right: 		
		#print("a")
		if root._Symbol == "^":		
			#print("a")			
			#print( str(root._Left._Class),  str(NodeType.Identifier))
			#print( str(root._Right._Class), str(NodeType.Literal))
			if str(root._Left._Class) == str(NodeType.Identifier) and \
			   str(root._Right._Class) == str(NodeType.Literal):			
				#print("a")
				result = str(root._Right._Symbol) + \
						 	 root._Left._Symbol   + "^"	+ \
						 	 str(int(root._Right._Symbol) - 1)
				print(result)

def is_leaf(node):
	if node._Left == None and node._Right == None:
		return True
	else:
		return False


def intg(expression_tree):
	return None



if __name__ == "__main__":
	print("Main func tests:\n===========================")