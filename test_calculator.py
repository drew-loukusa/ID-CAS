import calculator as calc
from sys import stdout

try:
    from colorama import Fore, Back, Style  
    
except ImportError as e:
    pip.main(['install', colorama])
    from colorama import Fore, Back, Style

def test(text, rule_string):
    print("-"*80)
    print(Fore.GREEN+"Rule tested:"+Style.RESET_ALL,rule_string)
    print(Fore.GREEN+"Input string:"+Style.RESET_ALL, text)
    stdout.write(Fore.CYAN+"Result: "+Style.RESET_ALL)
    calc.main(text)
    print("-"*80+"\n")

def main():
    test("1", "Constant")
    test("x", "Just x")
    test("x+x", "Addition")
    test("x^2", "Exponent")
    test("x^3", "Exponent")
    test("x^3+x^3", "Addition, Exponent")

    test("sin(x)", "sin")
    test("cos(x)", "cos")
    test("tan(x)", "tan")
    test("ln(x)", "natural log")

    test("1/x", "Quotient Rule")
    test("sin(x)*x^3", "Product Rule")

    test("sin(x^3)", "Chain Rule")
    test("cos(x^3)", "Chain Rule")


if __name__ == "__main__":
    main()