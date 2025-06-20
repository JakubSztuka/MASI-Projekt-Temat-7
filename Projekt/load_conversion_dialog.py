# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 12:51:24 2025

@author: Jakub
"""

import tkinter as tk
from tkinter import ttk, messagebox

class LoadConversionDialog(tk.Toplevel):
    def __init__(self, parent, db_manager, callback_on_load):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.callback_on_load = callback_on_load
        self.title("Wczytaj Konwersję")
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()

        self.converted_ops = []
        
        self.create_widgets()
        self.load_converted_operations()

    def create_widgets(self):
        ttk.Label(self, text="Wybierz skonwertowaną operację:").pack(pady=10)
        
        self.conversion_combo = ttk.Combobox(self, state="readonly", width=45)
        self.conversion_combo.pack(pady=5)

        ttk.Button(self, text="Wczytaj Wybraną", command=self.load_selected_conversion).pack(pady=20)

    def load_converted_operations(self):
        self.converted_ops = self.db_manager.get_converted_operations()
        
        if not self.converted_ops:
            self.conversion_combo['values'] = ["Brak zapisanych konwersji"]
            self.conversion_combo.set("Brak zapisanych konwersji")
            self.conversion_combo.config(state="disabled")
        else:
            display_values = []
            for op in self.converted_ops:
                p1_display = op['converted_structure']['param1']
                p2_display = op['converted_structure']['param2']

                if isinstance(p1_display, dict):
                    p1_display = f"({p1_display['param1']} ; {p1_display['param2']})"
                if isinstance(p2_display, dict):
                    p2_display = f"({p2_display['param1']} ; {p2_display['param2']})"
                
                display_values.append(f"ID: {op['id']} ({p1_display} ; {p2_display})")
            
            self.conversion_combo['values'] = display_values
            self.conversion_combo.set(display_values[0])
            self.conversion_combo.config(state="readonly")


    def load_selected_conversion(self):
        selected_op_str = self.conversion_combo.get()
        
        if selected_op_str == "Brak zapisanych konwersji":
            messagebox.showinfo("Informacja", "Nie ma żadnych konwersji do wczytania.")
            return

        try:
            selected_id = int(selected_op_str.split(' ')[1])
        except (ValueError, IndexError):
            messagebox.showerror("Błąd", "Niepoprawny format wybranej konwersji.")
            return

        selected_op = next((op for op in self.converted_ops if op['id'] == selected_id), None)

        if selected_op and selected_op['converted_structure']:
            self.callback_on_load(selected_op['converted_structure'])
            self.destroy()
        else:
            messagebox.showerror("Błąd", "Nie udało się wczytać wybranej konwersji.")