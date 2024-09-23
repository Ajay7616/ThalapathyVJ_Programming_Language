from lexer import lexer

def parser(tokens):
    index = 0  # Current position in the tokens list
    variables = {}  # Dictionary to store variable values

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
        print(expression)  # Print the evaluated expression
        return expression

    def parse_assignment():
        var_name = consume('VARIABLE')
        next_token = current_token()
        if next_token and next_token[0] in ('INCREMENT', 'DECREMENT',
                                            'PLUS_ASSIGN', 'MINUS_ASSIGN', 
                                            'MULTIPLY_ASSIGN', 'DIVIDE_ASSIGN', 
                                            'MODULUS_ASSIGN', 'FLOOR_DIVIDE_ASSIGN', 'EXPONENTIATION_ASSIGN'):
            # Assignment with operators
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

    # Logical Expressions: OR (kuruvi)
    def parse_logical_expression():
        left = parse_and_expression()
        while current_token() and current_token()[0] == 'OR':
            consume('OR')
            right = parse_and_expression()
            left = left or right
        return left

    # AND Expressions: AND (sura)
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
                left = (left == right)  # Evaluate the equality
            elif current_token()[0] == 'NOT_EQUALS':
                consume('NOT_EQUALS')
                right = parse_comparison_expression()
                left = (left != right)  # Evaluate the inequality
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
            elif op == '//':  # Handle floor division
                left //= right
            elif op == '%':
                left %= right  # Handle modulus operation
            elif op == '**':  # Handle exponentiation
                left **= right
            elif op == '&':
                left &= right
            elif op == '|':
                left |= right
            elif op == '^':
                left ^= right
            elif op == '<<':  # Handle left shift
                left <<= right
            elif op == '>>':  # Handle right shift
                left >>= right
        return left

    def parse_primary_expression():
        token = current_token()
        if token[0] == 'INTEGER':
            return int(consume('INTEGER'))
        elif token[0] == 'FLOAT_NUMBER':
            return float(consume('FLOAT_NUMBER'))
        elif token[0] == 'STRING':
            return consume('STRING')  # Return string without quotes
        elif token[0] == 'MULTILINE_STRING':
            return consume('MULTILINE_STRING')
        elif token[0] == 'VARIABLE':
            var_name = consume('VARIABLE')
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
            # Now parse the following INTEGER token
            if current_token() and current_token()[0] == 'INTEGER':
                return -int(consume('INTEGER'))  # Return negative integer
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
    
    def handle_indexing(var_name):
        value = variables[var_name]
        if current_token() and current_token()[0] == 'LBRACKET':
            return parse_list_indexing(var_name, value)
        return value

    def parse_list_indexing(var_name, value):
        consume('LBRACKET')
        start_index = parse_expression()  # Parse the start index

        # Initialize end_index to None
        end_index = None
        

        # Check for COLON to determine if there's an end index
        if current_token() and current_token()[-2] == 'COLON':
            consume('COLON')
            # Set end_index to the length of value if no expression follows the colon
            if current_token() and current_token()[0] != 'RBRACKET':
                end_index = parse_expression()  # Parse end index after the colon
            else:
                end_index = len(value)

        # If end_index is still None, set it based on start_index
        if end_index is None:
            if start_index >= 0:
                end_index = start_index + 1  # Set end_index to start_index + 1
            else:
                end_index = len(value)  # Default to length of value if start_index is not positive

        consume('RBRACKET')

        print(f"Variable '{var_name}': Value = '{value}', Start Index = {start_index}, End Index = {end_index}")

        # Handling slicing
        if isinstance(value, str):
            # Adjust for negative indexing
            if isinstance(start_index, int):
                # Handle negative indexing for start_index
                if start_index < 0:
                    start_index += len(value)

                # Handle negative indexing for end_index if it's defined
                if end_index is not None and end_index < 0:
                    end_index += len(value)

                # Check for valid indices
                if 0 <= start_index <= len(value) and 0 <= end_index <= len(value):
                    # Ensure start_index is always less than end_index
                    if start_index > end_index:
                        start_index, end_index = end_index, start_index
                    result = value[start_index:end_index]  # Return the sliced string
                    print(f"Slicing result: '{result}'")
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
    a = "Hello, World!"
    en_nenjil_kudi_irukkum(a[:-1])

    '''
    
    tokens = list(lexer(code))  # Convert the generator to a list
    print("Tokens:", tokens)  # Debug: Print tokens

    try:
        parser(tokens)
    except ValueError as e:
        print(f"Error: {e}")
