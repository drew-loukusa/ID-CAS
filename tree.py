#==============================================================================#
#                                                                              #
# Author: Drew Loukusa                                                         #
# Tree building algorithm based a slide deck on a Symbolic Derivation program  #
# written in C by PSU Instructor Herbert G. Mayer                              #
#                                                                              #
# Email: dlwerd@gmail.com                                                      #
# Date: 4/30/19                                                                #
#                                                                              #
# Tree builder portion of my derivative calculator.                            #
#                                                                              #
#==============================================================================#

from sys import stdout as std
from sys import argv
from enum import Enum
from math import ceil   


#================================================================#

class NodeType(Enum):
    Literal     = 1
    Identifier  = 2 
    Operator    = 3
    Function    = 4
    
class Node:
    def __init__(_, NType, Symbol, LitVal, Left, Right):
        _._NType    = NType
        _._Symbol   = Symbol 
        _._LitVal   = LitVal # If leaf node, usually an integer, can be float or double?
        _._Left     = Left
        _._Right    = Right
        _._Seen     = False 

    def __str__(_):
        return  ("<class 'Node' - NType: "  + str(_._NType) + 
                " Symbol: " +   str(_._Symbol) + 
                " LitVal "  + str(_._LitVal) + " >")            

class Tree: 
    def __init__(_, input_stream):
        _.token_stream = input_stream
        _.NextToken = _.token_stream[0]
        _.NextTokenIndex = 0
        _.MatchParenIndex = 0
        _.Tab = 0

    def build_tree(_, debug=False):
        return _.expression(debug=debug)

    def get_next_token(_):
        """Advances NextToken to the next token in the token stream."""
        
        _.NextTokenIndex += 1
        #print("  "*Tab+"Index", NextTokenIndex, "stream length:", len(token_stream))
        if _.NextTokenIndex >= len(_.token_stream):
            #print("Returning false...")
            return False
        
        #print("CurrentToken",NextToken)
        _.NextToken = _.token_stream[ _.NextTokenIndex ]    
        #print("NextToken:",NextToken)
        return True

    #================================ Tree Building ===============================#

    def expression(_, debug=False):
        """ Handles addition operators: '-' and '+' """
        Tab = _.Tab 
        
        if debug: std.write("  "*Tab+"EX:->\n")

        Tab += 1
        Op = None

        # If the current token is of lower precedence, parse it as well as 
        # handling any subsequent lower precedence terms:
        Left = _.term(debug)

        """ 
        The above call to term parsed items, if it ended because we 
        encountered a closing paren then we need to return the current 
        expression back up a layer of recursion: 
        """
        if _.NextToken[1] == ')': 
            # Since the current token is a closing paren, advance it:
            _.get_next_token()

            if debug: 
                std.write("\n"+str(_.NextToken))            
                std.write("\n"+"  "*Tab+"<-:EX- ")

            return Left     

        # If after parsing lower precedence tokens there are more 
        # plus operators to parse, parse them now:
        while _.NextToken[0] == 'PLUS_OP':
            if debug: print("  "*Tab+_.NextToken[1])

            Op = _.NextToken[1]
            _.get_next_token()

            # Immediately after parsing a plus op, there should be another, 
            # lower any precedence item. So call term again inside this new node:
            Left = Node( 
                            NType   = NodeType.Operator, 
                            Symbol  = Op, 
                            LitVal  = None, 
                            Left    = Left,
                            Right   = _.term(debug) 
                        )

        Tab -= 1
        if debug: std.write("\n"+"  "*Tab+"<-:EX- ")
        return Left 

    def term(_, debug=False):
        """ Handles multiplication operators: '*' and '/' """
        Tab = _.Tab     
        if debug: std.write("  "*Tab+"TM:->\n")
        Tab += 1
        Op = None

        # If the current token is of lower precedence, parse it as well as 
        # handling any subsequent lower precedence tokens:
        Left = _.factor(debug)

        # If after parsing lower precedence tokens there are more 
        # multiplication operators to parse, parse them now:
        while _.NextToken[0] == 'MULT_OP':
            if debug: print(_.NextToken)
            
            Op = _.NextToken[1]
            _.get_next_token()

            # Immediately after parsing a mult op, there should be another, 
            # lower precedence item. So call Factor again inside this new node:
            Left = Node( 
                            NType   = NodeType.Operator,
                            Symbol  = Op, 
                            LitVal  = None, 
                            Left    = Left, 
                            Right   = _.factor(debug) 
                        )

        Tab -= 1
        if debug: std.write("\n"+"  "*Tab+"<-:TM- ")
        return Left

    def factor(_, debug=False):
        """ Handles exponent operator: '^' """
        Tab = _.Tab     
        if debug: std.write("  "*Tab+"FR:->\n")
        Tab += 1

        # If the current token is of lower precedence, parse it as well as 
        # handling any subsequent lower precedence tokens:      
        Left = _.primary(debug) 

        # If after parsing lower precedence tokens there are more 
        # exponent operators to parse, parse them now:
        while _.NextToken[0] == 'EXP_OP':
            if debug: print("  "*Tab+_.NextToken[1])

            _.get_next_token()
            # Immediately after parsing a exponet op, there must be a
            # lower precedence item. So call primary inside this new node:
            Left = Node( 
                            NType   = NodeType.Operator, 
                            Symbol  = '^',
                            LitVal  = None, 
                            Left    = Left, 
                            Right   = _.primary(debug) 
                        )

        Tab -= 1
        if debug: std.write("\n"+"  "*Tab+"<-:FR- ")
        return Left

    def primary(_, debug=False):
        """ Handles all of the lowest level 'items' in the grammar: """
        Tab = _.Tab
        if debug: 
            std.write("  "*Tab+"PR:->\n")
            print("  "*Tab+_.NextToken[1])
        
        Tab += 1
        Symbol = _.NextToken
        Temp = None
        
        # If GetNextToken() returns the end of the 
        # string, then we're done parsing the tree:
        if not _.get_next_token():
            if debug: 
                print("REACHED END OF Expression")
                std.write("\n"+"  "*Tab+"<-:PR- ")
            Tab -= 1
            return Node( 
                            NType   = NodeType.Operator, 
                            Symbol  = '$', 
                            LitVal  = 0, 
                            Left    = None, 
                            Right   = None 
                        )
        
        if Symbol[0] == "NUM":      
            if debug:
                std.write("  "*Tab+"IsNum")     
                std.write("\n"+"  "*Tab+"<-:PR- ")
            Tab -= 1
            Symbol = Symbol[1]
            return Node( 
                            NType   = NodeType.Literal, 
                            Symbol  = Symbol, 
                            LitVal  = int(Symbol), 
                            Left    = None, 
                            Right   = None
                        )

        elif Symbol[0] == "IDENT":
            if debug: print("  "*Tab+"IsIdent")
            Tab -= 1
            if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
            Symbol = Symbol[1]
            return Node( 
                            NType   = NodeType.Identifier, 
                            Symbol  = Symbol.lower(), 
                            LitVal  = None, 
                            Left    = None, 
                            Right   = None
                        )

        elif Symbol[0] in ["TRIG", "EULER", "LN"]:
            if debug: print("  "*Tab+"Is"+Symbol[0])
            _.get_next_token()
            Temp = _.expression(debug)
            Tab -= 1        
            #Must_Be( ')' )
            if debug: std.write("\n"+"  "*Tab+"<-:PR- ")

            Symbol = Symbol[1]
            return Node( 
                            NType   = NodeType.Function, 
                            Symbol  = Symbol.lower(), 
                            LitVal  = None, 
                            Left    = None, 
                            Right   = Temp
                        )       

        elif Symbol[1] == '(':

            if debug: print("  "*Tab+_.NextToken[1])        

        
            # If an opening paren is found, then we have 
            # reached the start of a new expression to parse:
                        
            Temp = _.expression(debug)

            Tab -= 1
            
            if debug: std.write("\n"+"  "*Tab+"<-:PR")
            return Temp

        elif Symbol[0] == 'EOS':
            if debug: print("Found &")
            Tab -= 1
            if debug: std.write("\n"+"  "*Tab+"<-:PR- ")
            return Node( 
                            NType   = NodeType.Operator, 
                            Symbol  = '&',
                            LitVal  = 0, 
                            Left    = None, 
                            Right   = _.primary()
                        )

        else:
            print( "Illegal Character:", Symbol )

    def must_be(_, c): 
        """ 
            NOT IN USE ANYMORE: I changed how my parsing works to not use this.

            I should probably have some sort of check, but I'll worry about that
            later. It works for now.

            Mostly used to ensure if there is an opening brace, then there is 
            a matching closing brace somewhere in the expression. 

            This function also saves the location of the last found closing brace
            into MatchParenIndex. If we start looking for another closing brace, 
            then we start looking from MatchParenIndex.
        """     
        #print("MatchParenIndex",MatchParenIndex)

        index = _.NextTokenIndex
        if _.MatchParenIndex > _.NextTokenIndex: 
            index = _.MatchParenIndex

        #print("* _.NextToken",_.NextToken)
        #print("* NextTokenIndex", NextTokenIndex)
        #print("* Index", index)

        for i in range(index, len(_.token_stream)):
            if _.token_stream[i][1] == c: 
                _.MatchParenIndex = i
                #GetNextToken()
                #std.write("Found closing paren")
                #print("* _.NextToken",_.NextToken)
                #print("* NextTokenIndex", NextTokenIndex)
                #print("* Index", index)

                return True 


        raise Exception("Missing closing '{}'".format(c))

