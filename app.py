import re
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np

class MatrixSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Matrices")
        self.size = 4  # Tamaño inicial de la matriz
        self.entries = []
        self.result_labels = []
        self.solve_button = None  # Botón de resolver
        self.error_label = None  # Etiqueta de error
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Solucionador de Matrices", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=6, pady=10)
        
        self.size_var = tk.IntVar(value=self.size)
        tk.Label(self.root, text="Tamaño:", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        self.size_menu = ttk.Combobox(self.root, textvariable=self.size_var, values=[2, 3, 4, 5, 6], state="readonly")
        self.size_menu.grid(row=1, column=1, pady=5, padx=5)
        self.size_menu.bind("<<ComboboxSelected>>", self.update_size)
        
        self.clear_button = tk.Button(self.root, text="Limpiar", font=("Arial", 12), command=self.clear_matrix)
        self.clear_button.grid(row=1, column=2, padx=10, pady=5)
        
        self.error_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.error_label.grid(row=2, column=0, columnspan=6)
        
        tk.Label(self.root, text="Ingrese los coeficientes de la matriz:", font=("Arial", 14)).grid(row=3, column=0, columnspan=6, pady=10)
        
        self.matrix_frame = tk.Frame(self.root)
        self.matrix_frame.grid(row=4, column=0, columnspan=6, pady=10)
        
        self.result_frame = tk.Frame(self.root)
        self.result_frame.grid(row=4, column=7, padx=10)
        
        self.draw_matrix()
    
    def validate_input(self, event):
        entry = event.widget
        value = entry.get()
        
        # Expresión regular que permite:
        #   - Opcionalmente un "-" al inicio (solo uno)
        #   - Seguido de dígitos (0-9)
        #   - Opcionalmente un "." y más dígitos (pero solo un punto)
        if not re.fullmatch(r'^-?\d*\.?\d*$', value):
            # Si no coincide, borrar el último carácter ingresado
            entry.delete(0, tk.END)
            entry.insert(0, value[:-1])
    
    def draw_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        self.entries = [[tk.Entry(self.matrix_frame, width=7, font=("Arial", 14), justify='center') for _ in range(self.size+1)] for _ in range(self.size)]
        
        for i in range(self.size):
            for j in range(self.size+1):
                self.entries[i][j].grid(row=i, column=j, padx=10, pady=10)
                self.entries[i][j].bind("<KeyRelease>", self.validate_input)
                if j == self.size:
                    self.entries[i][j].config(bg="lightgray")
                else:
                    self.entries[i][j].config(bg="white")
        
        if self.solve_button:
            self.solve_button.destroy()
        
        self.solve_button = tk.Button(self.root, text="Resolver", font=("Arial", 12), command=self.solve_matrix)
        self.solve_button.grid(row=5, column=0, columnspan=self.size+1, pady=10)
        
        self.result_labels = [tk.Label(self.result_frame, text=f"x{i+1} = ", font=("Arial", 12)) for i in range(self.size)]
        for i, label in enumerate(self.result_labels):
            label.grid(row=i, column=0, padx=10, pady=5)
    
    def update_size(self, event):
        self.size = self.size_var.get()
        self.error_label.config(text="")
        self.draw_matrix()
    
    def clear_matrix(self):
        for i in range(self.size):
            for j in range(self.size+1):
                self.entries[i][j].delete(0, tk.END)
        for label in self.result_labels:
            label.config(text="")
        self.error_label.config(text="")
    
    def solve_matrix(self):
        try:
            matrix = np.array([[float(self.entries[i][j].get()) for j in range(self.size)] for i in range(self.size)])
            results = np.array([float(self.entries[i][-1].get()) for i in range(self.size)])
            solution = np.linalg.solve(matrix, results)

            for i, val in enumerate(solution):
                self.result_labels[i].config(text=f"x{i+1} = {val:.2f}")
            self.error_label.config(text="")
        except ValueError:
            self.error_label.config(text="Error: Ingrese solo números válidos.")
        except np.linalg.LinAlgError:
            self.error_label.config(text="Error: La matriz no tiene solución única.")
        except Exception as e:
            self.error_label.config(text=f"Error inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixSolverApp(root)
    root.mainloop()
