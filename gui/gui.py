import tkinter as tk
from tkinter import ttk, scrolledtext
from core import Emulator, Converter

NUMBER_OF_VISIBLE_MEMORY_CELLS = 20

class AssemblerIDE:

    def __init__(self, emu: Emulator, cnv: Converter):
        
        self.__root = tk.Tk()
        self.__root.title("ASSembler IDE")
        self.__root.geometry("1100x600")

        self.__emu = emu
        self.__cnv = cnv
        
        self.__data_lables = {}
        self.__mem_lables = [None] * NUMBER_OF_VISIBLE_MEMORY_CELLS
        self.__run_code_btns = []
        self.__is_programm_finished = True

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
            reg_label = ttk.Label(data_frame, text=reg, font=('Arial', 11))
            reg_label.grid(row=i + 1, column=0, sticky=tk.W)
            reg_value = ttk.Label(data_frame, text="0", width=6, background="white", relief="sunken", font=('Arial', 11))
            reg_value.grid(row=i + 1, column=1, sticky=tk.W)

            self.__data_lables[reg] = reg_value

        flg_row = 1 + len(service_registers)

        flg_label = ttk.Label(data_frame, text="Флаги:", font=('Arial', 10, 'bold'))
        flg_label.grid(row=flg_row, column=0, sticky=(tk.W), pady=(0, 0))

        for i, flg in enumerate(flags):
            flg_label = ttk.Label(data_frame, text=flg, font=('Arial', 11))
            flg_label.grid(row=flg_row + i + 1, column=0, sticky=tk.W)
            flg_value = ttk.Label(data_frame, text="0", width=6, background="white", relief="sunken", font=('Arial', 11))
            flg_value.grid(row=flg_row + i + 1, column=1, sticky=tk.W)

            self.__data_lables[flg] = flg_value

        ron_label = ttk.Label(data_frame, text="RON:", font=('Arial', 10, 'bold'))
        ron_label.grid(row=0, column=2, sticky=(tk.W), pady=(0, 10), padx=(20, 0))

        for i, ron in enumerate(ron_registers):
            ron_label = ttk.Label(data_frame, text=ron, font=('Arial', 11))
            ron_label.grid(row=i + 1, column=2, sticky=tk.W, padx=(20, 0))
            ron_value = ttk.Label(data_frame, text="0", width=6, background="white", relief="sunken", font=('Arial', 11))
            ron_value.grid(row=i + 1, column=3, sticky=tk.W)

            self.__data_lables[ron] = ron_value

        # Memory frame
        memory_frame = ttk.Labelframe(left_frame, text='Память', padding=10)
        memory_frame.grid(row=0, column=2, columnspan=1, sticky=(tk.W, tk.N, tk.S, tk.E), padx=(20, 0))
        
        mem_label = ttk.Label(memory_frame, text="Ячейки памяти:", font=('Arial', 10, 'bold'))
        mem_label.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        for i in range(NUMBER_OF_VISIBLE_MEMORY_CELLS):
            mem_label = ttk.Label(memory_frame, text=f'dmem[{i}]', font=('Arial', 11))
            mem_label.grid(row=i + 1, column=0, sticky=tk.W)
            mem_value = ttk.Label(memory_frame, text='0', width=10, background='white', relief='sunken', font=('Arial', 11))
            mem_value.grid(row=i + 1, column=1, sticky=tk.W, padx=(5, 0))
            self.__mem_lables[i] = mem_value

        # Buttons frame
        control_frame = ttk.LabelFrame(left_frame, text='Управление', padding=10)
        control_frame.grid(row=0, column=3, columnspan=1, sticky=(tk.W, tk.N, tk.S, tk.E), padx=(20, 0))

        style = ttk.Style()
        style.configure('Custom.TButton', font=('Arial', 11))

        load_programm_btn = ttk.Button(control_frame, text="Загрузить программу", command=self.__load_code, style='Custom.TButton')
        load_programm_btn.grid(row=0, column=0, sticky=(tk.W, tk.E))

        start_btn = ttk.Button(control_frame, text='Запустить код', command=self.__run_code, style='Custom.TButton')
        start_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        start_btn.state(['disabled'])
        self.__run_code_btns.append(start_btn)

        step_btn = ttk.Button(control_frame, text='Выполнить шаг', command=self.__step_code, style='Custom.TButton')
        step_btn.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        step_btn.state(['disabled'])
        self.__run_code_btns.append(step_btn)

        clear_btn = ttk.Button(control_frame, text='Сбросить программу', command=self.__reset_programm, style='Custom.TButton')
        clear_btn.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        # Right frame
        right_frame = ttk.Frame(main_frame, padding='10')
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        right_frame.grid(row=0, column=2, columnspan=1, sticky=(tk.W, tk.N, tk.S, tk.E))

        code_label = ttk.Label(right_frame, text="Код на Assembler:", font=('Arial Black', 10))
        code_label.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S, tk.E))

        self.__code_text_field = scrolledtext.ScrolledText(right_frame, width=20, height=60, font=('Consolas', 11))
        self.__code_text_field.grid(row=1, column=0, sticky=(tk.W, tk.S, tk.E), pady=(0, 10))
    
    def __load_code(self):
        code_text = self.__code_text_field.get("1.0", tk.END)

        self.__cnv.convert(code_text)

        self.__emu.retrieve_programm(
            self.__cnv.get_data(),
            self.__cnv.get_commands()
        )

        self.__is_programm_finished = False
        for btn in self.__run_code_btns:
            btn.state(['!disabled'])

        self.__update_memory_lables()

    def __run_code(self):
        self.__emu.run_emulator()
        self.__update_register_lables()
        self.__update_memory_lables()
        self.__finish_programm()

    def __step_code(self):
        if self.__is_programm_finished:
            return
        
        try:
            self.__emu.next_step()
        except Emulator.EndOfProgrammError as e:
            self.__finish_programm()

        self.__update_register_lables()
        self.__update_memory_lables()
    
    def __update_register_lables(self):
        for key, value in self.__emu.get_registers().items():
            self.__data_lables[key].config(text=value)

    def __update_memory_lables(self):

        mem_cells = self.__emu.get_memory()
        mem_cells = mem_cells[:min(NUMBER_OF_VISIBLE_MEMORY_CELLS, len(mem_cells))]

        for i, mem_cell in enumerate(mem_cells):
            self.__mem_lables[i].config(text=mem_cell)

    def __finish_programm(self):
        self.__is_programm_finished = False
        for btn in self.__run_code_btns:
            btn.state(['disabled'])

    def __reset_programm(self):
        self.__code_text_field.delete('1.0', tk.END)
        self.__emu.clear_emulator()
        self.__update_register_lables()
        self.__update_memory_lables()


    def start(self):
        self.__root.mainloop()
        

if __name__ == "__main__":
    app = AssemblerIDE()
    app.start()