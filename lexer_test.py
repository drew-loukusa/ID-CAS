
from lexer import Lexer

#============================== Lexer Tests ===============================#

def test_method_lex_1():
	assert Lexer()._split_text("2x") == ['2','*','x','$']	

def test_method_lex_2():	
	assert Lexer()._split_text("x2") == ['x','*','2','$']

def test_method_lex_3():	
	assert Lexer()._split_text("x2x5") == ['x','*','2','*','x','*','5','$']

def test_method_lex_4():	
	assert Lexer()._split_text("x20") == ['x','*','20','$']

def test_method_lex_5():	
	assert Lexer()._split_text("20x") == ['20','*','x','$']

def test_method_lex_6():	
	assert Lexer()._split_text("20*x5*300+45") == ['20','*','x','*','5','*','300','+','45','$']

def test_method_lex_7():	
	assert Lexer()._split_text("sinx") == ['sin','x','$']

def test_method_lex_8():	
	assert Lexer()._split_text("sin(x)") == ['sin','(','x',')','$']

def test_method_lex_9():	
	assert Lexer()._split_text("sin(x)x5") == ['sin','(','x',')','*','x','*','5','$']

def test_method_lex_10():	
	assert Lexer()._split_text("sin(20*x5*300+45)") == ['sin','(','20','*','x','*','5','*','300','+','45',')','$']