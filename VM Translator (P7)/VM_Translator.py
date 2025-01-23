import Parser
import CodeWriter
import os

def translate_file(vm_file, code_writer):
    parser = Parser.Parser(vm_file)
    base_name = os.path.basename(vm_file.name)
    code_writer.set_input_name(os.path.splitext(base_name)[0])
    
    while parser.has_more_lines():
        parser.advance()
        if not parser.line:  # Skip empty lines
            continue
            
        cmd_type = parser.command_type()
        if cmd_type == 'C_ARITHMETIC':
            code_writer.write_arithmetic(parser.arg1())
        elif cmd_type in ['C_PUSH', 'C_POP']:
            code_writer.write_push_pop(cmd_type, parser.arg1(), parser.arg2())
        elif cmd_type == 'C_LABEL':
            code_writer.write_label(parser.arg1())
        elif cmd_type == 'C_GOTO':
            code_writer.write_goto(parser.arg1())
        elif cmd_type == 'C_IF':
            code_writer.write_if(parser.arg1())
        elif cmd_type == 'C_FUNCTION':
            code_writer.write_function(parser.arg1(), int(parser.arg2()))
        elif cmd_type == 'C_RETURN':
            code_writer.write_return()
        elif cmd_type == 'C_CALL':
            code_writer.write_call(parser.arg1(), int(parser.arg2()))

def main():
    # Get input source (file or directory)
    source = input('Enter VM file or directory name: ')
    file_names = []
    
    # Collect all VM files
    if os.path.isdir(source):
        for file_name in os.listdir(source):
            if file_name.endswith('.vm'):
                file_names.append(os.path.join(source, file_name))
    else:
        file_names.append(source)
    output_file = 'source.asm'

    # Create CodeWriter
    with open(output_file, 'w') as asm_file:
        code_writer = CodeWriter.CodeWriter(asm_file, 0)
        
        # Write bootstrap code if translating multiple files
        if len(file_names) > 1:
            code_writer.write_init()
        
        # Translate each file
        for file_name in file_names:
            with open(file_name, 'r') as vm_file:
                translate_file(vm_file, code_writer)

if __name__ == "__main__":
    main()