#================================ Tree Setup =================================#

def check_node_type( node, type ):
    """ Checks that 'node' is of NodeType 'type' """
        
    if type == "Literal": type = NodeType.Literal
    elif type == "Identifier": type = NodeType.Identifier
    elif type == "Operator": type = NodeType.Operator
    elif type == "Function": type = NodeType.Function
    
    if str(node._NType) == str(type): return True
    else: return False
    

def reset_seen( root ):
    """ Resets every nodes '_Seen' property. The '_Seen' property is used
        by the _ptrec() function to mark nodes that have already been printed"""
    if root: 
        root._Seen = False
        if root._Left: reset_seen( root._Left )
        if root._Right: reset_seen( root._Right )

def count_nodes( root, count = [0]):
    if root: 
        count[0] += 1
        if root._Left: count_nodes( root._Left, count )
        if root._Left: count_nodes( root._Right, count )
    return count[0]

def copy_tree( root ):
    """ Returns a deep copy of the tree pointed to by 'root'. """
    if root is None: 
        return None
    else:       
        return Node(
                        NType   = root._NType, 
                        Symbol  = root._Symbol, 
                        LitVal  = root._LitVal, 
                        Left    = copy_tree(root._Left), 
                        Right   = copy_tree(root._Right)
                    )


#================================ Tree Dumping ================================#

