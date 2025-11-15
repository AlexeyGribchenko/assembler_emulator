# hello everyone today we gonna learn c++
'''
    commands:
    
    0b0000 EMPTY  - do nothing
    0b0001 LOAD   - load data into __acc from operand
    0b0010 STORE  - load data from __acc into operand
    0b0011 STOREH - load data from __accH into operand
    0b0100 INC    - increment operand
    0b0101 DEC    - decrement operand
    0b0110 JP     - jump to istruction if result of comparement if positive
    0b0111 JN     - jump to istruction if result of comparement if negative
    0b1000 CMP    - compare __acc and operand values
    0b1001 MUL    - multiply __acc and operand
    0b1010 ADD    - add up __acc with operand
    0b1011 ADH    - add up __accH with operand
    0b1100 LOADH  - load data into __acch from operand
    0b1101 - free for command
    0b1110 - free for command
    0b1111 RET    - stop the programm

    comand:

    |-------------|-------------|--------------|---------|
    |    15-12    |     11      |      10      |   9-0   |
    |-------------|-------------|--------------|---------|
    | comand type | is register |  is address  |  value  |
    |-------------|-------------|--------------|---------|

'''

class Emulator:

    class EndOfProgrammError(Exception):
        pass

    def __init__(self):
        # registers
        self.__acc = 0
        self.__acch = 0
        self.__pc = 0
        self.__RON = [0] * 16
        # memory
        self.__cmem = [0] * 64
        self.__dmem = [0] * 64
        # flags
        self.__ez = 0
        self.__sf = 0
        self.__cf = 0
        # variables
        self.var_addresses = {}

    def clear_emulator(self):
        # registers
        self.__acc = 0
        self.__acch = 0
        self.__pc = 0
        self.__RON = [0] * 16
        # memory
        self.__cmem = [0] * 64
        self.__dmem = [0] * 64
        # flags
        self.__ez = 0
        self.__sf = 0
        self.__cf = 0
        # variables
        self.var_addresses = {}

    def get_memory(self):
        return self.__dmem.copy()

    def get_registers(self):
        return {
            'ACC': self.__acc,
            'ACCH': self.__acch,
            'PC': self.__pc,
            **{f'R{i}': self.__RON[i] for i in range(16)},
            'EZ': self.__ez,
            'SF': self.__sf,
            'CF': self.__cf
        }
    
    def get_current_command(self):
        return self.__cmem[self.__pc] >> 12

    def __separate_address(self, operand):
        is_reg = (operand >> 11) & 1
        is_bracket = (operand >> 10) & 1
        value = operand & 0x3FF
        
        return is_reg, is_bracket, value

    def __handle_command(self, command, operand):

        self.__pc += 1

        match command:
            case 0b0000:
                """EMPTY"""

                pass
            case 0b0001:
                """LOAD"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_bracket and not is_reg:
                    self.__acc = val
                    return
                
                if is_reg and is_bracket:
                    self.__acc = self.__dmem[self.__RON[val]]
                    return
                
                if is_bracket:
                    self.__acc = self.__dmem[val]
                    return
                
                if is_reg:
                    self.__acc = self.__RON[val]
                    return

            case 0b1100:
                """LOADH"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_bracket and not is_reg:
                    self.__acch = val
                    return
                
                if is_reg and is_bracket:
                    self.__acch = self.__dmem[self.__RON[val]]
                    return
                
                if is_bracket:
                    self.__acch = self.__dmem[val]
                    return
                
                if is_reg:
                    self.__acch = self.__RON[val]
                    return


            case 0b0010:
                """STORE"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_bracket and not is_reg:
                    print("Error! Can not load value into scalar!")
                    exit(1)

                if is_reg and is_bracket:
                    self.__RON[val] = self.__dmem[self.__acc]
                    return
                elif is_reg and not is_bracket:
                    self.__RON[val] = self.__acc
                else:
                    self.__dmem[val] = self.__acc
                        
            case 0b0011:
                """STOREH"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_bracket and not is_reg:
                    print("Error! Can not load value into scalar!")
                    exit(1)

                if is_reg and is_bracket:
                    self.__RON[val] = self.__dmem[self.__acch]
                    return
                elif is_reg and not is_bracket:
                    self.__RON[val] = self.__acch
                else:
                    self.__dmem[val] = self.__acch


            case 0b0100:
                """
                INC
                
                Increments value in register or in memory. Does not increment scalars!
                """

                is_reg, is_bracket, val = self.__separate_address(operand)

                if not is_reg and not is_bracket:
                    raise ValueError("Error! Can not increment scalar!")

                if is_reg and is_bracket:
                    self.__dmem[self.__RON[val]] += 1
                    return
                
                if is_reg:
                    self.__RON[val] += 1
                    return
                
                if is_bracket:
                    self.__dmem[val] += 1
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
                    self.__dmem[self.__RON[val]] -= 1
                    return
                
                if is_reg:
                    self.__RON[val] -= 1
                    return
                
                if is_bracket:
                    self.__dmem[val] -= 1
                    return
            
            case 0b0110:
                """JP"""

                if self.__ez == 0 and self.__sf == 0:
                    self.__pc = operand
                else:
                    pass

            case 0b0111:
                """JN"""

                if self.__ez == 0 and self.__sf == 1:
                    self.__pc = operand
                else:
                    pass
            
            case 0b1000:
                """CMP"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                subtrahend = operand

                if is_reg and is_bracket:
                    subtrahend = self.__dmem[self.__RON[val]]
                elif is_reg:
                    subtrahend = self.__RON[val]
                elif is_bracket:
                    subtrahend = self.__dmem[val]

                diff = self.__acc - subtrahend
                if diff > 0:
                    self.__ez = 0
                    self.__sf = 0
                elif diff == 0:
                    self.__ez = 1
                    self.__sf = 0
                else:
                    self.__ez = 0
                    self.__sf = 1

            case 0b1001:
                """MUL"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                multipliable2 = val

                if is_reg and is_bracket:
                    # '[R1]' is restricted syntax
                    print("Error: '[R1]' is restricted syntax")
                    pass
                elif is_reg:
                    multipliable2 = self.__RON[val]
                elif is_bracket:
                    multipliable2 = self.__dmem[val]

                multipliable1 = self.__acch << 16 | self.__acc

                product = multipliable1 * multipliable2

                lower = product & 0xFFFF
                higher = (product >> 16) & 0xFFFF

                self.__acc = lower
                self.__acch = higher

            case 0b1010:
                """ADD"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                summand = val

                if is_reg and is_bracket:
                    summand = self.__dmem[self.__RON[val]]
                elif is_reg:
                    summand = self.__RON[val]
                elif is_bracket:
                    summand = self.__dmem[val]

                summa = self.__acc + summand

                self.__cf = summa & (1 << 16)
                self.__acc = summa & 0xFFFF

            case 0b1011:
                """ADH"""

                is_reg, is_bracket, val = self.__separate_address(operand)

                summand = val

                if is_reg and is_bracket:
                    summand = self.__dmem[self.__RON[val]]
                elif is_reg:
                    summand = self.__RON[val]
                elif is_bracket:
                    summand = self.__dmem[val]

                summa = self.__acch + summand

                self.__acch = (summa + self.__cf) & 0xFFFF
                self.__cf = 0

            case 0b1111:
                """RET"""
                pass

            case _:
                print("Error, w__RONg comand value!")
                exit(1)

    def retrieve_programm(self, data: list[int], commands: list[int]) -> None:
        """
        Retrieves programm from converter and loads it into emulator.
        """
        self.clear_emulator()

        self.__dmem[0:len(data)] = data[:]
        self.__cmem[0:len(commands)] = commands[:]


    def run_emulator(self) -> None:

        cmd = 0
        ad = 0

        # "programm loop"
        while cmd != 0b1111:
    
            cmd = self.__cmem[self.__pc] >> 12
            ad = self.__cmem[self.__pc] & 0xFFF

            self.__handle_command(cmd, ad)
    
    def next_step(self) -> None:
        cmd = self.__cmem[self.__pc] >> 12
        ad = self.__cmem[self.__pc] & 0xFFF            

        if cmd == 0b1111:
            raise Emulator.EndOfProgrammError("Programm finished!")

        self.__handle_command(cmd, ad)


if __name__ == "__main__":
    pass