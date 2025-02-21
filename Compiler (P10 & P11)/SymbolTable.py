class SymbolTable:
    def __init__(self):
        """Creates a new empty symbol table"""
        self.class_scope = {}
        self.subroutine_scope = {}
        self.indices = {
            'static': 0,
            'field': 0,
            'arg': 0,
            'local': 0
        }
        
    def start_subroutine(self):
        """Starts a new subroutine scope (resets the subroutine's symbol table)"""
        self.subroutine_scope = {}
        self.indices['arg'] = 0
        self.indices['local'] = 0
        
    def define(self, name, type, kind):
        """
        Defines a new identifier of given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and LOCAL identifiers have 
        a subroutine scope.
        """
        if kind in ['static', 'field']:
            self.class_scope[name] = {'type': type, 'kind': kind, 'index': self.indices[kind]}
            self.indices[kind] += 1
        else:  # 'arg' or 'local'
            self.subroutine_scope[name] = {'type': type, 'kind': kind, 'index': self.indices[kind]}
            self.indices[kind] += 1
            
    def var_count(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope"""
        return self.indices[kind]
        
    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns None.
        """
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['kind']
        elif name in self.class_scope:
            return self.class_scope[name]['kind']
        return None
        
    def type_of(self, name):
        """
        Returns the type of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns None.
        """
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['type']
        elif name in self.class_scope:
            return self.class_scope[name]['type']
        return None
        
    def index_of(self, name):
        """
        Returns the index assigned to the named identifier.
        If the identifier is unknown in the current scope, returns None.
        """
        if name in self.subroutine_scope:
            return self.subroutine_scope[name]['index']
        elif name in self.class_scope:
            return self.class_scope[name]['index']
        return None