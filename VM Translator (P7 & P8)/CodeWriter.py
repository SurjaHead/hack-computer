class CodeWriter():
    def __init__(self, output_file, label_count):
        self.output_file = output_file
        self.f = output_file
        self.label_count = label_count

    def write_init(self):
        # Initialize SP to 256
        self.f.write('// Bootstrap code\n')
        self.f.write('@256\n')
        self.f.write('D=A\n')
        self.f.write('@SP\n')
        self.f.write('M=D\n')
        self.write_call('Sys.init', 0)

    # To generate unique labels
    def get_label_count(self):
        return self.label_count
    
    def set_input_name(self, input_file):
        self.input_file = input_file
    
    def get_input_name(self):
        return self.input_file
    
    def write_arithmetic(self, command):
        if command == 'add':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n')
        elif command == 'sub':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n')
        elif command == 'neg':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n')
        elif command == 'eq':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@EQ_TRUE{str(self.label_count)}\nD;JEQ\n@EQ_FALSE{str(self.label_count)}\n0;JMP\n(EQ_TRUE{str(self.label_count)})\nD=-1\n@END{str(self.label_count)}\n0;JMP\n(EQ_FALSE{str(self.label_count)})\nD=0\n(END{str(self.label_count)})\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif command == 'gt':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@GT_TRUE{str(self.label_count)}\nD;JGT\n@GT_FALSE{str(self.label_count)}\n0;JMP\n(GT_TRUE{str(self.label_count)})\nD=-1\n@END{str(self.label_count)}\n0;JMP\n(GT_FALSE{str(self.label_count)})\nD=0\n(END{str(self.label_count)})\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif command == 'lt':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@LT_TRUE{str(self.label_count)}\nD;JLT\n@LT_FALSE{str(self.label_count)}\n0;JMP\n(LT_TRUE{str(self.label_count)})\nD=-1\n@END{str(self.label_count)}\n0;JMP\n(LT_FALSE{str(self.label_count)})\nD=0\n(END{str(self.label_count)})\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif command == 'and':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1\n')
        elif command == 'or':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n')
        elif command == 'not':
            self.f.write(f'// {command}\n@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n')
        self.label_count += 1
    
    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            if segment == 'constant':
                self.f.write(f"// push {segment} {index}\n@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'local':
                self.f.write(f"// push {segment} {index}\n@{index}\nD=A\n@LCL\nA=M\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'argument':
                self.f.write(f"// push {segment} {index}\n@{index}\nD=A\n@ARG\nA=M\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'this':
                self.f.write(f"// push {segment} {index}\n@{index}\nD=A\n@THIS\nA=M\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'that':
                self.f.write(f"// push {segment} {index}\n@{index}\nD=A\n@THAT\nA=M\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'temp':
                self.f.write(f"// push {segment} {index}\n@{index}\nD=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'pointer':
                if index == '0':
                    self.f.write(f"// push {segment} {index}\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                elif index == '1':
                    self.f.write(f"// push {segment} {index}\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == 'static':
                self.f.write(f"// push {segment} {index}\n@{self.input_file}.{index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        elif command == 'C_POP':
            if segment == 'local':
                self.f.write(f"// pop {segment} {index}\n@{index}\nD=A\n@LCL\nA=M\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'argument':
                self.f.write(f"// pop {segment} {index}\n@{index}\nD=A\n@ARG\nA=M\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'this':
                self.f.write(f"// pop {segment} {index}\n@{index}\nD=A\n@THIS\nA=M\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'that':
                self.f.write(f"// pop {segment} {index}\n@{index}\nD=A\n@THAT\nA=M\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'temp':
                self.f.write(f"// pop {segment} {index}\n@{index}\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == 'pointer':
                if index == '0':
                    self.f.write(f"// pop {segment} {index}\n@SP\nAM=M-1\nD=M\n@THIS\nM=D\n")
                elif index == '1':
                    self.f.write(f"// pop {segment} {index}\n@SP\nAM=M-1\nD=M\n@THAT\nM=D\n")
            elif segment == 'static':
                self.f.write(f"// pop {segment} {index}\n@SP\nAM=M-1\nD=M\n@{self.input_file}.{index}\nM=D\n")
    
    def write_label(self, label):
        self.f.write(f'// label {label}\n({label})\n')
    
    def write_goto(self, label):
        self.f.write(f'// goto {label}\n@{label}\n0;JMP\n')

    def write_if(self, label):
        self.f.write(f'// if-goto {label}\n@SP\nAM=M-1\nD=M\n@{label}\nD;JNE\n')

    def write_call(self, function_name, n_args):
        return_label = f'RETURN_ADDRESS{self.label_count}'
        # Push return address
        self.f.write(f'// call {function_name} {n_args}\n@{return_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        # Push LCL
        self.f.write(f'@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        # Push ARG
        self.f.write(f'@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        # Push THIS
        self.f.write(f'@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        # Push THAT
        self.f.write(f'@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        # ARG = SP-5-nArgs
        self.f.write(f'@SP\nD=M\n@{n_args + 5}\nD=D-A\n@ARG\nM=D\n')
        # LCL = SP
        self.f.write(f'@SP\nD=M\n@LCL\nM=D\n')
        # goto function
        self.f.write(f'@{function_name}\n0;JMP\n')
        # (return address)
        self.f.write(f'({return_label})\n')
        self.label_count += 1
    
    def write_function(self, function_name, n_vars):
        self.f.write(f'// function {function_name} {n_vars}\n({function_name})\n')
        # Initialize local variables to 0
        for _ in range(int(n_vars)):
            self.f.write('@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
    
    def write_return(self):
        # FRAME = LCL
        self.f.write('@LCL\nD=M\n@R13\nM=D\n')  # R13 is FRAME
        # RET = *(FRAME-5)
        self.f.write('@5\nA=D-A\nD=M\n@R14\nM=D\n')  # R14 is RET
        # *ARG = pop()
        self.f.write('@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n')
        # SP = ARG+1
        self.f.write('@ARG\nD=M+1\n@SP\nM=D\n')
        # THAT = *(FRAME-1)
        self.f.write('@R13\nAM=M-1\nD=M\n@THAT\nM=D\n')
        # THIS = *(FRAME-2)
        self.f.write('@R13\nAM=M-1\nD=M\n@THIS\nM=D\n')
        # ARG = *(FRAME-3)
        self.f.write('@R13\nAM=M-1\nD=M\n@ARG\nM=D\n')
        # LCL = *(FRAME-4)
        self.f.write('@R13\nAM=M-1\nD=M\n@LCL\nM=D\n')
        # goto RET
        self.f.write('@R14\nA=M\n0;JMP\n')
    
    def close(self):
        self.f.close()