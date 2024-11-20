from lexer import lexer
from parser import parser

def interpret_from_file(filename):
    if not filename.endswith('.tvj'):
        print("Error: The file must have a .tvj extension.")
        return
    
    try:
        with open(filename, 'r') as file:
            code = file.read()
        
        tokens = lexer(code)
        tokens_list = list(tokens)
        
        parser(tokens_list)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        interpret_from_file(filename)
    else:
        print("Please provide the filename with a .tvj extension as an argument.")
