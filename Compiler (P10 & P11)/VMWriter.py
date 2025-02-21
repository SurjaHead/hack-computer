class VMWriter:
    def __init__(self, output_file):
        """Creates a new output .vm file and prepares it for writing"""
        self.file = open(output_file, 'w')
        
    def write_push(self, segment, index):
        """Writes VM push command"""
        self.file.write(f"push {segment} {index}\n")
        
    def write_pop(self, segment, index):
        """Writes VM pop command"""
        self.file.write(f"pop {segment} {index}\n")
        
    def write_arithmetic(self, command):
        """Writes VM arithmetic command"""
        self.file.write(f"{command}\n")
        
    def write_label(self, label):
        """Writes VM label command"""
        self.file.write(f"label {label}\n")
        
    def write_goto(self, label):
        """Writes VM goto command"""
        self.file.write(f"goto {label}\n")
        
    def write_if(self, label):
        """Writes VM if-goto command"""
        self.file.write(f"if-goto {label}\n")
        
    def write_call(self, name, n_args):
        """Writes VM call command"""
        self.file.write(f"call {name} {n_args}\n")
        
    def write_function(self, name, n_locals):
        """Writes VM function command"""
        self.file.write(f"function {name} {n_locals}\n")
        
    def write_return(self):
        """Writes VM return command"""
        self.file.write("return\n")
        
    def close(self):
        """Closes the output file"""
        self.file.close()