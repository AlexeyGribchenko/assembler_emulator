import tkinter as tk
from tkinter import ttk, scrolledtext

class AssemblerIDE:

    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Assembler IDE")
        self.root.geometry("800x600")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Область ввода кода
        ttk.Label(main_frame, text="Код на Assembler:").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.code_text = scrolledtext.ScrolledText(main_frame, width=60, height=15, font=("Courier New", 10))
        self.code_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.run_button = ttk.Button(button_frame, text="Запуск", command=self.run_code)
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.step_button = ttk.Button(button_frame, text="Выполнить по шагу", command=self.step_code)
        self.step_button.pack(side=tk.LEFT)
        
        # Панель состояния (регистры и флаги)
        status_frame = ttk.LabelFrame(main_frame, text="Состояние процессора", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(1, weight=1)
        
        # Регистры
        registers_frame = ttk.Frame(status_frame)
        registers_frame.grid(row=0, column=0, sticky=(tk.W, tk.N), padx=(0, 20))
        
        ttk.Label(registers_frame, text="Регистры", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.registers = {}
        register_names = ["ACC"] + [f"R{i}" for i in range(16)]
        
        for i, name in enumerate(register_names):
            ttk.Label(registers_frame, text=f"{name}:").grid(row=i+1, column=0, sticky=tk.W, padx=(0, 5))
            register_value = ttk.Label(registers_frame, text="0x0000", width=8, background="white", relief="sunken")
            register_value.grid(row=i+1, column=1, sticky=tk.W, pady=1)
            self.registers[name] = register_value
        
        # Флаги
        flags_frame = ttk.Frame(status_frame)
        flags_frame.grid(row=0, column=1, sticky=(tk.W, tk.N))
        
        ttk.Label(flags_frame, text="Флаги", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        self.flags = {}
        flag_names = ["EZ", "SF", "OF", "CF"]  # Zero, Sign, Overflow, Carry
        flag_descriptions = ["Ноль", "Знак", "Переполнение", "Перенос"]
        
        for i, (name, desc) in enumerate(zip(flag_names, flag_descriptions)):
            ttk.Label(flags_frame, text=f"{name} ({desc}):").grid(row=i+1, column=0, sticky=tk.W, padx=(0, 5))
            flag_value = ttk.Label(flags_frame, text="0", width=3, background="white", relief="sunken")
            flag_value.grid(row=i+1, column=1, sticky=tk.W, pady=1)
            self.flags[name] = flag_value
    
    def run_code(self):
        """Запуск выполнения кода"""
        code = self.code_text.get("1.0", tk.END)
        print("Запуск кода:")
        print(code)
        # Здесь будет логика выполнения кода
    
    def step_code(self):
        """Выполнение одного шага"""
        print("Выполнение шага")
        # Здесь будет логика пошагового выполнения
    
    def start(self):
        self.root.mainloop()
        

if __name__ == "__main__":
    app = AssemblerIDE()
    app.start()