# hello everyone today we gonna learn c++

from command_converter import Converter

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
    0b1111 RET    - stop the programm

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
        self.__acc = 0
        self.__acch = 0
        self.__pc = 0
        self.__RON = [0] * 16
        # memory
        self.__cmem = [0] * 32
        self.__dmem = [0] * 16
        # flags
        self.__ez = 0
        self.__sf = 0
        self.__cf = 0
        # variables
        self.var_addresses = {}
    
    def get_flags(self):
        return {
            'ez': self.__ez,
            'sf': self.__sf,
            'cf': self.__cf
        }

    def get_registers(self):
        return {
            'acc': self.__acc,
            'acch': self.__acch,
            'pc': self.__pc,
            'RON': self.__RON.copy()
        }

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

                multipliable = val

                if is_reg and is_bracket:
                    multipliable = self.__dmem[self.__RON[val]]
                elif is_reg:
                    multipliable = self.__RON[val]
                elif is_bracket:
                    multipliable = self.__dmem[val]

                product = self.__acc * multipliable

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
    
    def run_emulator_by_steps(self) -> None:

        cmd = 0
        ad = 0

        # "programm loop"
        while cmd != 0b1111:
    
            cmd = self.__cmem[self.__pc] >> 12
            ad = self.__cmem[self.__pc] & 0xFFF

            self.__handle_command(cmd, ad)


if __name__ == "__main__":

    print("There's nothing!")