# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 11:38:38 2025

@author: Jakub
"""

import tkinter as tk
from tkinter import ttk, messagebox

class AddOperationDialog(tk.Toplevel):
    def __init__(self, parent, db_manager, callback_on_add):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.callback_on_add = callback_on_add
        self.title("Dodaj nową operację sekwencjonowania")
        self.geometry("300x250")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Parametr 1:").pack(pady=5)
        self.param1_entry = ttk.Entry(self, width=30)
        self.param1_entry.pack(pady=2)

        ttk.Label(self, text="Parametr 2:").pack(pady=5)
        self.param2_entry = ttk.Entry(self, width=30)
        self.param2_entry.pack(pady=2)

        ttk.Label(self, text="Typ operacji:").pack(pady=5)
        self.op_type_var = tk.StringVar(value="pionowa")
        ttk.Radiobutton(self, text="Pionowa", variable=self.op_type_var, value="pionowa").pack(anchor="w", padx=70)
        ttk.Radiobutton(self, text="Pozioma", variable=self.op_type_var, value="pozioma").pack(anchor="w", padx=70)

        ttk.Button(self, text="Dodaj operację sekwencjonowania", command=self.add_operation, style='Accent.TButton').pack(pady=15)

    def add_operation(self):
        param1 = self.param1_entry.get().strip()
        param2 = self.param2_entry.get().strip()
        op_type = self.op_type_var.get()

        if not param1 or not param2:
            messagebox.showerror("Błąd", "Oba parametry muszą być wypełnione!")
            return

        if self.db_manager.insert_operation(op_type, param1, param2):
            messagebox.showinfo("Sukces", "Operacja sekwencjonowania dodana pomyślnie!")
            self.callback_on_add()
            self.destroy()
        else:
            messagebox.showerror("Błąd", "Nie udało się dodać operacji sekwencjonowania do bazy danych.")