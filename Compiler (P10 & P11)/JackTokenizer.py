class JackTokenizer:
    def __init__(self, file):
        self.file = open(file, 'r')
        self.tokens = []
        self.token_index = 0
        self.token_history = []
        
        # Read and process the file line by line
        for line in self.file:
            # Remove comments and whitespace
            line = line.split('//')[0].strip()
            if not line:
                continue
            
            # Process the line character by character
            i = 0
            while i < len(line):
                # Skip whitespace
                if line[i].isspace():
                    i += 1
                    continue
                
                # Handle symbols
                if line[i] in ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']:
                    self.tokens.append(line[i])
                    i += 1
                    continue
                
                # Handle string constants
                if line[i] == '"':
                    string_val = ""
                    i += 1
                    while i < len(line) and line[i] != '"':
                        string_val += line[i]
                        i += 1
                    if i < len(line):  # Make sure we found the closing quote
                        self.tokens.append('"' + string_val + '"')
                    i += 1
                    continue
                
                # Handle words (keywords or identifiers)
                if line[i].isalnum() or line[i] == '_':
                    word = ""
                    while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                        word += line[i]
                        i += 1
                    self.tokens.append(word)
                    continue
                
                i += 1
        
        print("Tokens:", self.tokens)  # Debug print
        self.file.close()
        self.current_token = None

    def has_more_tokens(self):
        # Check if there are more tokens to process
        return self.token_index < len(self.tokens)

    def advance(self):
        if self.has_more_tokens():
            if self.current_token is not None:
                self.token_history.append(self.current_token)
            self.current_token = self.tokens[self.token_index]
            print(f"Advancing to token: {self.current_token}")  # Debug print
            self.token_index += 1
            return self.current_token
        return None

    def backup(self):
        if self.token_index > 0 and self.token_history:
            self.token_index -= 1
            self.current_token = self.tokens[self.token_index]
            print(f"Backing up to token: {self.current_token}")  # Debug print
            return self.current_token
        return None

    def peek(self, offset=0):
        peek_index = self.token_index + offset
        if 0 <= peek_index < len(self.tokens):
            print(f"Peeking at token: {self.tokens[peek_index]}")  # Debug print
            return self.tokens[peek_index]
        return None

    def current_token(self):
        if self.token_index > 0:
            return self.tokens[self.token_index - 1]
        return None

    def token_type(self):
        # Determine the type of the current token
        if not self.has_more_tokens():
            return None
            
        token = self.tokens[self.token_index]
        
        # Check for symbol
        if token in ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', 
                    '-', '*', '/', '&', '|', '<', '>', '=', '~']:
            return 'SYMBOL'
            
        # Check for integer constant
        if token.isdigit():
            return 'INT_CONST'
            
        # Check for keyword
        if token in ['class', 'constructor', 'function', 'method', 'field', 
                    'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 
                    'false', 'null', 'this', 'let', 'do', 'if', 'else', 
                    'while', 'return']:
            return 'KEYWORD'
            
        # Check for string constant
        if token.startswith('"'):
            return 'STRING_CONST'
            
        # If none of the above, it must be an identifier
        return 'IDENTIFIER'

    def keyword(self):
        if self.token_type() == 'KEYWORD':
            return self.tokens[self.token_index]
        return None

    def symbol(self):
        if self.token_type() == 'SYMBOL':
            return self.tokens[self.token_index]
        return None
        
    def identifier(self):
        if self.token_type() == 'IDENTIFIER':
            return self.tokens[self.token_index]
        return None
        
    def int_val(self):
        if self.token_type() == 'INT_CONST':
            return int(self.tokens[self.token_index])
        return None
        
    def string_val(self):
        if self.token_type() == 'STRING_CONST':
            return self.tokens[self.token_index].strip('"')
        return None