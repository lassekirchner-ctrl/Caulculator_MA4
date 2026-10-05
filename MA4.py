"""
Solutions to module 4 - A calculator
Student: 
Mail:
"""

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class CalculatorSyntaxError is complete as well as handling in main
of CalculatorSyntaxError and TokenError.
"""

import math
from tokenize import TokenError  
from MA4tokenizer import TokenizeWrapper


class CalculatorSyntaxError(Exception):
    pass


def statement(wtok, variables):
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    #needs to check if we are at EOL
    #use built in function from the wrapper
    if wtok.is_at_end() == False:
        raise CalculatorSyntaxError ('Expected EOL')
    return result


def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)
    return result


def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == '-':
        if wtok.get_current() == '+':
            wtok.next()
            result = result + term(wtok, variables)
        else: #handles subtraction. Doesnt handle unary minus though! 
            wtok.next()
            result = result - term(wtok, variables)
    return result


def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/': 
        if wtok.get_current() == '*':
            wtok.next()
            result = result * factor(wtok, variables)
        else:
            wtok.next()
            result = result /factor(wtok, variables)
    return result




def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise CalculatorSyntaxError("Expected ')'")
        else:
            wtok.next()          
    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()

    elif wtok.get_current() == '-': ## unary minus?
        wtok.next()
        result = -factor(wtok, variables)

    elif wtok.is_name() == True:
        if wtok.get_current() in variables:
            result = variables[(wtok.get_current())]
            wtok.next()
        else:
            raise CalculatorSyntaxError

    else:
        raise CalculatorSyntaxError(
            "Expected number, '(' or '-'") #slight mod with -  
    return result


         
def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    variables = {"ans": 0.0}
    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA4init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0]=='#':
            continue
        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit':
            print('Bye')
            exit()
        else:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result ##implementation of ex3.
                variables['PI'] = math.pi #exc4
                variables['E'] = math.e #exc4
                print('Result:', result)

            except CalculatorSyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')
 


if __name__ == "__main__":
    main()
