from core import Converter
from core import Emulator
from gui import AssemblerIDE

def main():
    cnv = Converter()
    emu = Emulator()
    app = AssemblerIDE(emu, cnv)
    
    app.start()

if __name__ == '__main__':
    main()