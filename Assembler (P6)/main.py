import Parser
import Code
import Symbol_Table as SymbolTable

# Define the input and output file paths
input_file_path = input("Enter the path to the assembly file (.asm): ")
output_file_path = input("Enter the path and name of the output file (.hack): ")

with open(input_file_path, 'r') as file, open(output_file_path, 'w') as output_file:
    parser = Parser.Parser(file)
    decoder = Code.Code()
    symbol_table = SymbolTable.SymbolTable()
    line_number_first_pass = 0
    next_memory_address = 16  # Starting address for variables

    # FIRST PASS: Build the symbol table with label declarations
    while parser.has_more_lines():
        parser.advance()  
        current_line = parser.line.strip()

        if not current_line:
            continue              # Skip empty lines

        instruction_type = parser.instructionType()

        if instruction_type == 'L_INSTRUCTION':
            symbol = parser.symbol()
            if not symbol_table.contains(symbol):
                symbol_table.add_entry(symbol, line_number_first_pass)
        else:
            line_number_first_pass += 1

    # Reset the file pointer to the beginning for the second pass
    file.seek(0)
    parser = Parser.Parser(file)

    # SECOND PASS: Translate instructions and write to the output file
    while parser.has_more_lines():
        parser.advance()         
        current_line = parser.line.strip()

        if not current_line:
            continue              # Skip empty lines

        instruction_type = parser.instructionType()

        if instruction_type == 'L_INSTRUCTION':
            continue  # Labels are already handled in the first pass

        if instruction_type == 'A_INSTRUCTION':
            symbol = parser.symbol()
            if not symbol.isdigit():
                if not symbol_table.contains(symbol):
                    symbol_table.add_entry(symbol, next_memory_address)
                    next_memory_address += 1
                address = symbol_table.get_address(symbol)
            else:
                address = int(symbol)

            # Convert the address to a 15-bit binary string
            binary_address = bin(address)[2:].zfill(15)
            # A-instruction starts with '0'
            new_line = '0' + binary_address
            output_file.write(new_line + '\n')  # Write to the output file

        elif instruction_type == 'C_INSTRUCTION':
            # C-instruction starts with '111'
            comp_mnemonic = parser.comp()
            dest_mnemonic = parser.dest()
            jump_mnemonic = parser.jump()

            comp_bits = decoder.comp(comp_mnemonic)
            dest_bits = decoder.dest(dest_mnemonic)
            jump_bits = decoder.jump(jump_mnemonic)
            new_line = '111' + comp_bits + dest_bits + jump_bits
            output_file.write(new_line + '\n')  # Write to the output file

    print("Assembly complete. Binary instructions written to:", output_file_path)
    print("Symbol Table:", symbol_table.table)