def print_expr( root, parent=None, Tab=0 ): 
    """Prints a parenthesized expression of the tree pointed to by root"""  
    tab = Tab
    if root is not None:

        print_expr( root._Left, root , tab + 1 )
        if root._NType == NodeType.Literal:
            std.write(str( root._LitVal ))
        else:
            if root._Symbol is tuple:
                std.write(str(root._Symbol[1]))
            else:
                std.write(str(root._Symbol))

        if parent and ( root._NType == NodeType.Operator 
                        or root._NType == NodeType.Function ): 
            std.write("(")

        print_expr( root._Right, root, tab + 1   )
        
        if parent and ( root._NType == NodeType.Operator 
                        or root._NType == NodeType.Function ):
            std.write(")")

def create_expr( root, cur_string="", parent=None, Tab=0 ): 
    """Creates a parenthesized expression of the tree pointed to by root""" 
    tab = Tab
    if root is not None:

        if parent and ( root._NType == NodeType.Operator 
                        or root._NType == NodeType.Function ): 
            cur_string +="("

        cur_string = create_expr( root._Left, cur_string, root , tab + 1 )
        if root._NType == NodeType.Literal:
            cur_string += str(root._LitVal)
        else:
            if root._Symbol is tuple:
                cur_string += str(root._Symbol[1])
            else:
                cur_string += root._Symbol

        cur_string = create_expr( root._Right, cur_string, root, tab + 1  )
        
        if parent and ( root._NType == NodeType.Operator 
                        or root._NType == NodeType.Function ):
            cur_string += ")"
    return cur_string

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

def print_tree( root ): 
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
    """ Recursive function called by the setup function print_tree().
        
        See print_tree for a descripton of the algorithm.

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

def dump_tree( root , indent=0):
    """ Line by line dump of tree pointed to by root using indentation """
    
    #if root._NType:    print("  "*indent + str(root._NType))
    if root:
        if root._Symbol:    print("--"*indent + str(root._Symbol))  
        if root._Left:      dump_tree(root._Left, indent + 1)
        if root._Right:     dump_tree(root._Right, indent + 1)


#================================ Misc and Main ===============================#

def is_digit(c): 
    if c[0] == "NUM":
        return True
    else:
        return False

def is_letter(c): 
    if c[1] in "abcdefghijklmnopqrstuvwxyz":
        return True
    else:
        return False

if __name__ == "__main__":      
    pass