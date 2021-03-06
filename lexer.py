""" 
#==============================================================================#
#                                                                              #
# Author: Drew Loukusa                                                         #
# Email: dlwerd@gmail.com                                                      #
# Date: 4/30/19                                                                #
#                                                                              #
# Lexer portion of my derivative calculator.                                   #
#                                                                              #
#==============================================================================#                                                     
"""
import re
from sys import stderr 

VAR = "x"
EOS = "$"
NUMS = "0123456789"
OPS = "+*/-^"
TRIG = "sct"
LN = "l"

class Lexer:
    def __init__(self, integral_mode=False):
        self.integral_mode = integral_mode

    def lex(self, text):
        """ Lexes 'text' into tokens and applies id's to each token. """

        # Strip any whitespace in the input string:
        text = text.replace(' ','')

        # If the calculator is running in integral mode, replace any occurance of 'x'
        # with 'x^1'. Do not relpace 'x' if it already has an power higher than 1, just 'x'.
        regex = re.compile(r"((x)[^^])")
        
        # "Split" the text into tokens
        tokens = self._split_text(text)
        if tokens:
            # If the input stream isn't empty, apply an ID to each token:
            tokens = self._apply_ids(tokens)
        return tokens

    def _split_text(self, text):
        """
            Splits text into logical chunks. sin functions, natural log, parens, numbers, variables,
            operators, etc, etc.
        """
        # Add EOS char to string:
        text = text + "$"

        # Insert explicit multiplication symbols:
        text = self._insert_explicit_mult(text)
        #print(text)

        char = ""
        last = None
        cur_num = ""
        explicit_text = []

        # ==================== Split Text into Tokens: ====================== #
        i = 0
        token = ""
        while i < len(text):
            char = text[i]
            # print(last,char, i)

            # ------------- Handle Multi Digit Numbers ------------- #
            if char in NUMS:
                token = self._parse_num(text, i)
                # print("\t",i, token)
                i += len(token) - 1
                # print("\t",i)
                char = text[i]

            # ------------- Handle Trig Functions ------------------ #
            elif char in TRIG:
                token = self._parse_trig(text, i)
                i += len(token) - 1
                # print("\t",i)
                char = text[i]

            elif char in "ln":
                token = "ln"
                i += 1
                char = text[i]

            # Add any single char as necessary:
            elif char in VAR + OPS + "()" + "e":

                # Parse negative numbers:
                if char == "-" and ((last and last in "+*/(") or (last == None)):
                    token = self._parse_num(text, i)
                    # print("\t",i, token)
                    i += len(token) - 1
                    # print("\t",i)
                    char = text[i]                  
                else:
                    token = char
            # print(last,char)
            elif char != EOS:
                raise Exception("Found unsupported character in expression: '{}'\n ".format(char))              
                return False

            if char != EOS:
                explicit_text.append(token)

            last = char
            i += 1

        explicit_text.append("$")
        return explicit_text

    def _apply_ids(self, tokens):
        """
            Applies an ID to each token in 'tokens'
            Returns a list of ID'd tokens
        """
        tokens_and_ids = []

        for token in tokens:

            token = token.lower()

            token_id = ""

            if token in "+-":
                token_id = "PLUS_OP"

            elif token in "*/":
                token_id = "MULT_OP"

            elif token == "^":
                token_id = "EXP_OP"

            elif token == VAR:
                token_id = "IDENT"

            elif self._is_number(token):
                token_id = "NUM"

            elif token == "e":
                token_id = "EULER"

            elif token == "ln":
                token_id = "LN"

            elif self._is_trig(token):
                token_id = "TRIG"

            elif token in "()":
                token_id = "PAREN"

            elif token == "$":
                token_id = "EOS"            

            tokens_and_ids.append((token_id, token))

        return tokens_and_ids

    def _insert_explicit_mult(self, text):
        """ 
            Inserts multiplication symbols to convert implicit multiplication into 
            explicit multiplication. 

            Also converts any negative signs into explicit -1 coefficients: 
                
                -sin(x) ---------> -1*sin(x)

            This isn't strictly necessary but it allows the tree building algorithm to 

        """
        i = 0
        char = text[i]
        last = None
        text = list(text)
        while char != "$":

            # If we have a VAR and a NUM next to each other, insert a mult op:
            #   This handles left and right associativity: "x5" and "5x"
            if last and (
                (char in NUMS and last in VAR) or (char in VAR and last in NUMS)
            ):
                text.insert(i, "*")

            # Handle left and right associativity on parens and nums:
            if last and (
                (char in NUMS and last in ")") or (char in "(" and last in NUMS)
            ):
                text.insert(i, "*")

            # Handle left and right associativity on parens and vars:
            if last and (
                (char in VAR and last in ")") or (char in "(" and last in VAR)
            ):
                text.insert(i, "*")

            # Change any negative signs to addition of a negative: 2-2 -> 2 + - 2
            if last and ( char in "-" and last not in OPS+"("):
                 text.insert(i, "+")
                 i += 1

            # Handle implicit negative signs. Example: -x^2 -> -1*x^2
            if last and (
                (last in "-" and char not in NUMS) 
            ):
                text.insert(i, "1")
                i += 1
                text.insert(i, "*")
                i += 1

            # Handle left and on funcs and vars:
            if last and (char in TRIG + LN and last in NUMS + "x"):
                text.insert(i, "*")

            i += 1
            last = char
            char = text[i]
        textstr = ""
        for char in text:
            textstr += char
        #print(textstr)
        return textstr

    def _parse_num(self, text, index):
        """Parses multi-digit numbers and returns them"""
        cur_num = ""
        i = index
        char = text[i]
        if char == "-": 
            cur_num += "-"
            i += 1
            char = text[i]
        while char in NUMS:
            cur_num += char
            i += 1
            char = text[i]

        return cur_num

    def _parse_trig(self, text, index):
        """Parses trig functions returns a string"""
        cur_trig = ""
        i = index
        char = text[i]
        j = 0
        while j < 3:
            cur_trig += char
            i += 1
            j += 1
            char = text[i]

        return cur_trig

    def _is_number(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def _is_trig(self, string):
        if string in ["sin", "cos", "tan"]:
            return True
        else:
            return False


def test(result, expect):
    try:
        assert result == expect
    except AssertionError as e:
        print("Test failed...")
        print("  Expected:\t" + str(expect))
        print("  Received:\t" + str(result))


if __name__ == "__main__":
    foo = Lexer()
    print(foo.Lex("20x*300+45-2"))
    print(foo.Lex("20x*300+45-2sin(x)"))

    # test(foo.Lex("20x*300*sin(x)"), ['20','*','x','*','300','*','sin','(','x',')','$'])
    # test(foo.Lex("20x*300+45-2"), ['20','*','x','*','300','+','45','-','2'])
