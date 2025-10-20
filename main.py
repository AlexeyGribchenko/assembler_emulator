from core import Converter
from core import Emulator
# from gui import AssemblerIDE

def main():
    cnv = Converter("./programms/sum_mul.txt")
    cnv.convert()

    eml = Emulator()
    eml.retrieve_programm(cnv.get_data(), cnv.get_commands())

    # app = AssemblerIDE()
    # app.start()

if __name__ == '__main__':
    main()