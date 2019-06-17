#!/usr/bin/python3
#==============================================================================#
#                                                                              #
# Author: Drew Loukusa                                                         #
# Email: dlwerd@gmail.com                                                      #
# Date: 4/30/19                                                                #
#                                                                              #
# Calculator portion of my derivative calculator.                              #
#                                                                              #
#==============================================================================#

import argparse
from sys import stdout as std, argv

from derivative import find_derivative, find_integral, simplify, \
simplify_mult, simplify_expo, replace_to_simplify

from tree import Tree, print_tree, reset_seen, print_expr, create_expr  

try:
    from colorama import Fore, Back, Style  
    
except ImportError as e:
    pip.main(['install', colorama])
    from colorama import Fore, Back, Style

# Setup and parse args:
INPUT_EXPRESSION    = None
INTERACTIVE_MODE    = False
DEBUG_MODE          = False
INTEGRAL_MODE       = False
PRETTY_MODE         = False

p = argparse.ArgumentParser()
add = p.add_argument

add('-e',   dest    = 'input_expression', 
            default = INPUT_EXPRESSION, 
            help    = "Runs calculator with the given input expression")

#----------- Not functional - To be worked on at a later date. ----------
# add('-i', dest    = 'integral_mode', 
#           action  = "store_true", 
#           help    = "Switches calculator from derivative mode to integral mode")

add('--pretty', 
            dest    = 'pretty_mode', 
            action  = "store_true", 
            help    = " Enables nice answer printing.")

add('--interactive',    
            dest    = 'interactive_mode', 
            action  = "store_true", 
            help    = " Enables mode with a nice TUI and ability to enter expressions and recieve answers until you type quit.")



add('--debug',  
            dest    = 'debug', 
            action  = "store_true", 
            help    = "Displays debug info: Token stream, expression tree.")

args = p.parse_args()

def main(   
            input_expression    = INPUT_EXPRESSION,
            interactive_mode    = INTERACTIVE_MODE, 
            integral_mode       = INTEGRAL_MODE,
            pretty_mode         = PRETTY_MODE,
            debug               = DEBUG_MODE
        ):  
    #================================== Header ===============================#
    if interactive_mode and input_expression is None:
        print(Fore.BLUE+"┌"+78*"-"+"┐") 
        print("|"+Fore.RED+"Derivative Calculator".center(78, " ")+Fore.BLUE+"|")   
        print("└"+78*"-"+"┘")
        print(Style.RESET_ALL)      
    
    if not interactive_mode and input_expression is None:       
        print("Error: Must use '-e' to input an expression unless running in interactive mode.")
        p.print_help()
        quit()

    # Run in interactive mode if no expression given on startup:
    if input_expression is None and interactive_mode:
        run = True
        while run:  
            try:        
                calculate(  
                            input_string     = None,                            
                            interactive_mode = True, 
                            integral_mode    = integral_mode,
                            pretty_mode      = pretty_mode,
                            debug            = debug
                        )

            except Exception as e:
                print(e)

    else:
        try:
            return calculate(   
                        input_string     = input_expression,                        
                        interactive_mode = False, 
                        integral_mode    = integral_mode,
                        pretty_mode      = pretty_mode,
                        debug            = debug
                    )
        #except Exception as e:
        except KeyError as e:
            print(e)

