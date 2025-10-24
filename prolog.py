######################################################################################################
######################################################################################################
##
##
##  This work is the doing of:
##  1. Karim Elsayed (b00092054) 
##  2. Khalid Mohamed (b00087968)
##   
##  This work is submitted to Dr. Michel Pasquier as part of 
##  CMP321 course project assignment. 
##
##
##
from lark import Lark
from lark import exceptions
import regex as re

# building the parser for the grammar
prolog_parser = Lark(r"""
    program: [clause (clause)*] query
    clause: predicate [":-" predicatelst] "."
    predicatelst: predicate ("," predicate)*
    query: "?""-" predicatelst "."
    termlst: term ("," term)*
    predicate: atom ["(" termlst ")"]
    term: atom | variable | structure | numeral
    structure: atom "(" termlst ")"
    atom: smallatom | "'" string "'"
    smallatom: lowercasechar[characterlst]
    variable: uppercasechar[characterlst]
    alphanumeric: lowercasechar | uppercasechar | digit
    characterlst: alphanumeric (alphanumeric)*
    numeral: digit (digit)*
    character: alphanumeric | special
    string: character (character)*
    lowercasechar: "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
    uppercasechar: "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "_"
    digit: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
    special: "+" | "-" | "*" | "/" | "\\" | "^" | "~" | ":" | "." | "?" | " " | "#" | "$" | "&"

    %import common.WS                     
    %ignore WS
                     
                     """, start = 'program') # start parsing from program



# reads the txt files, then returns a list containing all string formated programs to be parsed
def get_files_content():
    counter = 1 # starts by reading 1.txt 
    file_lst = [] # list to store the txt file content 
    try:
        while True:
            txtfile = open(f'{counter}.txt')
            file_lst.append(txtfile.read())
            counter+=1
    except: pass # would mean we do not have any files left to read
    return file_lst 

# checks if code is syntactically correct 
def is_correct(program):
    try:
        prolog_parser.parse(program) # if no exception catched, code is correct.
        return True
    except Exception as e: # if code is no syntactically correct, it returns an exception
        return False # returns false as code is not correct
    
# functions for basic errors:

# check if expression has a missing closing bracket 
def has_missing_closing_brackets(sub_program):
    return sub_program.count('(') > sub_program.count(')')

# check if an expression has a missing opening bracket
def has_missing_opening_brackets(sub_program):
    return sub_program.count('(') < sub_program.count(')')

# check if user is using an unknown character to the grammar
def is_unknown_char(letter):
    return bool(re.match(r'[^A-Za-z0-9+\-*/~\\:.,?#$&()]', letter))

# function to write meaningful message to the output file
def parse(program):
    if not is_correct(program):
        # returns the error message in the form of a string
        # one file can consist of many error msgs

        output_msg = ''
        done = False
        while not done:
            try:
                prolog_parser.parse(program)
                done = True  # if it is paresd correctly, stop
            except exceptions.UnexpectedEOF:
                return output_msg
            except Exception as e:
                err = str(e).split('\n')   # getting each line in the error exception message
                col_num = int(err[0].split(' ')[-1]) # extracting the column number (i.e. which character is causing the error)
                line_num = int(err[0].split(' ')[-3]) # extracting the line that has the error
                err_part = err[2].strip()  # getting the expression cuasing the error
                # check if the error is possibly a missing closing or opening brackets
                # or check if the error is a character that is not defined in the grammar
                if is_unknown_char(err[2][col_num - 1]):
                    output_msg += f'Unknown character {err[2][col_num - 1]} in line {line_num} character {col_num} at "{err_part}"\n'
                elif has_missing_closing_brackets(err_part):
                    output_msg += f'Missing closing paranthesis in line {line_num} at "{err_part}"\n'
                elif has_missing_opening_brackets(err_part):
                    output_msg += f'Missing opening paranthesis in line {line_num} at "{err_part}"\n'
                else:
                    output_msg += f'Unexpected {err[2][col_num - 1]} in line {line_num} character {col_num} at "{err_part}"\n'
                program = program.replace(err_part.rstrip(), '', 1)   # remove that line from program, then parse again   
                # if parsing is correct, function will terminate only showing the error messages for wrong syntax  
        return output_msg        
            
    else:
        return 'Code is syntactically correct!\n'
    

# read the files sequentially starting from 1.txt to n.txt where n is the number of files
counter = 1
with open('output.txt', 'w') as file:
    for program in get_files_content():
        file.write(75*"#")
        file.write('\n')
        file.write(f'{counter}.txt:\n')
        msgs = parse(program)  # get the msgs
        file.write(msgs)       # write the messages to the output.txt file
        counter+=1