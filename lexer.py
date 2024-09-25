import re

# Define token types and regular expressions
token_specification = [
    ('MULTILINE_STRING', r'""".*?"""|\'\'\'.*?\'\'\''),
    ('PRINT', r'en_nenjil_kudi_irukkum'),
    ('UPPER', r'yeru_yeru_muneru'),  # Uppercase string function
    ('LOWER', r'life_is_very_short_nanba'),
    ('PLUS_ASSIGN', r'\+='), 
    ('MINUS_ASSIGN', r'-='), 
    ('EXPONENTIATION_ASSIGN', r'\*\*='),  
    ('MULTIPLY_ASSIGN', r'\*='), 
    ('DIVIDE_ASSIGN', r'/='),  
    ('MODULUS_ASSIGN', r'%='),  
    ('FLOOR_DIVIDE_ASSIGN', r'//='),  
    ('DOUBLE', r'coca_cola'), 
    ('STRING_FUNC', r'naa_guru_than_pesuren'),  
    ('LPAREN', r'\('), 
    ('RPAREN', r'\)'), 
    ('FLOAT', r'nei_nei_eduthutu_vaa'),  
    ('INT', r'nei_eduthutu_vaa'),        
    ('TRUE', r'naa_thanda_leo'),         
    ('FALSE', r'naa_avan_illa'),
    ('EQUALS', r'=='),
    ('NOT_EQUALS', r'!='),  
    ('GREATER_THAN_EQUAL', r'>='),  
    ('LESS_THAN_EQUAL', r'<='),  
    ('LEFT_SHIFT', r'<<'),  # Zero fill left shift
    ('RIGHT_SHIFT', r'>>'),  # Signed right shift
    ('GREATER_THAN', r'>'),
    ('LESS_THAN', r'<'),
    ('AND', r'sura'),      # Logical AND
    ('OR', r'kuruvi'),      # Logical OR
    ('NOT', r'villu'),      # Logical NOT
    ('VARIABLE', r'[a-zA-Z_][a-zA-Z_0-9]*'),  
    ('ASSIGN', r'='), 
    ('INCREMENT', r'\+\+'),
    ('DECREMENT', r'--'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('FLOOR_DIVIDE', r'//'),
    ('DIVIDE', r'/'),
    ('MODULUS', r'%'),  
    ('EXPONENTIATION', r'\*\*'),  
    ('MULTIPLY', r'\*'),  
    ('FLOAT_NUMBER', r'\d+\.\d+'),  
    ('INTEGER', r'\d+'),            
    ('STRING', r'"[^"]*"'),
    ('BITWISE_AND', r'&'), 
    ('BITWISE_OR', r'\|'), 
    ('BITWISE_XOR', r'\^'),
    ('BITWISE_NOT', r'~'),  
    ('LBRACKET', r'\['), 
    ('RBRACKET', r'\]'),
    ('COLON', r'\:'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('MISMATCH', r'.'),
]

# Create a regex pattern from token specifications
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

def lexer(code):
    for match in re.finditer(token_regex, code, re.DOTALL):
        type_ = match.lastgroup
        value = match.group()
        if type_ == 'NEWLINE':
            continue
        elif type_ == 'SKIP':
            continue
        elif type_ == 'STRING':
            value = value[1:-1]
        elif type_ == 'MULTILINE_STRING':
            value = value[3:-3]  # Remove the surrounding quotes
        elif type_ == 'INTEGER':
            value = int(value)
        elif type_ == 'FLOAT_NUMBER':
            value = float(value)
        elif type_ in ('INT', 'FLOAT', 'DOUBLE', 'STRING_FUNC'):
            pass  # Preserve original strings
        elif type_ == 'TRUE':
            value = True  # Convert to Python boolean True
        elif type_ == 'FALSE':
            value = False  # Convert to Python boolean False
        elif type_ == 'UPPER':
            # Find next token and apply .upper() method
            next_token = next(lexer(code), None)
            if next_token and next_token[0] == 'STRING':
                value = next_token[1].upper()
        
        elif type_ == 'LOWER':
            # Find next token and apply .lower() method
            next_token = next(lexer(code), None)
            if next_token and next_token[0] == 'STRING':
                value = next_token[1].lower()

        yield (type_, value)

if __name__ == "__main__":
    code = '''en_nenjil_kudi_irukkum("Hello Thalapthy") 
    a = "Hello World"
    a = "Hello World"
    en_nenjil_kudi_irukkum(a.yeru_yeru_muneru())
    en_nenjil_kudi_irukkum(a.life_is_very_short_nanba())
    '''
    
    tokens = list(lexer(code))  # Convert the generator to a list
    print("Tokens:", tokens)  # Debug: Print tokens