def calculate(input_string, interactive_mode, integral_mode, pretty_mode, debug=False):

    #print("YOU NEED TO CONVERT THE TREE MODLUE INTO A CLASS BASED MODULE FROM A GLOBALS BASED MODULE.")
    #print("YOU STARTED IT, AND YOUR CODE WON'T WORK UNTIL IT'S DONE")
    #return 0

    if interactive_mode: 
        print("Enter an expression to differentiate: (Type 'quit' to quit)")
        input_string = input(">>> ")

    if input_string == "quit":
        quit()

    if debug:
        #====================== Input Info + Preprocessing =======================#
        print(Fore.GREEN+"Input Information:"+Style.RESET_ALL)
        print(80*"-")
        print(Fore.GREEN+"Input:"+Style.RESET_ALL,input_string)
    
    # Lex the input string into tokens:
    #-------------------------------------------------------------------------#
    from lexer import Lexer 
    foo = Lexer()
    token_stream = foo.lex(input_string)    
    if not token_stream: quit()
    #-------------------------------------------------------------------------#
    
    if debug:
        print(Fore.GREEN+"\nToken Stream:"+Style.RESET_ALL)
        
        # Print the token stream: 
        cur_line_length = 0
        for token in token_stream:
            s = str(token)
            if len(s) + cur_line_length > 80:
                std.write("\n") 
                cur_line_length = 0
            std.write(s+", ")
            cur_line_length += len(s)

    
    #print("Input String Length:", len(args[1]))    
    
    # Build The Expression Tree: 
    #-------------------------------------------------------------------------#
    root = Tree(token_stream).build_tree(debug=False)   
    #-------------------------------------------------------------------------#

    # Try to simplify the input expression tree:
    # Simplify the result expression tree:

    #UNCOMMENT THIS: Commented out temporarily for fun
    root = main_simplify( root )

    #print(Fore.GREEN+"\nNumber of nodes:"+Style.RESET_ALL, count_nodes( root ))
    reset_seen( root )
    
    if debug:
        print(Fore.GREEN+"\nNormalized input string:"+Style.RESET_ALL   )
        print_expr( root ) 
        print("\n")

        print(80*"-")
        print(Fore.GREEN+"Input Expression Tree:"+Style.RESET_ALL)
        print_tree( root )
        print()
        
        #print(80*"=")
        #print("Tree Dump:\n")
        #dump_tree(root, 0)
        #print(80*"-")
        
        #return 0
    
    #======================== Derivative Calculating =========================#
    
    # Differentiate or integrate the expression:
    #-------------------------------------------------------------------------#
    result = None
    steps = []
    if integral_mode:
        result = find_integral( root )      
    else:
        result = find_derivative( root, show_steps=True, expr_stack=steps)
    for etree in steps:
        print_expr(etree)
        print()
    #-------------------------------------------------------------------------#

    if debug:
        print(80*"-")
        print(Fore.GREEN+"Derivative Result Tree:"+Style.RESET_ALL)
        print_tree( result )

        # print("\nResult Tree Dump:")
        # dump_tree(result,0)
        
        print(80*"-")   
        print(Fore.GREEN+"Derivative Result Expression:"+Style.RESET_ALL)
        print_expr( result )
        print("\n")
    
    # Simplify the result expression tree:
    simp = main_simplify( result )

    if debug:
        print(80*"-")       
        print(Fore.GREEN+"Simplified Derivative Result Tree:"+Style.RESET_ALL)
        print_tree( simp )  
        print()
    
        print(80*"-")
        print(Fore.GREEN+"Simplified Derivative Result Expression:"+Style.RESET_ALL)
        answer = create_expr( simp )
        answer = replace_to_simplify( answer )
        if pretty_mode:
            pretty_print( answer )
        else:
            print( answer )
        #print("\n")
    else:
        if interactive_mode:
            std.write(Fore.GREEN+"Result:"+Style.RESET_ALL)
        answer = create_expr( simp )
        answer = replace_to_simplify( answer )
        
        if pretty_mode:
            pretty_print( answer )
        else:
            print( answer )
        #print("\n")
        
    del(root)
    return answer

def pretty_print( text ):
    replaces = { 
             "2":"\N{SUPERSCRIPT TWO}",
             "3":"\N{SUPERSCRIPT THREE}",
             "4":"\N{SUPERSCRIPT FOUR}",
             "5":"\N{SUPERSCRIPT FIVE}",
             "6":"\N{SUPERSCRIPT SIX}",
             "7":"\N{SUPERSCRIPT SEVEN}",
             "8":"\N{SUPERSCRIPT EIGHT}",
             "9":"\N{SUPERSCRIPT NINE}",
            }

    last = None
    i = 0
    length = len(text)
    while i < length:
        if i == len(text): break
        char = text[i]
        if char == "^":
            text
            i += 1
            char = text[i]
            rep  = replaces[char]
            text = text[0:i]+rep+text[i+1:]
            i += len(rep)
            length += len(rep)
        i += 1
    text = text.replace("*", "")
    text = text.replace("^", "")
    print(text)


def main_simplify( root ):
    #-------------------------------------------------------------------------#
    #print_tree(root)
    simp = simplify( root )
    #-------------------------------------------------------------------------#

    # Reduce coeffecients:
    #-------------------------------------------------------------------------#
    simp = simplify_mult( simp )
    simp = simplify( simp ) #, direction=None, parent=None, debug=True)

    simp = simplify_expo( simp )
    simp = simplify( simp )
    #-------------------------------------------------------------------------#
    return simp

if __name__ == "__main__":
    main(
            input_expression=args.input_expression,
            interactive_mode=args.interactive_mode, 
            pretty_mode=args.pretty_mode,
            debug=args.debug
        )