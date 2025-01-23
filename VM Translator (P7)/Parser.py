# Parser.py

class Parser:
    def __init__(self, file):
        self.file = file
        self.line = None

    def has_more_lines(self):
        current_pos = self.file.tell()      # Remember current position
        line = self.file.readline()         # Attempt to read one line
        if line:
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

    def command_type(self):
        if not self.line:
            return None
        if self.line.startswith('push'):
            return 'C_PUSH'
        elif self.line.startswith('pop'):
            return 'C_POP'
        elif self.line.startswith('label'):
            return 'C_LABEL'
        elif self.line.startswith('goto'):
            return 'C_GOTO'
        elif self.line.startswith('if-goto'):
            return 'C_IF'
        elif self.line.startswith('function'):
            return 'C_FUNCTION'
        elif self.line.startswith('return'):
            return 'C_RETURN'
        elif self.line.startswith('call'):
            return 'C_CALL'
        else:
            return 'C_ARITHMETIC'

    def arg1(self):
        ctype = self.command_type()
        if ctype == 'C_ARITHMETIC':
            return self.line.split()[0]
        else:
            return self.line.split()[1]

    def arg2(self):
        return self.line.split()[2]
