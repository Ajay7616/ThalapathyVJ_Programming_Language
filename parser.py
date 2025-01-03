from lexer import lexer

def parser(tokens):
    index = 0 
    variables = {}  

    def current_token():
        return tokens[index] if index < len(tokens) else None

    def consume(expected_type):
        nonlocal index
        token = current_token()
        if token and token[0] == expected_type:
            index += 1
            return token[1]
        else:
            raise ValueError(f"Expected token type {expected_type}, but got {token}")

    def parse_print_statement():
        consume('PRINT')
        consume('LPAREN')
        expression = parse_expression()
        consume('RPAREN')
        print(expression)  
        return expression

    def parse_assignment():
        var_name = consume('VARIABLE')
        next_token = current_token()
        if next_token and next_token[0] in ('INCREMENT', 'DECREMENT',
                                            'PLUS_ASSIGN', 'MINUS_ASSIGN', 
                                            'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN', 
                                            'MODULUS_ASSIGN', 'FLOOR_DIVIDE_ASSIGN', 'EXPONENTIATION_ASSIGN'):
            if next_token[0] == 'INCREMENT':
                variables[var_name] = variables.get(var_name, 0) + 1
                consume('INCREMENT')
            elif next_token[0] == 'DECREMENT':
                variables[var_name] = variables.get(var_name, 0) - 1
                consume('DECREMENT')
            elif next_token[0] == 'PLUS_ASSIGN':
                consume('PLUS_ASSIGN')
                value = parse_expression()
                variables[var_name] = variables.get(var_name, 0) + value
            elif next_token[0] == 'MINUS_ASSIGN':
                consume('MINUS_ASSIGN')
                value = parse_expression()
                variables[var_name] = variables.get(var_name, 0) - value
            elif next_token[0] == 'MULTIPLY_ASSIGN':
                consume('MULTIPLY_ASSIGN')
                value = parse_expression()
                variables[var_name] = variables.get(var_name, 0) * value
            elif next_token[0] == 'DIVIDE_ASSIGN':
                consume('DIVIDE_ASSIGN')
                value = parse_expression()
                if value == 0:
                    raise ValueError("Division by zero error")
                variables[var_name] = variables.get(var_name, 0) / value
            elif next_token[0] == 'MODULUS_ASSIGN':
                consume('MODULUS_ASSIGN')
                value = parse_expression()
                variables[var_name] = variables.get(var_name, 0) % value
            elif next_token[0] == 'FLOOR_DIVIDE_ASSIGN':
                consume('FLOOR_DIVIDE_ASSIGN')
                value = parse_expression()
                if value == 0:
                    raise ValueError("Division by zero error")
                variables[var_name] = variables.get(var_name, 0) // value
            elif next_token[0] == 'EXPONENTIATION_ASSIGN':
                consume('EXPONENTIATION_ASSIGN')
                value = parse_expression()
                variables[var_name] = variables.get(var_name, 0) ** value
        else:
            consume('ASSIGN')
            value = parse_expression()
            variables[var_name] = value
        return variables.get(var_name, 0)

    def parse_expression():
        return parse_logical_expression()

    def parse_logical_expression():
        left = parse_and_expression()
        while current_token() and current_token()[0] == 'OR':
            consume('OR')
            right = parse_and_expression()
            left = left or right
        return left

    def parse_and_expression():
        left = parse_equality_expression()
        while current_token() and current_token()[0] == 'AND':
            consume('AND')
            right = parse_equality_expression()
            left = left and right
        return left

    def parse_equality_expression():
        left = parse_comparison_expression()
        while current_token() and current_token()[0] in ('EQUALS', 'NOT_EQUALS'):
            if current_token()[0] == 'EQUALS':
                consume('EQUALS')
                right = parse_comparison_expression()
                left = (left == right)  
            elif current_token()[0] == 'NOT_EQUALS':
                consume('NOT_EQUALS')
                right = parse_comparison_expression()
                left = (left != right)  
        return left

    def parse_comparison_expression():
        left = parse_additive_expression()
        while current_token() and current_token()[0] in ('GREATER_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL'):
            op = consume(current_token()[0])
            right = parse_additive_expression()
            if op == '>':
                left = (left > right)
            elif op == '<':
                left = (left < right)
            elif op == '>=':
                left = (left >= right)
            elif op == '<=':
                left = (left <= right)
        return left

    def parse_additive_expression():
        left = parse_multiplicative_expression()
        while current_token() and current_token()[0] in ('PLUS', 'MINUS'):
            op = consume(current_token()[0])
            right = parse_multiplicative_expression()
            
            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    left = string_concatenation(left, right)
                else:
                    left += right  
            elif op == '-':
                left -= right  
        return left


    def parse_multiplicative_expression():
        left = parse_primary_expression()
        while current_token() and current_token()[0] in ('MULTIPLY', 'DIVIDE', 'FLOOR_DIVIDE', 'MODULUS', 'EXPONENTIATION', 
                                                         'BITWISE_AND', 'BITWISE_OR', 'BITWISE_XOR', 'LEFT_SHIFT', 'RIGHT_SHIFT'):
            op = consume(current_token()[0])
            right = parse_primary_expression()
            if op == '*':
                left *= right
            elif op == '/':
                left /= right
            elif op == '//': 
                left //= right
            elif op == '%':
                left %= right  
            elif op == '**':  
                left **= right
            elif op == '&':
                left &= right
            elif op == '|':
                left |= right
            elif op == '^':
                left ^= right
            elif op == '<<': 
                left <<= right
            elif op == '>>': 
                left >>= right
        return left

    def parse_primary_expression():
        token = current_token()
        if token[0] == 'INTEGER':
            return int(consume('INTEGER'))
        elif token[0] == 'FLOAT_NUMBER':
            return float(consume('FLOAT_NUMBER'))
        elif token[0] == 'STRING':
            return consume('STRING')  
        elif token[0] == 'MULTILINE_STRING':
            return consume('MULTILINE_STRING')
        elif token[0] == 'VARIABLE':
            var_name = consume('VARIABLE')
            if current_token() and current_token()[0] == 'MISMATCH':
                consume('MISMATCH')
                method_name = current_token()
                if method_name[0] in ('UPPER', 'LOWER', 'REPLACE', 'SPLIT','ALPHANUMERIC', 'ALPHA', 'CAPITALIZE',
                                      'INDEX'):
                    consume(method_name[0])  
                    consume('LPAREN')
                    if var_name in variables:
                        value = variables[var_name]
                        if method_name[0] == 'UPPER':
                            result = value.upper() if isinstance(value, str) else str(value).upper()
                        elif method_name[0] == 'LOWER':
                            result = value.lower() if isinstance(value, str) else str(value).lower()
                        elif method_name[0] == 'REPLACE':
                            old_substring = consume('STRING')  
                            consume('MISMATCH')
                            new_substring = consume('STRING')  
                            
                            if isinstance(value, str):
                                result = value.replace(old_substring, new_substring).replace(old_substring.lower(), new_substring)
                            else:
                                raise ValueError(f"REPLACE method can only be used on strings. Provided value is {type(value).__name__}")
                        elif method_name[0] == 'SPLIT':
                            separator = ' '
                            
                            if current_token() and current_token()[0] == 'STRING':
                                separator = consume('STRING')  
                            
                            if isinstance(value, str):
                                result = value.split(separator)
                            else:
                                raise ValueError(f"SPLIT method can only be used on strings. Provided value is {type(value).__name__}")
                        elif method_name[0] == 'ALPHANUMERIC':
                            if isinstance(value, str):
                                result = value.isalnum()
                            else:
                                raise ValueError(f"ALPHANUMERIC method can only be used on strings. Provided value is {type(value).__name__}")                       
                        elif method_name[0] == 'ALPHA':
                            if isinstance(value, str):
                                result = value.isalpha()
                            else:
                                raise ValueError(f"ALPHANUMERIC method can only be used on strings. Provided value is {type(value).__name__}")                        
                        elif method_name[0] == 'CAPITALIZE':
                            result = value.capitalize() if isinstance(value, str) else str(value).capitalize()
                        elif method_name[0] == 'INDEX':
                            search_substring = consume('STRING')  

                            start_position = None
                            end_position = None

                            if current_token() and current_token()[0] == 'MISMATCH':
                                consume('MISMATCH')
                                if current_token() and current_token()[0] == 'INTEGER':
                                    start_position = consume('INTEGER') 
                                    if current_token() and current_token()[0] == 'MISMATCH':
                                        consume('MISMATCH')  
                                        if current_token() and current_token()[0] == 'INTEGER':
                                            end_position = consume('INTEGER') 

                            if isinstance(value, str):
                                try:
                                    if start_position is not None and end_position is not None:
                                        result = value.index(search_substring, int(start_position), int(end_position))
                                    elif start_position is not None:
                                        result = value.index(search_substring, int(start_position))
                                    else:
                                        result = value.index(search_substring)
                                except ValueError:
                                    raise ValueError(f"Substring '{search_substring}' not found in '{value}' within the specified range")
                            else:
                                raise ValueError(f"INDEX method can only be used on strings. Provided value is {type(value).__name__}")
                        consume('RPAREN')
                        return result
                    else:
                        raise ValueError(f"Undefined variable '{var_name}'")
            else:
                if var_name in variables:
                    return handle_indexing(var_name)
                else:
                    raise ValueError(f"Undefined variable '{var_name}'")
        elif token[0] == 'LPAREN':
            consume('LPAREN')
            value = parse_expression()
            consume('RPAREN')
            return value
        elif token[0] == 'DOUBLE':
            consume('DOUBLE')
            consume('LPAREN')
            value = parse_expression()
            consume('RPAREN')
            return float(value)
        elif token[0] == 'MINUS':
            consume('MINUS')
            if current_token() and current_token()[0] == 'INTEGER':
                return -int(consume('INTEGER')) 
            raise ValueError("Expected integer after minus sign.")
        elif token[0] == 'INT':
            consume('INT')
            consume('LPAREN')
            value = parse_expression()
            consume('RPAREN')
            if isinstance(value, (int, float, str)):
                try:
                    return int(value)
                except ValueError:
                    raise ValueError(f"Cannot convert {value} to int")
            else:
                raise ValueError(f"Unsupported type for int conversion: {type(value)}")
        elif token[0] == 'FLOAT':
            consume('FLOAT')
            consume('LPAREN')
            value = parse_expression()
            consume('RPAREN')
            if isinstance(value, (int, float, str)):
                try:
                    return float(value)
                except ValueError:
                    raise ValueError(f"Cannot convert {value} to float")
                else:
                    raise ValueError(f"Unsupported type for float conversion: {type(value)}")
        elif token[0] == 'STRING_FUNC':
            consume('STRING_FUNC')
            consume('LPAREN')
            value = parse_expression()
            consume('RPAREN')
            return str(value)
        elif token[0] == 'FORMAT':
            consume('FORMAT')
            consume('LPAREN')
            format_string = consume('STRING')  
            consume('MISMATCH')  
            
            format_args = []
            while current_token() and current_token()[0] != 'RPAREN':
                format_args.append(parse_expression()) 
                if current_token() and current_token()[0] == 'MISMATCH':
                    consume('MISMATCH')  
            
            consume('RPAREN')  
            
            try:
                result = format_string.format(*format_args)
            except KeyError as e:
                raise ValueError(f"Format string error: Missing key {e}")
            
            return result
        elif token[0] == 'UPPER':
            consume('UPPER')
            consume('LPAREN')
            value = parse_expression()  
            consume('RPAREN')
            if isinstance(value, str):
                return value.upper()
            else:
                raise ValueError(f"upper() expects a string, but got {type(value)}")
        elif token[0] == 'LOWER':
            consume('LOWER')
            consume('LPAREN')
            value = parse_expression() 
            consume('RPAREN')
            if isinstance(value, str):
                return value.lower()
            else:
                raise ValueError(f"lower() expects a string, but got {type(value)}")
        elif token[0] == 'TRUE':
            consume('TRUE')
            return True
        elif token[0] == 'FALSE':
            consume('FALSE')
            return False
        elif token[0] == 'BITWISE_NOT':
            consume('BITWISE_NOT')
            value = parse_primary_expression()
            return ~value
        elif token[0] == 'NOT':
            consume('NOT')
            value = parse_primary_expression()
            result = not value
            return result
        else:
            raise ValueError(f"Unexpected token in expression: {token}")

    def string_concatenation(left, right):
        """Concatenates two strings, adding a space only if necessary."""
        if isinstance(left, str) and isinstance(right, str):
            if left.endswith(" ") or right.startswith(" "):
                return left + " " + right  
            else:
                return left + right  
        else:
            raise TypeError("Both arguments must be strings")
    
    
    def handle_indexing(var_name):
        value = variables[var_name]
        if current_token() and current_token()[0] == 'LBRACKET':
            return parse_list_indexing(var_name, value)
        return value

    def parse_list_indexing(var_name, value):
        consume('LBRACKET')

        start_index = None
        end_index = None
        
        if current_token() and current_token()[0] == 'COLON':
            consume('COLON')
            
            if current_token() and current_token()[0] == 'MINUS':
                consume('MINUS')
                end_index = -parse_expression()
            else:
                end_index = parse_expression()

            start_index = 0
        else:
            start_index = parse_expression()
        
        if current_token() and current_token()[-2] == 'COLON':
            consume('COLON')
            if current_token() and current_token()[0] != 'RBRACKET':
                end_index = parse_expression()  
            else:
                end_index = len(value)

        if end_index is None:
            if start_index >= 0:
                end_index = start_index + 1  
            else:
                end_index = len(value)  

        consume('RBRACKET')

        if isinstance(value, str):
            if isinstance(start_index, int):
                if start_index < 0:
                    start_index += len(value)

                if end_index is not None and end_index < 0:
                    end_index += len(value)

                if 0 <= start_index <= len(value) and 0 <= end_index <= len(value):
                    if start_index > end_index:
                        start_index, end_index = end_index, start_index
                    result = value[start_index:end_index] 
                    return result
                else:
                    raise ValueError(f"Index {start_index}:{end_index} out of bounds for string '{value}'")
            else:
                raise ValueError(f"Invalid start index for string slicing: {start_index}")
        else:
            raise ValueError(f"Indexing not supported for variable '{var_name}' of type {type(value).__name__}")
    


    while index < len(tokens):
        token = current_token()
        if token[0] == 'PRINT':
            parse_print_statement()
        elif token[0] == 'VARIABLE':
            next_token = tokens[index + 1] if index + 1 < len(tokens) else None
            if next_token and next_token[0] in ('ASSIGN', 'INCREMENT', 'DECREMENT',
                                                'PLUS_ASSIGN', 'MINUS_ASSIGN', 
                                                'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN',
                                                'MODULUS_ASSIGN', 'EXPONENTIATION_ASSIGN', 'FLOOR_DIVIDE_ASSIGN'):
                parse_assignment()
            else:
                raise ValueError(f"Unexpected token after variable '{token[1]}': {next_token}")
        else:
            raise ValueError(f"Unexpected token at top level: {token}")

    if index < len(tokens):
        remaining_tokens = tokens[index:]
        raise ValueError(f"Unexpected tokens remaining at end of input: {remaining_tokens}")


if __name__ == "__main__":
    code = '''en_nenjil_kudi_irukkum("Hello Thalapthy")
    txt = "Hello, welcome to my world."
    en_nenjil_kudi_irukkum(txt.thamizhan("Hello"))
    '''
    
    tokens = list(lexer(code))  
    print("Tokens:", tokens)  

    try:
        parser(tokens)
    except ValueError as e:
        print(f"Error: {e}")