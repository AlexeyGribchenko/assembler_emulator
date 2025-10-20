import tkinter as tk
from tkinter import ttk, scrolledtext
from core import Emulator, Converter

class AssemblerIDE:

    def __init__(self, emu: Emulator, cnv: Converter):
        
        self.__root = tk.Tk()
        self.__root.title("ASSembler IDE")
        self.__root.geometry("800x600")

        self.__emu = emu
        self.__cnv = cnv
        self.__data_lables = {}

        self.__create_widgets()
        
    def __create_widgets(self):

        main_frame = ttk.Frame(self.__root, padding='10')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S, tk.E))

        self.__root.columnconfigure(0, weight=1)
        self.__root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left frame
        left_frame = ttk.Frame(main_frame, padding='10')
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        left_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.N, tk.S))
        
        # Registers frame
        data_frame = ttk.LabelFrame(left_frame, text='Данные', padding='10')
        data_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.N, tk.S, tk.E))

        service_registers = ['ACC', 'ACCH', 'PC']
        flags = ['EZ', 'SF', 'CF']
        ron_registers = ['R' + str(i) for i in range(16)]

        reg_label = ttk.Label(data_frame, text="Регистры:", font=('Arial', 10, 'bold'))
        reg_label.grid(row=0, column=0, sticky=(tk.W), pady=(0, 10))
        reg_label.__setattr__('text', 'asdsad')

        for i, reg in enumerate(service_registers):
            reg_label = ttk.Label(data_frame, text=reg)
            reg_label.grid(row=i + 1, column=0, sticky=tk.W)
            reg_value = ttk.Label(data_frame, text="0", width=8, background="white", relief="sunken")
            reg_value.grid(row=i + 1, column=1, sticky=tk.W)

            self.__data_lables[reg] = reg_value

        flg_row = 1 + len(service_registers)

        flg_label = ttk.Label(data_frame, text="Флаги:", font=('Arial', 10, 'bold'))
        flg_label.grid(row=flg_row, column=0, sticky=(tk.W), pady=(0, 0))

        for i, flg in enumerate(flags):
            flg_label = ttk.Label(data_frame, text=flg)
            flg_label.grid(row=flg_row + i + 1, column=0, sticky=tk.W)
            flg_value = ttk.Label(data_frame, text="0", width=8, background="white", relief="sunken")
            flg_value.grid(row=flg_row + i + 1, column=1, sticky=tk.W)

            self.__data_lables[flg] = flg_value

        ron_label = ttk.Label(data_frame, text="RON:", font=('Arial', 10, 'bold'))
        ron_label.grid(row=0, column=2, sticky=(tk.W), pady=(0, 10), padx=(20, 0))

        for i, ron in enumerate(ron_registers):
            ron_label = ttk.Label(data_frame, text=ron)
            ron_label.grid(row=i + 1, column=2, sticky=tk.W, padx=(20, 0))
            ron_value = ttk.Label(data_frame, text="0", width=8, background="white", relief="sunken")
            ron_value.grid(row=i + 1, column=3, sticky=tk.W)

            self.__data_lables[ron] = ron_value

        # Buttons frame
        control_frame = ttk.LabelFrame(left_frame, text='Управление', padding=10)
        control_frame.grid(row=0, column=2, columnspan=1, sticky=(tk.W, tk.N, tk.S, tk.E), padx=(20, 0))

        start_btn = ttk.Button(control_frame, text='Запустить код', command=self.run_code)
        start_btn.grid(row=0, column=0, sticky=(tk.W, tk.E))

        step_btn = ttk.Button(control_frame, text='Выполнить шаг', command=self.step_code)
        step_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        clear_btn = ttk.Button(control_frame, text='Очистить поле ввода', command=self.clear_text)
        clear_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))


        # Right frame
        right_frame = ttk.Frame(main_frame, padding='10')
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        right_frame.grid(row=0, column=2, columnspan=1, sticky=(tk.W, tk.N, tk.S, tk.E))

        code_label = ttk.Label(right_frame, text="Код на Assembler:", font=('Arial Black', 10))
        code_label.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S, tk.E))

        self.code_text = scrolledtext.ScrolledText(right_frame, width=20, height=60, font=('Consolas', 11))
        self.code_text.grid(row=1, column=0, sticky=(tk.W, tk.S, tk.E), pady=(0, 10))
    
    def run_code(self):
        """Запуск выполнения кода"""
        code = self.code_text.get("1.0", tk.END)

        # TODO: implement converting str into code, update method convert or smth
        # maybe 

        self.__cnv.convert(code)
        self.__emu.retrieve_programm(
            self.__cnv.get_data(),
            self.__cnv.get_commands()
        )
        
    def step_code(self):
        """Выполнение одного шага"""
        print("Выполнение шага")
        # Здесь будет логика пошагового выполнения
    
    def clear_text(self):
        self.code_text.delete('1.0', tk.END)

    def start(self):
        self.__root.mainloop()
        

if __name__ == "__main__":
    app = AssemblerIDE()
    app.start()