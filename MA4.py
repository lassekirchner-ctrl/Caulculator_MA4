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

##exc8 
memory = {0:0, 1:1}
def fib(n): #from MA1
    def _fib(n):
        if n not in memory:
            memory[n] = _fib(n-1) + _fib(n-2)
        return memory[n]
    return _fib(n)

def to_int(x):
    if type(x) != float:
        raise CalculatorSyntaxError (f'Expected an int argument, but got {x}') 
    if x < 0:
        raise CalculatorSyntaxError (f'Expected a non-negative argument')
    return int(x)

def fac_wrapper(x):
    return math.factorial(to_int(x))

def fib_wrapper(x):
    return fib(to_int(x))

##exc 8 
function_1 = {}
function_1['sin'] = math.sin
function_1['cos'] = math.cos 
function_1['exp'] = math.exp
function_1['log_10'] = math.log10 ##assue log 10
function_1['log_e'] = math.log
function_1['fac'] = fac_wrapper
function_1['fib'] = fib_wrapper


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

    ##note: while allows chained expressions like 10 = X = Y 
    while wtok.get_current() == '=': #exc 5 and 6 
        wtok.next()
        if wtok.is_name():
            name = wtok.get_current()
            wtok.next()
            variables[name] = result #adds to variables
        else:
            raise CalculatorSyntaxError ('Expected a variable name after "=" according to left to right assignment')

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

    elif wtok.is_name() == True: #ex3 ##modified in ex 8
        if wtok.get_current() in variables:
            result = variables[(wtok.get_current())]
            wtok.next()

        ##exc 8 mods
        elif wtok.get_current() in function_1:
            function_name = wtok.get_current()
            wtok.next()
            if wtok.get_current() == '(':
                wtok.next()
                arg = assignment(wtok, variables)
                if wtok.get_current() == ')':
                    wtok.next()
                    try:
                        result = function_1[function_name](arg)
                    except ValueError: #handles case like log(-10) which gives a better error msg
                        raise CalculatorSyntaxError(f"Invalid argument to {function_name}")
                else:
                    raise CalculatorSyntaxError ("Excpected ')' after function input") 
            else:
                raise CalculatorSyntaxError ('Expected "(" after a function call')
        else:
            raise CalculatorSyntaxError ('The given function or variable is not defined!')

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

        if wtok.get_current() == 'vars': ##exc 7 
            for item in variables:
                print (f'{item} = {variables[item]}')
        
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
