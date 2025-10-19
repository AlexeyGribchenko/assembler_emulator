# hello everyone today we gonna learn c++

from command_converter import Assembler

'''
    commands:
    
    0b0000 EMPTY - do nothing
    0b0001 LOAD  - load data into ACC from operand
    0b0010 STORE - load data from ACC into operand
    0b0100 INC   - increment operand
    0b0101 DEC   - decrement operand
    0b0110 JP    - jump to istruction if result of comparement if positive
    0b0111 JN    - jump to istruction if result of comparement if negative
    0b1000 CMP   - compare ACC and operand values
    0b1001 ADD   - add up ACC with operand
    0b1010 MUL   - multiply ACC and operand
    0b1111 RET   - stop the programm

    comand:

    |-------------|-------------|--------------|---------|
    |    15-12    |     11      |      10      |   9-0   |
    |-------------|-------------|--------------|---------|
    | comand type | is register |  is address  |  value  |
    |-------------|-------------|--------------|---------|

'''

class Emulator:

    def __init__(self):
        # registers
        self.acc = 0
        self.pc = 0
        self.RON = [0] * 16
        # memory
        self.cmem = [0] * 32
        self.dmem = [0] * 16
        # flags
        self.ez = 0
        self.sf = 0
        # variables
        self.var_addresses = {}
    
    def __separate_address(self, operand):
        is_reg = (operand >> 11) & 1
        is_bracket = (operand >> 10) & 1
        value = operand & 0x3FF
        
        return is_reg, is_bracket, value

    def __handle_command(self, command, operand):

        self.pc += 1

        match command:
            case 0b0000:
                """EMPTY"""

                pass
            case 0b0001:
                """LOAD"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_bracket and not is_reg:
                    self.acc = val
                    return
                
                if is_reg and is_bracket:
                    self.acc = self.dmem[self.RON[val]]
                    return
                
                if is_bracket:
                    self.acc = self.dmem[val]
                    return
                
                if is_reg:
                    self.acc = self.RON[val]
                    return
            
            case 0b0010:
                """STORE"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_bracket and not is_reg:
                    print("Error! Can not load value into scalar!")
                    exit(1)

                if is_reg and is_bracket:
                    self.RON[val] = self.dmem[self.acc]
                    return
                elif is_reg and not is_bracket:
                    self.RON[val] = self.acc
                else:
                    self.dmem[val] = self.acc

            case 0b0100:
                """
                INC
                
                Increments value in register or in memory. Does not increment scalars!
                """

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_reg and not is_bracket:
                    raise ValueError("Error! Can not increment scalar!")

                if is_reg and is_bracket:
                    self.dmem[self.RON[val]] += 1
                    return
                
                if is_reg:
                    self.RON[val] += 1
                    return
                
                if is_bracket:
                    self.dmem[val] += 1
                    return
            
            case 0b0101:
                """
                DEC
                
                Decrements value in register or in memory. Does not decrement scalars!
                """

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_reg and not is_bracket:
                    raise ValueError("Error! Can not increment scalar!")

                if is_reg and is_bracket:
                    self.dmem[self.RON[val]] -= 1
                    return
                
                if is_reg:
                    self.RON[val] -= 1
                    return
                
                if is_bracket:
                    self.dmem[val] -= 1
                    return
            
            case 0b0110:
                """JP"""

                if self.ez == 0 and self.sf == 0:
                    self.pc = operand
                else:
                    pass

            case 0b0111:
                """JN"""

                if self.ez == 0 and self.sf == 1:
                    self.pc = operand
                else:
                    pass
            
            case 0b1000:
                """CMP"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                subtrahend = operand

                if is_reg and is_bracket:
                    subtrahend = self.dmem[self.RON[val]]
                elif is_reg:
                    subtrahend = self.RON[val]
                elif is_bracket:
                    subtrahend = self.dmem[val]

                diff = self.acc - subtrahend
                if diff > 0:
                    self.ez = 0
                    self.sf = 0
                elif diff == 0:
                    self.ez = 1
                    self.sf = 0
                else:
                    self.ez = 0
                    self.sf = 1
            
            case 0b1111:
                """RET"""
                pass

            case 0b1001:
                """ADD"""
                print('ADD')
                pass

            case 0b1010:
                """MUL"""
                print('MUL')
                pass

            case _:
                print("Error, wrong comand value!")
                exit(1)
    
    def retrieve_data(self, data: list) -> None:
        """
        Retrieves data from assembler and loads it into emulator.
        """
        self.dmem[0:len(data)] = data[:]

    def retrieve_programm(self, programm: list) -> None:
        """
        Retrieves programm from assembler and loads it into emulator.
        """
        self.cmem[0:len(programm)] = programm[:]


    def run_emulator(self, assembler: Assembler):

        assembler.assemble()

        # load data into emilator
        self.retrieve_data(assembler.data)
        self.retrieve_programm(assembler.programm)

        cmd = 0
        ad = 0

        # "programm loop"
        while cmd != 0b1111:
    
            cmd = self.cmem[self.pc] >> 12
            ad = self.cmem[self.pc] & 0xFFF

            self.__handle_command(cmd, ad)

        print(f'Maximum: {self.RON[2]}')
        print(self.dmem)


if __name__ == "__main__":

    a = Assembler('programm.txt')
    e = Emulator()
    e.run_emulator(a)