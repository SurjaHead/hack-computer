from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

class CompilationEngine:
    def __init__(self, input_file, output_file):
        """
        Creates a new compilation engine with the given input and output.
        The next routine called must be compileClass().
        """
        self.tokenizer = JackTokenizer(input_file)
        self.writer = VMWriter(output_file)
        self.symbol_table = SymbolTable()
        self.class_name = ""
        self.subroutine_name = ""
        self.label_count = 0
        
        # Start compilation
        self.compile_class()
        self.writer.close()
        
    def get_unique_label(self):
        """Generate a class-specific unique label"""
        label = f"{self.class_name}_{self.label_count}"
        self.label_count += 1
        return label
        
    def compile_class(self):
        """Compile a complete class"""
        # 'class' className '{' classVarDec* subroutineDec* '}'
        token = self.tokenizer.advance()  # Get 'class'
        if token != "class":
            raise SyntaxError(f"Expected 'class', got '{token}'")
        
        self.class_name = self.tokenizer.advance()  # Get className
        
        token = self.tokenizer.advance()  # Get '{'
        if token != "{":
            raise SyntaxError(f"Expected '{{', got '{token}'")
        
        # Compile class variable declarations
        while self.tokenizer.peek() in ["static", "field"]:
            self.compile_class_var_dec()
            
        # Compile subroutines
        while self.tokenizer.peek() in ["constructor", "function", "method"]:
            self.compile_subroutine()
            
        token = self.tokenizer.advance()  # Get '}'
        if token != "}":
            raise SyntaxError(f"Expected '}}', got '{token}'")
    
    def compile_class_var_dec(self):
        """Compile a static or field declaration"""
        # ('static' | 'field') type varName (',' varName)* ';'
        kind = self.tokenizer.advance()  # Get 'static' or 'field'
        var_type = self.tokenizer.advance()  # Get type
        
        # Declare first variable
        var_name = self.tokenizer.advance()  # Get varName
        self.symbol_table.define(var_name, var_type, kind)
        
        # Declare additional variables (if any)
        while self.tokenizer.peek() == ',':
            self.tokenizer.advance()  # Skip ','
            var_name = self.tokenizer.advance()  # Get next varName
            self.symbol_table.define(var_name, var_type, kind)
            
        token = self.tokenizer.advance()  # Get ';'
        if token != ";":
            raise SyntaxError(f"Expected ';', got '{token}'")
    
    def compile_subroutine(self):
        """Compile a method, function, or constructor"""
        # ('constructor' | 'function' | 'method') ('void' | type) subroutineName
        # '(' parameterList ')' subroutineBody
        
        # Reset the subroutine symbol table
        self.symbol_table.start_subroutine()
        
        subroutine_type = self.tokenizer.advance()  # Get subroutine type
        return_type = self.tokenizer.advance()  # Get return type
        self.subroutine_name = self.tokenizer.advance()  # Get subroutineName
        
        # If this is a method, define 'this' as first argument
        if subroutine_type == "method":
            self.symbol_table.define("this", self.class_name, "arg")
        
        token = self.tokenizer.advance()  # Get '('
        if token != "(":
            raise SyntaxError(f"Expected '(', got '{token}'")
            
        self.compile_parameter_list()
        
        token = self.tokenizer.advance()  # Get ')'
        if token != ")":
            raise SyntaxError(f"Expected ')', got '{token}'")
        
        # Subroutine body
        token = self.tokenizer.advance()  # Get '{'
        if token != "{":
            raise SyntaxError(f"Expected '{{', got '{token}'")
        
        # Local variables
        local_count = 0
        while self.tokenizer.peek() == "var":
            local_count += self.compile_var_dec()
        
        # Write function declaration
        full_name = f"{self.class_name}.{self.subroutine_name}"
        self.writer.write_function(full_name, local_count)
        
        # Handle constructor/method initialization
        if subroutine_type == "constructor":
            # Allocate memory for the object
            field_count = self.symbol_table.var_count("field")
            self.writer.write_push("constant", field_count)
            self.writer.write_call("Memory.alloc", 1)
            self.writer.write_pop("pointer", 0)  # Set THIS
        elif subroutine_type == "method":
            # Set THIS to the object (argument 0)
            self.writer.write_push("argument", 0)
            self.writer.write_pop("pointer", 0)
        
        # Compile statements
        self.compile_statements()
        
        token = self.tokenizer.advance()  # Get '}'
        if token != "}":
            raise SyntaxError(f"Expected '}}', got '{token}'")
    
    def compile_parameter_list(self):
        """Compile a parameter list"""
        # ((type varName) (',' type varName)*)?
        if self.tokenizer.peek() != ')':
            var_type = self.tokenizer.advance()  # Get type
            var_name = self.tokenizer.advance()  # Get varName
            self.symbol_table.define(var_name, var_type, "arg")
            
            while self.tokenizer.peek() == ',':
                self.tokenizer.advance()  # Skip ','
                var_type = self.tokenizer.advance()  # Get type
                var_name = self.tokenizer.advance()  # Get varName
                self.symbol_table.define(var_name, var_type, "arg")
    
    def compile_var_dec(self):
        """Compile a var declaration"""
        # 'var' type varName (',' varName)* ';'
        self.tokenizer.advance()  # Skip 'var'
        var_type = self.tokenizer.advance()  # Get type
        
        # Count how many local variables we declare
        var_count = 1
        
        # Declare first variable
        var_name = self.tokenizer.advance()  # Get varName
        self.symbol_table.define(var_name, var_type, "local")
        
        # Declare additional variables (if any)
        while self.tokenizer.peek() == ',':
            self.tokenizer.advance()  # Skip ','
            var_name = self.tokenizer.advance()  # Get next varName
            self.symbol_table.define(var_name, var_type, "local")
            var_count += 1
            
        token = self.tokenizer.advance()  # Get ';'
        if token != ";":
            raise SyntaxError(f"Expected ';', got '{token}'")
            
        return var_count
    
    def compile_statements(self):
        """Compile statements"""
        # statement*
        while self.tokenizer.peek() in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.peek() == "let":
                self.compile_let()
            elif self.tokenizer.peek() == "if":
                self.compile_if()
            elif self.tokenizer.peek() == "while":
                self.compile_while()
            elif self.tokenizer.peek() == "do":
                self.compile_do()
            elif self.tokenizer.peek() == "return":
                self.compile_return()
    
    def compile_let(self):
        """Compile a let statement"""
        # 'let' varName ('[' expression ']')? '=' expression ';'
        self.tokenizer.advance()  # Skip 'let'
        var_name = self.tokenizer.advance()  # Get varName
        
        # Get variable properties from symbol table
        var_kind = self.symbol_table.kind_of(var_name)
        var_index = self.symbol_table.index_of(var_name)
        
        is_array = False
        if self.tokenizer.peek() == '[':
            is_array = True
            # Array assignment: first push array base address
            self.writer.write_push(self.kind_to_segment(var_kind), var_index)
            
            self.tokenizer.advance()  # Skip '['
            self.compile_expression()  # Evaluate index expression
            
            token = self.tokenizer.advance()  # Get ']'
            if token != "]":
                raise SyntaxError(f"Expected ']', got '{token}'")
            
            # Calculate array element address (base + index)
            self.writer.write_arithmetic("add")
        
        token = self.tokenizer.advance()  # Skip '='
        if token != "=":
            raise SyntaxError(f"Expected '=', got '{token}'")
            
        self.compile_expression()  # Evaluate right-hand expression
        
        token = self.tokenizer.advance()  # Get ';'
        if token != ";":
            raise SyntaxError(f"Expected ';', got '{token}'")
        
        if is_array:
            # Array assignment
            self.writer.write_pop("temp", 0)     # Store value in temp
            self.writer.write_pop("pointer", 1)  # Set THAT to array element address
            self.writer.write_push("temp", 0)    # Restore value
            self.writer.write_pop("that", 0)     # Store value in array element
        else:
            # Simple assignment
            self.writer.write_pop(self.kind_to_segment(var_kind), var_index)
    
    def compile_if(self):
        """Compile an if statement"""
        # 'if' '(' expression ')' '{' statements '}'
        # ('else' '{' statements '}')?
        self.tokenizer.advance()  # Skip 'if'
        
        token = self.tokenizer.advance()  # Get '('
        if token != "(":
            raise SyntaxError(f"Expected '(', got '{token}'")
            
        self.compile_expression()  # Evaluate condition
        
        token = self.tokenizer.advance()  # Get ')'
        if token != ")":
            raise SyntaxError(f"Expected ')', got '{token}'")
        
        # Create labels
        else_label = self.get_unique_label()
        end_label = self.get_unique_label()
        
        # If condition is false, goto else
        self.writer.write_arithmetic("not")
        self.writer.write_if(else_label)
        
        token = self.tokenizer.advance()  # Get '{'
        if token != "{":
            raise SyntaxError(f"Expected '{{', got '{token}'")
            
        self.compile_statements()  # Compile if-block statements
        
        token = self.tokenizer.advance()  # Get '}'
        if token != "}":
            raise SyntaxError(f"Expected '}}', got '{token}'")
        
        # After if-block, go to end
        self.writer.write_goto(end_label)
        
        # Else block
        self.writer.write_label(else_label)
        if self.tokenizer.peek() == "else":
            self.tokenizer.advance()  # Skip 'else'
            
            token = self.tokenizer.advance()  # Get '{'
            if token != "{":
                raise SyntaxError(f"Expected '{{', got '{token}'")
                
            self.compile_statements()  # Compile else-block statements
            
            token = self.tokenizer.advance()  # Get '}'
            if token != "}":
                raise SyntaxError(f"Expected '}}', got '{token}'")
        
        # End of if-else
        self.writer.write_label(end_label)
    
    def compile_while(self):
        """Compile a while statement"""
        # 'while' '(' expression ')' '{' statements '}'
        self.tokenizer.advance()  # Skip 'while'
        
        # Create labels
        start_label = self.get_unique_label()
        end_label = self.get_unique_label()
        
        # Start of loop
        self.writer.write_label(start_label)
        
        token = self.tokenizer.advance()  # Get '('
        if token != "(":
            raise SyntaxError(f"Expected '(', got '{token}'")
            
        self.compile_expression()  # Evaluate condition
        
        token = self.tokenizer.advance()  # Get ')'
        if token != ")":
            raise SyntaxError(f"Expected ')', got '{token}'")
        
        # If condition is false, exit loop
        self.writer.write_arithmetic("not")
        self.writer.write_if(end_label)
        
        token = self.tokenizer.advance()  # Get '{'
        if token != "{":
            raise SyntaxError(f"Expected '{{', got '{token}'")
            
        self.compile_statements()  # Compile loop body
        
        token = self.tokenizer.advance()  # Get '}'
        if token != "}":
            raise SyntaxError(f"Expected '}}', got '{token}'")
        
        # Go back to start
        self.writer.write_goto(start_label)
        
        # End of loop
        self.writer.write_label(end_label)
    
    def compile_do(self):
        """Compile a do statement"""
        # 'do' subroutineCall ';'
        self.tokenizer.advance()  # Skip 'do'
        
        # Handle subroutine call
        self.compile_subroutine_call()
        
        # Discard the return value (must be void)
        self.writer.write_pop("temp", 0)
        
        token = self.tokenizer.advance()  # Get ';'
        if token != ";":
            raise SyntaxError(f"Expected ';', got '{token}'")
    
    def compile_return(self):
        """Compile a return statement"""
        # 'return' expression? ';'
        self.tokenizer.advance()  # Skip 'return'
        
        if self.tokenizer.peek() != ';':
            # Return with expression
            self.compile_expression()
        else:
            # Void return - push 0
            self.writer.write_push("constant", 0)
            
        self.writer.write_return()
        
        token = self.tokenizer.advance()  # Get ';'
        if token != ";":
            raise SyntaxError(f"Expected ';', got '{token}'")
    
    def compile_expression(self):
        """Compile an expression"""
        # term (op term)*
        self.compile_term()
        
        while self.tokenizer.peek() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            # Remember the operator
            op = self.tokenizer.advance()
            
            # Compile the right operand
            self.compile_term()
            
            # Apply the operator
            if op == '+':
                self.writer.write_arithmetic("add")
            elif op == '-':
                self.writer.write_arithmetic("sub")
            elif op == '*':
                self.writer.write_call("Math.multiply", 2)
            elif op == '/':
                self.writer.write_call("Math.divide", 2)
            elif op == '&':
                self.writer.write_arithmetic("and")
            elif op == '|':
                self.writer.write_arithmetic("or")
            elif op == '<':
                self.writer.write_arithmetic("lt")
            elif op == '>':
                self.writer.write_arithmetic("gt")
            elif op == '=':
                self.writer.write_arithmetic("eq")
    
    def compile_term(self):
        """Compile a term"""
        # Check token type to determine how to process the term
        token = self.tokenizer.peek()
        
        if token.isdigit():
            # Integer constant
            value = int(self.tokenizer.advance())
            self.writer.write_push("constant", value)
            
        elif token.startswith('"'):
            # String constant
            string = self.tokenizer.advance()[1:-1]  # Remove quotes
            
            # Create a new String object
            self.writer.write_push("constant", len(string))
            self.writer.write_call("String.new", 1)
            
            # Append each character
            for char in string:
                self.writer.write_push("constant", ord(char))
                self.writer.write_call("String.appendChar", 2)
                
        elif token in ['true', 'false', 'null', 'this']:
            # Keyword constant
            keyword = self.tokenizer.advance()
            
            if keyword == "true":
                self.writer.write_push("constant", 1)
                self.writer.write_arithmetic("neg")  # -1 represents true (1 neg = -1)
            elif keyword in ["false", "null"]:
                self.writer.write_push("constant", 0)
            elif keyword == "this":
                self.writer.write_push("pointer", 0)
                
        elif token == '(':
            # Parenthesized expression
            self.tokenizer.advance()  # Skip '('
            self.compile_expression()
            
            token = self.tokenizer.advance()  # Get ')'
            if token != ")":
                raise SyntaxError(f"Expected ')', got '{token}'")
                
        elif token in ['-', '~']:
            # Unary operator
            op = self.tokenizer.advance()
            self.compile_term()
            
            if op == '-':
                self.writer.write_arithmetic("neg")
            elif op == '~':
                self.writer.write_arithmetic("not")
                
        else:
            # varName | varName '[' expression ']' | subroutineCall
            identifier = self.tokenizer.advance()
            
            if self.tokenizer.peek() == '[':
                # Array access - can support arbitrary nesting like a[b[c[i]]]
                # Push array base address
                var_kind = self.symbol_table.kind_of(identifier)
                var_index = self.symbol_table.index_of(identifier)
                self.writer.write_push(self.kind_to_segment(var_kind), var_index)
                
                self.tokenizer.advance()  # Skip '['
                self.compile_expression()  # Evaluate index expression (handles nested array access)
                
                token = self.tokenizer.advance()  # Get ']'
                if token != "]":
                    raise SyntaxError(f"Expected ']', got '{token}'")
                
                # Calculate element address
                self.writer.write_arithmetic("add")
                
                # Get value from calculated address
                self.writer.write_pop("pointer", 1)  # THAT = address of array element
                self.writer.write_push("that", 0)    # Push value at that address
                
            elif self.tokenizer.peek() in ['.', '(']:
                # Subroutine call - need to back up one token
                self.tokenizer.backup()
                self.compile_subroutine_call()
                
            else:
                # Simple variable
                var_kind = self.symbol_table.kind_of(identifier)
                if var_kind is None:
                    raise ValueError(f"Undefined variable: {identifier}")
                var_index = self.symbol_table.index_of(identifier)
                self.writer.write_push(self.kind_to_segment(var_kind), var_index)
    
    def compile_subroutine_call(self):
        """Compile a subroutine call"""
        # subroutineName '(' expressionList ')' |
        # (className | varName) '.' subroutineName '(' expressionList ')'
        
        name = self.tokenizer.advance()
        
        if self.tokenizer.peek() == '.':
            # ClassName.methodName or varName.methodName
            self.tokenizer.advance()  # Skip '.'
            
            method_name = self.tokenizer.advance()
            
            if self.symbol_table.kind_of(name) is not None:
                # It's an object method call: push the object (this)
                var_type = self.symbol_table.type_of(name)
                var_kind = self.symbol_table.kind_of(name)
                var_index = self.symbol_table.index_of(name)
                
                self.writer.write_push(self.kind_to_segment(var_kind), var_index)
                full_name = f"{var_type}.{method_name}"
                args_count = 1  # including 'this'
            else:
                # It's a static function call
                full_name = f"{name}.{method_name}"
                args_count = 0
        else:
            # Direct method call within the class: push 'this'
            self.writer.write_push("pointer", 0)
            full_name = f"{self.class_name}.{name}"
            args_count = 1  # including 'this'
        
        token = self.tokenizer.advance()  # Get '('
        if token != "(":
            raise SyntaxError(f"Expected '(', got '{token}'")
        
        # Compile expression list and count arguments
        args_count += self.compile_expression_list()
        
        token = self.tokenizer.advance()  # Get ')'
        if token != ")":
            raise SyntaxError(f"Expected ')', got '{token}'")
        
        # Call the subroutine
        self.writer.write_call(full_name, args_count)
    
    def compile_expression_list(self):
        """Compile a comma-separated list of expressions"""
        # (expression (',' expression)*)?
        arg_count = 0
        
        if self.tokenizer.peek() != ')':
            self.compile_expression()
            arg_count += 1
            
            while self.tokenizer.peek() == ',':
                self.tokenizer.advance()  # Skip ','
                self.compile_expression()
                arg_count += 1
                
        return arg_count
    
    def kind_to_segment(self, kind):
        """Convert symbol kind to VM segment"""
        if kind == "static":
            return "static"
        elif kind == "field":
            return "this"
        elif kind == "arg":
            return "argument"
        elif kind == "local":
            return "local"
        else:
            raise ValueError(f"Unknown kind: {kind}")