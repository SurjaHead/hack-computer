class Parser:
    def __init__(self, file):
        self.file = file
        self.line = None

    def has_more_lines(self):
        current_pos = self.file.tell()      # Remember current position
        line = self.file.readline()         # Attempt to read one line
        if line:                             # If non-empty, there's another line
            self.file.seek(current_pos)     # Seek back so we haven't actually consumed it
            return True
        else:
            self.file.seek(current_pos)     # Seek back even if empty, for consistency
            return False

    def advance(self):
        if self.has_more_lines():
            line = self.file.readline()
            # Remove comments (anything after '//') and strip whitespace
            line = line.split('//')[0].strip()
            self.line = line

    def instructionType(self):
        if not self.line:
            return None
        if self.line.startswith('@'):
            return 'A_INSTRUCTION'
        elif self.line.startswith('(') and self.line.endswith(')'):
            return 'L_INSTRUCTION'
        else:
            return 'C_INSTRUCTION'

    def symbol(self):
        if self.instructionType() == 'A_INSTRUCTION':
            return self.line[1:].strip()
        elif self.instructionType() == 'L_INSTRUCTION':
            return self.line[1:-1].strip()

    def dest(self):
        if self.instructionType() == 'C_INSTRUCTION' and '=' in self.line:
            return self.line.split('=')[0].strip()
        return 'null'  # Default to 'null' if no dest part

    def comp(self):
        if self.instructionType() == 'C_INSTRUCTION':
            parts = self.line.split('=')
            if len(parts) > 1:
                comp_jump = parts[1].strip()
            else:
                comp_jump = parts[0].strip()
            if ';' in comp_jump:
                return comp_jump.split(';')[0].strip()
            return comp_jump
        return '0'  # Default value

    def jump(self):
        # Only handle a jump if it's a C-instruction *and* contains ';'
        if self.instructionType() == 'C_INSTRUCTION' and ';' in self.line:
            jump_part = self.line.split(';')[1].strip()
            if not jump_part:    # e.g., "D=M;" with nothing after semicolon
                return 'null'
            return jump_part
        # If no jump, return 'null'
        return 'null'
