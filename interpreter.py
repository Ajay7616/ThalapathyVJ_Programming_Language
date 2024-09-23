from lexer import lexer
from parser import parser

def interpret_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    
    # Tokenize the code
    tokens = lexer(code)
    tokens_list = list(tokens)  # Convert generator to list
    
    # Parse the tokens
    parser(tokens_list)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpret_from_file(filename)
    else:
        print("Please provide the filename as an argument.")
