import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        
        # Entry field for display
        self.display = ttk.Entry(root, justify="right", font=("Arial", 20))
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Button layout
        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        
        # Create and place buttons
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.button_click(x)
            ttk.Button(root, text=button, command=cmd).grid(
                row=row, column=col, padx=2, pady=2, sticky="nsew"
            )
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Clear button
        ttk.Button(root, text="C", command=self.clear).grid(
            row=row, column=0, columnspan=4, padx=2, pady=2, sticky="nsew"
        )
        
        # Configure grid weights
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        
        self.current = ""
        self.operation = None
        self.first_number = None

    def button_click(self, value):
        if value.isdigit() or value == ".":
            self.current += value
            self.display.delete(0, tk.END)
            self.display.insert(0, self.current)
        elif value in ["+", "-", "*", "/"]:
            if self.current:
                if self.first_number is None:
                    self.first_number = float(self.current)
                    self.operation = value
                    self.current = ""
                else:
                    self.calculate()
                    self.operation = value
        elif value == "=":
            self.calculate()

    def calculate(self):
        if self.first_number is not None and self.current and self.operation:
            second_number = float(self.current)
            try:
                if self.operation == "+":
                    result = self.first_number + second_number
                elif self.operation == "-":
                    result = self.first_number - second_number
                elif self.operation == "*":
                    result = self.first_number * second_number
                elif self.operation == "/":
                    if second_number == 0:
                        messagebox.showerror("Error", "Cannot divide by zero!")
                        self.clear()
                        return
                    result = self.first_number / second_number
                
                self.display.delete(0, tk.END)
                # Format result to avoid too many decimal places
                result = round(result, 8)
                # Remove trailing zeros after decimal point
                result = "{:.8f}".format(result).rstrip("0").rstrip(".")
                self.display.insert(0, result)
                self.first_number = float(result)
                self.current = ""
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.clear()

    def clear(self):
        self.current = ""
        self.first_number = None
        self.operation = None
        self.display.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
