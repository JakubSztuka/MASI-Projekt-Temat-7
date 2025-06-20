# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 11:39:06 2025

@author: Jakub
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ConvertOperationDialog(tk.Toplevel):
    def __init__(self, parent, db_manager, callback_on_convert_and_save):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.callback_on_convert_and_save = callback_on_convert_and_save
        self.title("Konwertuj operację sekwencjonowania")
        self.geometry("450x350")
        self.resizable(False, False)
        self.grab_set()

        self.vertical_ops = []
        self.horizontal_ops = []
        
        self.create_widgets()
        self.load_operations()

    def create_widgets(self):
        ttk.Label(self, text="1. Wybierz operację sekwencjonowania PIONOWĄ do konwersji:").pack(pady=5)
        self.vertical_combo = ttk.Combobox(self, state="readonly", width=40)
        self.vertical_combo.pack(pady=2)
        self.vertical_combo.bind("<<ComboboxSelected>>", self.on_vertical_selected)

        ttk.Label(self, text="2. Który parametr zamienić w operacji sekwencjonowania pionowej?").pack(pady=5)
        self.param_to_replace_var = tk.StringVar(value="param1")
        self.radio_frame = ttk.Frame(self)
        self.radio_frame.pack(pady=2)
        self.param1_radio = ttk.Radiobutton(self.radio_frame, text="Parametr 1", variable=self.param_to_replace_var, value="param1").pack(side="left", padx=10)
        self.param2_radio = ttk.Radiobutton(self.radio_frame, text="Parametr 2", variable=self.param_to_replace_var, value="param2").pack(side="left", padx=10)
        
        ttk.Label(self, text="3. Wybierz operację sekwencjonowania POZIOMĄ do wstawienia:").pack(pady=5)
        self.horizontal_combo = ttk.Combobox(self, state="readonly", width=40)
        self.horizontal_combo.pack(pady=2)

        ttk.Button(self, text="Wykonaj Konwersję", command=self.perform_conversion, style='Accent.TButton').pack(pady=20)

    def load_operations(self):
        self.vertical_ops = self.db_manager.get_operations_by_type('pionowa') 
        self.horizontal_ops = self.db_manager.get_operations_by_type('pozioma')

        vertical_display_values = [f"ID: {op['id']} ({op['param1']} ; {op['param2']})" for op in self.vertical_ops]
        self.vertical_combo['values'] = vertical_display_values
        if vertical_display_values:
            self.vertical_combo.set(vertical_display_values[0])
            self.on_vertical_selected(None)

        horizontal_display_values = [f"ID: {op['id']} ({op['param1']} ; {op['param2']})" for op in self.horizontal_ops]
        self.horizontal_combo['values'] = horizontal_display_values
        if horizontal_display_values:
            self.horizontal_combo.set(horizontal_display_values[0])

    def on_vertical_selected(self, event):
        pass

    def perform_conversion(self):
        selected_vertical_op_str = self.vertical_combo.get()
        selected_horizontal_op_str = self.horizontal_combo.get()
        param_to_replace = self.param_to_replace_var.get()

        if not selected_vertical_op_str or not selected_horizontal_op_str:
            messagebox.showerror("Błąd", "Musisz wybrać zarówno operację sekwencjonowania pionową, jak i poziomą.")
            return

        try:
            vertical_op_id = int(selected_vertical_op_str.split(' ')[1])
            horizontal_op_id = int(selected_horizontal_op_str.split(' ')[1])
        except (ValueError, IndexError):
            messagebox.showerror("Błąd", "Niepoprawny format wybranej operacji.")
            return

        vertical_op = next((op for op in self.vertical_ops if op['id'] == vertical_op_id), None)
        horizontal_op = next((op for op in self.horizontal_ops if op['id'] == horizontal_op_id), None)

        if not vertical_op or not horizontal_op:
            messagebox.showerror("Błąd", "Nie znaleziono wybranej operacji w bazie danych.")
            return
        
        converted_op_data = {
            'type': 'pionowa',
            'param1': vertical_op['param1'],
            'param2': vertical_op['param2']
        }

        horizontal_nest_data = {
            'type': 'pozioma',
            'param1': horizontal_op['param1'],
            'param2': horizontal_op['param2']
        }

        if param_to_replace == 'param1':
            converted_op_data['param1'] = horizontal_nest_data
        else:
            converted_op_data['param2'] = horizontal_nest_data
        
        self.callback_on_convert_and_save(vertical_op['param1'], vertical_op['param2'], converted_op_data)
        self.destroy()