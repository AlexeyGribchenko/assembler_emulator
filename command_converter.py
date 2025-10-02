COMMANDS = {
    'EMPTY': 0b0000,
    'LOAD': 0b0001,
    'STORE': 0b0010,
    'INC': 0b0100,
    'DEC': 0b0101,
    'JP': 0b0110,
    'JN': 0b0111,
    'CMP': 0b1000,
    'RET': 0b1111
}

class Assembler:

    def __init__(self, filename):
        self.points = {}
        self.programm = []
        self.data = {}
        self.filename = filename

    def parse_operand(self, operand):
        """
        Returns value, is_register, is_address.
        
        value - scalar value or memory address or register number.
        
        is_register - indicates if operand register or not.
        
        is_address - indicates whether to work with the memoty or with the value.
        """

        operand = operand.strip()
        is_address = '[' in operand
        
        clean_operand = operand.replace('[', '').replace(']', '') if is_address else operand
        is_register = clean_operand.startswith('R') and clean_operand[1:].isdigit()

        reg_number = clean_operand[1:] if is_register else clean_operand

        try:
            value = int(reg_number)
        except ValueError:
            value = reg_number
        
        return value, is_register, is_address

    def first_pass(self):
        """
        First pass. Collecting marks.
        Example:

            MARK:
        """

        with open(self.filename, 'r') as file:
            command_index = 0

            for line in file:
                words = line.strip().split()
                
                if len(words) == 0:
                    continue

                if len(words) == 1 and words[0].endswith(':'):
                    label = words[0][:-1]
                    self.points[label] = command_index
                elif words[0] in COMMANDS:
                    command_index += 1
        
    def second_pass(self):
        """
        Second pass. Machine code generation.
        Example:

            LOAD [R1] -> 0b00011100000000001
        """

        with open(self.filename, 'r') as file:
            command_insex = 0

            for line in file:
                words = line.strip().split()

                if len(words) == 0:
                    continue

                if len(words) == 1 and words[0].endswith(':'):
                    command_insex += 1
                    continue

                if words[0] not in COMMANDS:
                    continue
                    
                command = words[0]
                cmd_code = COMMANDS[command] << 12
                val = 0
                reg = 0
                ad = 0
                
                if len(words) == 1:
                    result = cmd_code
                
                elif len(words) == 2:
                    operand = words[1]

                    if command in ['JP', 'JN']:
                        if operand not in self.points:
                            raise ValueError(f'Error! Wrong operand value!\ncommand: {command}\nvalue: {operand}')
                        val = self.points[operand]
                    else:
                        val, reg, ad = self.parse_operand(operand)
                        # FOR WORK WITH DATA
                        # if isinstance(val, str) and val in seld.data:
                        #     val = self.data[val]
                    
                    result = cmd_code | reg << 11 | ad << 10 | val
                
                else:
                    raise ValueError('Error! Invalid syntax:', line)
                
                # print(f'self.cmem[{command_insex}] = {bin(result)} {words[0]}')

                self.programm.append(result)
                command_insex += 1
    
    def third_pass(self):

        section_data_found = False

        with open(self.filename, 'r') as file:

            for line in file:
                if 'section .text' in line:
                    break

                if 'section .data' in line:
                    section_data_found = True
                    continue
                
                if not section_data_found:
                    continue
                
                words = line.strip().split()

                if len(words) == 0:
                    continue
                
                if len(words) == 1:
                    raise ValueError(f"Error! Wrong number of arguments in line: {len(words)}")
                
                if not isinstance(words[0], str):
                    raise ValueError(f"Error! Wrong name for variable: {words[0]}")

                self.data[words[0]] = [int(words[i].replace(',', '')) for i in range(1, len(words))]


    def print_commands(self):

        for i, command in enumerate(self.programm):
            print(f'self.cmem[{i}] = {bin(command)}')

    def assemble(self):
        self.first_pass()
        self.second_pass()
        self.third_pass()


if __name__ == "__main__":
        
    a = Assembler('programm.txt')
    a.assemble()
    print(a.data)
