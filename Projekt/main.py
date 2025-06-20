# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 11:39:42 2025

@author: Jakub
"""

import tkinter as tk
from tkinter import ttk, messagebox
import operation_drawer as od
from database_manager import DatabaseManager
from add_operation_dialog import AddOperationDialog
from convert_operation_dialog import ConvertOperationDialog
from change_separator_dialog import ChangeSeparatorDialog

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelowanie i analiza systemu informatycznego")
        self.geometry("950x800")
        
        s = ttk.Style()
        s.theme_use('clam')
        
        s.configure('TButton', font=('Segoe UI', 10), padding=6, relief='flat')
        s.map('TButton',
              background=[('active', '#e1e1e1'), ('!disabled', '#f0f0f0')],
              foreground=[('active', 'black'), ('!disabled', 'black')])

        s.configure('Accent.TButton', background='#2196F3', foreground='white')
        s.map('TButton',
              background=[('active', '#1976D2'), ('!disabled', '#2196F3')],
              foreground=[('active', 'white'), ('!disabled', 'white')])

        s.configure('Danger.TButton', background='#F44336', foreground='white')
        s.map('Danger.TButton',
              background=[('active', '#D32F2F'), ('!disabled', '#F44336')],
              foreground=[('active', 'white'), ('!disabled', 'white')])

        s.configure('Separator.TButton', background='#BBDEFB', foreground='black', font=('Segoe UI', 10), padding=6, relief='flat')
        s.map('Separator.TButton',
              background=[('active', '#90CAF9'), ('!disabled', '#BBDEFB')],
              foreground=[('active', 'black'), ('!disabled', 'black')])

        s.configure('TLabel', font=('Segoe UI', 10))
        s.configure('Header.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#333333')

        s.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#dddddd', foreground='#333333', padding=5)
        s.configure('Treeview', font=('Segoe UI', 10), rowheight=25, background='white', fieldbackground='white', foreground='black')
        s.map('Treeview', background=[('selected', '#BDE2F2')])

        self.db = DatabaseManager("localhost", "root", "root", "uniterm_db")

        self.current_separator = ";"

        self.create_widgets()
        self.current_operations_display = []

        self.load_operations_and_display()

    def create_widgets(self):
        button_frame = ttk.Frame(self, padding="10 10 10 0")
        button_frame.pack(side="top", fill="x", pady=(0, 10))

        self.add_button = ttk.Button(button_frame, text="Dodaj Operację Sekwencjonowania", command=self.open_add_operation_dialog, style='Accent.TButton')
        self.add_button.pack(side="left", padx=5)

        self.convert_button = ttk.Button(button_frame, text="Konwertuj Operację Sekwencjonowania", command=self.open_convert_operation_dialog, style='Accent.TButton')
        self.convert_button.pack(side="left", padx=5)

        self.delete_button = ttk.Button(button_frame, text="Usuń Wybraną Operację Sekwencjonowania", command=self.delete_selected_operation, style='Danger.TButton')
        self.delete_button.pack(side="left", padx=5)

        self.change_separator_button = ttk.Button(button_frame, text="Zmień Znak Separacji", command=self.open_change_separator_dialog, style='Separator.TButton')
        self.change_separator_button.pack(side="left", padx=5)


        ttk.Label(self, text="Zapisane operacje sekwencjonowania:").pack(anchor="w", padx=10, pady=(10, 5))
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(pady=(0, 5), padx=10, fill="x", expand=True)

        columns = ("ID", "Typ", "Parametr 1", "Parametr 2")
        self.operations_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8, style='Treeview')
        
        for col in columns:
            self.operations_tree.heading(col, text=col)
            self.operations_tree.column(col, width=100, anchor="center")
        
        self.operations_tree.column("ID", width=50)
        self.operations_tree.column("Typ", width=80)
        self.operations_tree.column("Parametr 1", width=150)
        self.operations_tree.column("Parametr 2", width=150)
        self.operations_tree.column("#0", width=0, stretch=tk.NO)

        scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=self.operations_tree.yview)
        scrollbar_tree.pack(side="right", fill="y")
        
        self.operations_tree.pack(side="left", fill="both", expand=True)

        self.operations_tree.configure(yscrollcommand=scrollbar_tree.set)


        ttk.Label(self, text="Graficzna reprezentacja operacji sekwencjonowania:").pack(anchor="w", padx=10, pady=(10, 5))
        
        canvas_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        canvas_frame.pack(pady=(0, 10), padx=10, fill="both", expand=True)

        self.canvas_y_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", style='TScrollbar')
        self.canvas_y_scrollbar.pack(side="right", fill="y")

        self.canvas_x_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", style='TScrollbar')
        self.canvas_x_scrollbar.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(canvas_frame, bg="#EFEFEF", 
                                yscrollcommand=self.canvas_y_scrollbar.set,
                                xscrollcommand=self.canvas_x_scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas_y_scrollbar.config(command=self.canvas.yview)
        self.canvas_x_scrollbar.config(command=self.canvas.xview)


    def open_add_operation_dialog(self):
        AddOperationDialog(self, self.db, self.load_operations_and_display)

    def open_convert_operation_dialog(self):
        ConvertOperationDialog(self, self.db, self.display_and_save_converted_operation)

    def open_change_separator_dialog(self):
        ChangeSeparatorDialog(self, self.current_separator, self.update_separator_and_redraw)

    def update_separator_and_redraw(self, new_separator):
        self.current_separator = new_separator
        self.load_operations_and_display()


    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, 0, 0))
        self.current_operations_display = []

    def load_operations_and_display(self):
        self.clear_canvas()
        
        for item in self.operations_tree.get_children():
            self.operations_tree.delete(item)

        operations = self.db.get_all_operations()
        
        if not operations:
            self.operations_tree.insert("", "end", values=("Brak operacji", "", "", ""), iid="no_ops_msg")
            self.canvas.config(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))
        else:
            current_y_offset = 10
            max_width_needed = 0
            
            for op in operations:
                if op['converted_structure']:
                    display_type = "Konwersja"
                    p1_text = op['param1']
                    p2_text = op['param2']
                    self.operations_tree.insert("", "end", values=(op['id'], display_type, p1_text, p2_text), iid=op['id'])
                    
                    width, height = od.draw_operation_smartly(self.canvas, op['converted_structure'], 10, current_y_offset, self.current_separator)
                else:
                    self.operations_tree.insert("", "end", values=(op['id'], op['type'], op['param1'], op['param2']), iid=op['id'])
                    width, height = od.draw_operation_smartly(self.canvas, op, 10, current_y_offset, self.current_separator)
                
                max_width_needed = max(max_width_needed, 10 + width)
                current_y_offset += height + 20

            scroll_width = max(max_width_needed + 50, self.canvas.winfo_width())
            scroll_height = max(current_y_offset + 50, self.canvas.winfo_height())
            
            self.canvas.config(scrollregion=(0, 0, scroll_width, scroll_height))


    def display_and_save_converted_operation(self, original_param1, original_param2, converted_op_data):
        if self.db.insert_operation('pionowa', original_param1, original_param2, converted_structure=converted_op_data):
            messagebox.showinfo("Sukces", "Skonwertowana operacja sekwencjonowania została zapisana do bazy danych.")
        else:
            messagebox.showerror("Błąd", "Nie udało się zapisać skonwertowanej operacji sekwencjonowania do bazy danych.")
        
        self.load_operations_and_display()


    def delete_selected_operation(self):
        selected_item = self.operations_tree.selection()
        if not selected_item:
            messagebox.showerror("Błąd", "Wybierz operację sekwencjonowania do usunięcia z listy.")
            return

        op_id_to_delete = selected_item[0]
        
        if op_id_to_delete == "no_ops_msg":
             messagebox.showinfo("Informacja", "Nie możesz usunąć tego komunikatu.")
             return

        confirm = messagebox.askyesno(
            "Potwierdź usunięcie",
            f"Czy na pewno chcesz usunąć operację sekwencjonowania o ID: {op_id_to_delete}?"
        )
        
        if confirm:
            try:
                op_id_to_delete = int(op_id_to_delete)
                if self.db.delete_operation(op_id_to_delete):
                    messagebox.showinfo("Sukces", f"Operacja sekwencjonowania o ID {op_id_to_delete} została usunięta.")
                    self.load_operations_and_display()
                else:
                    messagebox.showerror("Błąd", f"Nie udało się usunąć operacji sekwencjonowania o ID {op_id_to_delete}.")
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowe ID operacji sekwencjonowania do usunięcia.")


    def on_closing(self):
        if self.db.connection:
            self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()