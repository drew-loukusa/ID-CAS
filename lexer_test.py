
from lexer import Lexer

#============================ Implicit to Explicit ===========================#

def test_implict_to_explicit_1():
	assert Lexer().Lex("2x") == ['2','*','x']	

def test_implict_to_explicit_2():	
	assert Lexer().Lex("x2") == ['x','*','2']

def test_implict_to_explicit_3():	
	assert Lexer().Lex("x2x5") == ['x','*','2','*','x','*','5']

def test_implict_to_explicit_4():	
	assert Lexer().Lex("x20") == ['x','*','20']