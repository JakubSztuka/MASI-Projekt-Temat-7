# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 11:37:56 2025

@author: Jakub
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ChangeSeparatorDialog(tk.Toplevel):
    def __init__(self, parent, current_separator, callback_on_apply):
        super().__init__(parent)
        self.parent = parent
        self.current_separator = current_separator
        self.callback_on_apply = callback_on_apply
        self.title("Zmień znak separacji")
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text=f"Aktualny znak: '{self.current_separator}'").pack(pady=5)
        ttk.Label(self, text="Wprowadź nowy znak separacji:").pack(pady=5)
        self.separator_entry = ttk.Entry(self, width=10)
        self.separator_entry.pack(pady=2)
        self.separator_entry.insert(0, self.current_separator)

        ttk.Button(self, text="Zastosuj", command=self.apply_separator, style='Separator.TButton').pack(pady=15)

    def apply_separator(self):
        new_sep = self.separator_entry.get().strip()
        if not new_sep:
            messagebox.showerror("Błąd", "Znak separacji nie może być pusty!")
            return
        if len(new_sep) > 1:
            messagebox.showerror("Błąd", "Znak separacji musi być pojedynczym znakiem!")
            return

        self.callback_on_apply(new_sep)
        self.destroy()