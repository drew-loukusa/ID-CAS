
from lexer import Lexer

#============================ Implicit to Explicit ===========================#

def test_method_lex_1():
	assert Lexer().Lex("2x") == ['2','*','x']	

def test_method_lex_2():	
	assert Lexer().Lex("x2") == ['x','*','2']

def test_method_lex_3():	
	assert Lexer().Lex("x2x5") == ['x','*','2','*','x','*','5']

def test_method_lex_4():	
	assert Lexer().Lex("x20") == ['x','*','20']

def test_method_lex_5():	
	assert Lexer().Lex("20x") == ['20','*','x']

def test_method_lex_6():	
	assert Lexer().Lex("20*x5*300+45") == ['20','*','x','*','5','*','300','+','45']

