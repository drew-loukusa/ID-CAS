import calculator as calc

def main():
    calc.main("1")
    calc.main("x")
    calc.main("x+x")
    calc.main("x^2")
    calc.main("x^3")
    calc.main("x^3+x^3")

    calc.main("sin(x)")
    calc.main("cos(x)")
    calc.main("tan(x)")
    calc.main("ln(x)")

    calc.main("1/x")
    calc.main("sin(x)*x^3")

    calc.main("sin(x^3)")
    calc.main("cos(x^3)")


if __name__ == "__main__":
    main()