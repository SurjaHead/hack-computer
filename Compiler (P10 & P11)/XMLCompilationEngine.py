from JackTokenizer import JackTokenizer

class CompilationEngine:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.indentation = 0
        open(self.output_file, 'w').close()
        self.tokenizer = JackTokenizer(input_file)
        self.compile_class()
        
    def write(self, text):
        with open(self.output_file, "a") as f:
            f.write("  " * self.indentation + text + "\n")
    
    def compile_class(self):
        self.write("<class>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # class
        self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")  # class name
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # {
        
        # Process class body
        while self.tokenizer.has_more_tokens():
            token = self.tokenizer.peek()
            if token in ["static", "field"]:
                self.compile_class_var_dec()
            elif token in ["constructor", "function", "method"]:
                self.compile_subroutine()
            elif token == "}":
                break
                
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # }
        self.indentation -= 1
        self.write("</class>")

    def compile_class_var_dec(self):
        self.write("<classVarDec>")
        self.indentation += 1
        
        # Handle static/field
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")
        # Handle type
        token = self.tokenizer.advance()
        if token in ["int", "char", "boolean"]:
            self.write("<keyword> " + token + " </keyword>")
        else:
            self.write("<identifier> " + token + " </identifier>")
        # Handle name
        self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
        
        while self.tokenizer.peek() == ",":
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ,
            self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
            
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ;
        
        self.indentation -= 1
        self.write("</classVarDec>")

    def compile_subroutine(self):
        self.write("<subroutineDec>")
        self.indentation += 1
        
        # Handle subroutine type (constructor/function/method)
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")
        
        # Handle return type
        token = self.tokenizer.advance()
        if token in ["int", "char", "boolean", "void"]:
            self.write("<keyword> " + token + " </keyword>")
        else:
            self.write("<identifier> " + token + " </identifier>")
            
        # Handle name
        self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
        
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # (
        self.compile_parameter_list()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # )
        self.compile_subroutine_body()
        
        self.indentation -= 1
        self.write("</subroutineDec>")

    def compile_parameter_list(self):
        self.write("<parameterList>")
        self.indentation += 1
        
        if self.tokenizer.peek() != ")":  # If there are parameters
            # Handle first parameter
            token = self.tokenizer.advance()
            if token in ["int", "char", "boolean"]:
                self.write("<keyword> " + token + " </keyword>")
            else:
                self.write("<identifier> " + token + " </identifier>")
            self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
            
            # Handle additional parameters
            while self.tokenizer.peek() == ",":
                self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ,
                token = self.tokenizer.advance()
                if token in ["int", "char", "boolean"]:
                    self.write("<keyword> " + token + " </keyword>")
                else:
                    self.write("<identifier> " + token + " </identifier>")
                self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
        
        self.indentation -= 1
        self.write("</parameterList>")

    def compile_subroutine_body(self):
        self.write("<subroutineBody>")
        self.indentation += 1
        
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # {
        
        while self.tokenizer.peek() == "var":
            self.compile_var_dec()
            
        self.compile_statements()
        
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # }
        
        self.indentation -= 1
        self.write("</subroutineBody>")

    def compile_var_dec(self):
        self.write("<varDec>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # var
        token = self.tokenizer.advance()
        if token in ["int", "char", "boolean"]:
            self.write("<keyword> " + token + " </keyword>")
        else:
            self.write("<identifier> " + token + " </identifier>")
            
        self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
        
        while self.tokenizer.peek() == ",":
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ,
            self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
            
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ;
        
        self.indentation -= 1
        self.write("</varDec>")
    def compile_statements(self):
        self.write("<statements>")
        self.indentation += 1
        
        while self.tokenizer.peek() != "}":
            token = self.tokenizer.peek()
            if token == "let":
                self.compile_let()
            elif token == "if":
                self.compile_if()
            elif token == "while":
                self.compile_while()
            elif token == "do":
                self.compile_do()
            elif token == "return":
                self.compile_return()
            else:
                break
        
        self.indentation -= 1
        self.write("</statements>")

    def compile_let(self):
        self.write("<letStatement>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # let
        self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")  # varName
        
        # Check for array access
        if self.tokenizer.peek() == "[":
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # [
            self.compile_expression()
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ]
            
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # =
        self.compile_expression()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ;
        
        self.indentation -= 1
        self.write("</letStatement>")

    def compile_if(self):
        self.write("<ifStatement>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # if
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # (
        self.compile_expression()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # )
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # {
        self.compile_statements()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # }
        
        # Handle else clause if present
        if self.tokenizer.peek() == "else":
            self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # else
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # {
            self.compile_statements()
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # }
            
        self.indentation -= 1
        self.write("</ifStatement>")

    def compile_while(self):
        self.write("<whileStatement>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # while
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # (
        self.compile_expression()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # )
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # {
        self.compile_statements()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # }
        
        self.indentation -= 1
        self.write("</whileStatement>")

    def compile_do(self):
        self.write("<doStatement>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # do
        
        # Handle subroutine name or className/varName
        self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
        
        # Handle possible method call
        if self.tokenizer.peek() == ".":
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # .
            self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
            
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # (
        self.compile_expression_list()
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # )
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ;
        
        self.indentation -= 1
        self.write("</doStatement>")

    def compile_return(self):
        self.write("<returnStatement>")
        self.indentation += 1
        
        self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")  # return
        
        if self.tokenizer.peek() != ";":
            self.compile_expression()
            
        self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ;
        
        self.indentation -= 1
        self.write("</returnStatement>")

    def compile_expression(self):
        self.write("<expression>")
        self.indentation += 1
        
        self.compile_term()
        while self.tokenizer.peek() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")
            self.compile_term()
            
        self.indentation -= 1
        self.write("</expression>")
        
    def compile_expression_list(self):
        self.write("<expressionList>")
        self.indentation += 1
        
        if self.tokenizer.peek() != ")":
            self.compile_expression()
            while self.tokenizer.peek() == ",":
                self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ,
                self.compile_expression()
                
        self.indentation -= 1
        self.write("</expressionList>")

    def compile_term(self):
        self.write("<term>")
        self.indentation += 1
        
        if self.tokenizer.token_type() == "INT_CONST":
            self.write("<integerConstant> " + self.tokenizer.advance() + " </integerConstant>")
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.write("<stringConstant> " + self.tokenizer.advance().strip('"') + " </stringConstant>")
        elif self.tokenizer.token_type() == "KEYWORD":
            self.write("<keyword> " + self.tokenizer.advance() + " </keyword>")
        elif self.tokenizer.token_type() == "IDENTIFIER":
            name = self.tokenizer.advance()
            self.write("<identifier> " + name + " </identifier>")
            
            if self.tokenizer.peek() == "[":  # array
                self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # [
                self.compile_expression()
                self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # ]
            elif self.tokenizer.peek() in ["(", "."]:  # subroutine call
                if self.tokenizer.peek() == ".":
                    self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # .
                    self.write("<identifier> " + self.tokenizer.advance() + " </identifier>")
                self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # (
                self.compile_expression_list()
                self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # )
        elif self.tokenizer.peek() == "(":
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # (
            self.compile_expression()
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")  # )
        else:  # unary op
            self.write("<symbol> " + self.tokenizer.advance() + " </symbol>")
            self.compile_term()
            
        self.indentation -= 1
        self.write("</term>")