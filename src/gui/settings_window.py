import os
import tkinter as tk
from tkinter import messagebox, ttk
from ..config import AppSettings
from ..utils.validators import validate_number, validate_decimal, validate_name
from ..core import gui_settings_logger

# Fenster für die Einstellungen
class SettingsWindow:
    def __init__(self, parent, db_manager, main_window):
        gui_settings_logger.info("Initialisiere Einstellungsfenster")
        self.db_manager = db_manager
        self.main_window = main_window
        self.parent = parent
        
        # Initialize window
        self._create_window()
        
        # Setup components
        self._setup_window_properties()
        self._setup_ui_components()
        
        # Initialize state
        self._initialize_state()
    
    def _create_window(self):
        """Create the toplevel window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title('Einstellungen')
        self.window.geometry(AppSettings.SETTINGS_WINDOW_SIZE)
        self.window.resizable(False, False)
    
    def _setup_window_properties(self):
        """Setup window styling and positioning"""
        self.setup_style()
        self.load_icon()
        self.center_window(self.parent)
    
    def _setup_ui_components(self):
        """Setup all UI components"""
        self.main_frame = ttk.Frame(self.window, padding="15 15 15 15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_components()
    
    def _initialize_state(self):
        """Initialize component state"""
        self.selected_weapon_id = None
        self.selected_ammo_id = None
        self.selected_distance_id = None

    def setup_style(self):
        self.style = ttk.Style()
        
        bg_color = AppSettings.BACKGROUND_COLOR
        
        self.window.configure(bg=bg_color)
    
    def center_window(self, parent):
        self.window.update_idletasks()
        parent.update_idletasks()
        
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        x = parent_x + (parent_width - window_width) // 2
        y = parent_y + (parent_height - window_height) // 2
        
        self.window.geometry(f'+{x}+{y}')
    
    def load_icon(self):
        try:
            icons_dir = AppSettings.get_icons_dir()
            icon_path = os.path.join(icons_dir, 'settings_icon.ico')
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except Exception as e:
            pass
    
    def setup_components(self):
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        weapon_frame = ttk.Frame(notebook, padding="10 10 10 10")
        ammo_frame = ttk.Frame(notebook, padding="10 10 10 10")
        distance_frame = ttk.Frame(notebook, padding="10 10 10 10")
        results_frame = ttk.Frame(notebook, padding="10 10 10 10")
        
        notebook.add(weapon_frame, text='Waffen')
        notebook.add(ammo_frame, text='Munition')
        notebook.add(distance_frame, text='Entfernungen')
        notebook.add(results_frame, text='Ergebnisse')
        
        self.setup_weapons_tab(weapon_frame)
        self.setup_ammunition_tab(ammo_frame)
        self.setup_distances_tab(distance_frame)
        self.setup_results_tab(results_frame)
        
        close_button = ttk.Button(self.main_frame, text="Schließen", command=self.close, style='Big.TButton')
        close_button.pack(pady=10)
    
    def setup_weapons_tab(self, parent):
        table_frame = ttk.LabelFrame(parent, text="Verfügbare Waffen")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Waffe', 'Kaliber')
        self.weapon_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.weapon_tree.yview)
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.weapon_tree.xview)
        x_scrollbar.pack(side='bottom', fill='x')
        
        self.weapon_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        for col in columns:
            self.weapon_tree.heading(col, text=col)
            width = 50 if col == 'ID' else 200
            self.weapon_tree.column(col, width=width, minwidth=width)
        
        self.weapon_tree.pack(fill='both', expand=True)
        
        self.weapon_tree.bind('<<TreeviewSelect>>', self.on_weapon_select)
        
        self.weapon_context_menu = tk.Menu(self.weapon_tree, tearoff=0)
        self.weapon_context_menu.add_command(label="Löschen", command=self.remove_weapon)
        self.weapon_tree.bind("<Button-3>", self.show_weapon_context_menu)
        
        form_frame = ttk.LabelFrame(parent, text="Neue Waffe hinzufügen")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Waffenname:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.weapon_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.weapon_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Kaliber:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.caliber_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.caliber_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        self.weapon_caliber_unit_var = tk.StringVar(value="mm")
        unit_frame = ttk.Frame(form_frame)
        unit_frame.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        
        ttk.Radiobutton(unit_frame, text="mm", variable=self.weapon_caliber_unit_var, value="mm").pack(side='left')
        ttk.Radiobutton(unit_frame, text="in", variable=self.weapon_caliber_unit_var, value="in").pack(side='left')
        
        ttk.Button(form_frame, text="Waffe hinzufügen", command=self.add_weapon).grid(row=2, column=0, columnspan=3, padx=5, pady=10)
        
        self.load_weapons_table()

    def setup_ammunition_tab(self, parent):
        table_frame = ttk.LabelFrame(parent, text="Verfügbare Munition")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Munition', 'Kaliber')
        self.ammo_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.ammo_tree.yview)
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.ammo_tree.xview)
        x_scrollbar.pack(side='bottom', fill='x')
        
        self.ammo_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        for col in columns:
            self.ammo_tree.heading(col, text=col)
            width = 50 if col == 'ID' else 200
            self.ammo_tree.column(col, width=width, minwidth=width)
        
        self.ammo_tree.pack(fill='both', expand=True)
        
        self.ammo_tree.bind('<<TreeviewSelect>>', self.on_ammo_select)
        
        self.ammo_context_menu = tk.Menu(self.ammo_tree, tearoff=0)
        self.ammo_context_menu.add_command(label="Löschen", command=self.remove_ammo)
        self.ammo_tree.bind("<Button-3>", self.show_ammo_context_menu)
        
        form_frame = ttk.LabelFrame(parent, text="Neue Munition hinzufügen")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Munitionsname:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ammo_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.ammo_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Kaliber:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.ammo_caliber_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.ammo_caliber_var, width=10).grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        self.ammo_caliber_unit_var = tk.StringVar(value="mm")
        unit_frame = ttk.Frame(form_frame)
        unit_frame.grid(row=1, column=2, padx=5, pady=5, sticky='w')
        
        ttk.Radiobutton(unit_frame, text="mm", variable=self.ammo_caliber_unit_var, value="mm").pack(side='left')
        ttk.Radiobutton(unit_frame, text="in", variable=self.ammo_caliber_unit_var, value="in").pack(side='left')
        
        ttk.Button(form_frame, text="Munition hinzufügen", command=self.add_ammo).grid(row=2, column=0, columnspan=3, padx=5, pady=10)
        
        self.load_ammo_table()

    def setup_distances_tab(self, parent):
        table_frame = ttk.LabelFrame(parent, text="Verfügbare Entfernungen")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Entfernung', 'Einheit')
        self.distance_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.distance_tree.yview)
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.distance_tree.xview)
        x_scrollbar.pack(side='bottom', fill='x')
        
        self.distance_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        for col in columns:
            self.distance_tree.heading(col, text=col)
            width = 50 if col == 'ID' else 200
            self.distance_tree.column(col, width=width, minwidth=width)
        
        self.distance_tree.pack(fill='both', expand=True)
        
        self.distance_tree.bind('<<TreeviewSelect>>', self.on_distance_select)
        
        self.distance_context_menu = tk.Menu(self.distance_tree, tearoff=0)
        self.distance_context_menu.add_command(label="Löschen", command=self.remove_distance)
        self.distance_tree.bind("<Button-3>", self.show_distance_context_menu)
        
        form_frame = ttk.LabelFrame(parent, text="Neue Entfernung hinzufügen")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Entfernung:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.distance_value_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.distance_value_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        self.distance_unit_var = tk.StringVar(value="m")
        unit_frame = ttk.Frame(form_frame)
        unit_frame.grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        ttk.Radiobutton(unit_frame, text="m", variable=self.distance_unit_var, value="m").pack(side='left')
        ttk.Radiobutton(unit_frame, text="yd", variable=self.distance_unit_var, value="yd").pack(side='left')
        
        ttk.Button(form_frame, text="Entfernung hinzufügen", command=self.add_distance).grid(row=1, column=0, columnspan=3, padx=5, pady=10)
        
        self.load_distances_table()

    def setup_results_tab(self, parent):
        table_frame = ttk.LabelFrame(parent, text="Verfügbare Ergebnisse")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        filter_frame = ttk.Frame(table_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Nach Waffe filtern:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.results_weapon_filter_var = tk.StringVar()
        weapons = self.db_manager.get_weapons()
        weapon_names = ["Alle"] + [weapon[1] for weapon in weapons]
        self.results_weapon_filter_var.set("Alle")
        ttk.OptionMenu(filter_frame, self.results_weapon_filter_var, *weapon_names).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Nach Munition filtern:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.results_ammo_filter_var = tk.StringVar()
        ammunition = self.db_manager.get_ammunition()
        ammo_names = ["Alle"] + [ammo[1] for ammo in ammunition]
        self.results_ammo_filter_var.set("Alle")
        ttk.OptionMenu(filter_frame, self.results_ammo_filter_var, *ammo_names).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(filter_frame, text="Filter anwenden", command=self.apply_results_filter).grid(row=0, column=4, padx=5, pady=5)
        
        columns = ('ID', 'Waffe', 'Munition', 'Entfernung', 'Ergebnis')
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        y_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.results_tree.yview)
        y_scrollbar.pack(side='right', fill='y')
        x_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.results_tree.xview)
        x_scrollbar.pack(side='bottom', fill='x')
        
        self.results_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            width = 50 if col == 'ID' else 150
            self.results_tree.column(col, width=width, minwidth=width)
        
        self.results_tree.pack(fill='both', expand=True)
        
        self.results_tree.bind('<<TreeviewSelect>>', self.on_results_tree_select)
        
        self.results_context_menu = tk.Menu(self.results_tree, tearoff=0)
        self.results_context_menu.add_command(label="Löschen", command=self.remove_result_from_tree)
        self.results_context_menu.add_command(label="Bearbeiten", command=self.edit_result_from_tree)
        self.results_tree.bind("<Button-3>", self.show_results_context_menu)
        
        edit_frame = ttk.LabelFrame(parent, text="Ergebnis bearbeiten/hinzufügen")
        edit_frame.pack(fill='x', padx=10, pady=10)
        
        edit_grid = ttk.Frame(edit_frame)
        edit_grid.pack(fill='x', padx=5, pady=5)
        
        for i in range(4):
            edit_grid.columnconfigure(i, weight=1)
                
        weapons = self.db_manager.get_weapons()
        weapon_names = ["-- Waffe auswählen --"] + [weapon[1] for weapon in weapons] if weapons else ['Keine Waffen']
        
        self.results_weapon_var = tk.StringVar()
        self.results_weapon_var.set(weapon_names[0])
        
        ttk.Label(edit_grid, text='Waffe:').grid(row=0, column=0, padx=5, pady=5, sticky='e')
        
        self.results_weapon_menu = ttk.OptionMenu(edit_grid, self.results_weapon_var, *weapon_names)
        self.results_weapon_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        self.results_weapon_var.trace('w', self.on_results_weapon_var_change)
        
        ammunition = self.db_manager.get_ammunition()
        ammo_names = ["-- Munition auswählen --"] + [ammo[1] for ammo in ammunition] if ammunition else ['Keine Munition']
        
        self.results_ammo_var = tk.StringVar()
        self.results_ammo_var.set(ammo_names[0])
        
        ttk.Label(edit_grid, text='Munition:').grid(row=0, column=2, padx=5, pady=5, sticky='e')
        
        self.results_ammo_menu = ttk.OptionMenu(edit_grid, self.results_ammo_var, *ammo_names)
        self.results_ammo_menu.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        
        distances = self.db_manager.get_distances()
        distance_names = ["-- Entfernung auswählen --"] + [f"{dist[1]}{dist[2]}" for dist in distances] if distances else ['Keine Entfernungen']
        
        self.results_distance_var = tk.StringVar()
        self.results_distance_var.set(distance_names[0])
        
        ttk.Label(edit_grid, text='Entfernung:').grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        self.results_distance_menu = ttk.OptionMenu(edit_grid, self.results_distance_var, *distance_names)
        self.results_distance_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        
        self.results_value_var = tk.StringVar()
        ttk.Label(edit_grid, text='Klickposition:').grid(row=1, column=2, padx=5, pady=5, sticky='e')
        
        ttk.Entry(edit_grid, textvariable=self.results_value_var, width=15).grid(row=1, column=3, padx=5, pady=5, sticky='w')
        
        button_frame = ttk.Frame(edit_grid)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        self.add_result_button = ttk.Button(button_frame, text='Ergebnis hinzufügen', command=self.add_result_from_tab, width=15)
        self.add_result_button.pack(side='left', padx=5, pady=5)
        
        self.update_result_button = ttk.Button(button_frame, text='Ergebnis aktualisieren', command=self.update_result_from_tab, width=15, state='disabled')
        self.update_result_button.pack(side='left', padx=5, pady=5)
        
        self.cancel_edit_button = ttk.Button(button_frame, text='Abbrechen', command=self.cancel_result_edit, width=10, state='disabled')
        self.cancel_edit_button.pack(side='left', padx=5, pady=5)
        
        self.selected_result_id = None
        self.load_results_table()

    def on_results_weapon_var_change(self, *args):
        selected_weapon = self.results_weapon_var.get()
        if selected_weapon in ['Keine Waffen', '-- Waffe auswählen --']:
            # Reset ammunition to default when no weapon is selected
            ammunition = self.db_manager.get_ammunition()
            ammo_names = ["-- Munition auswählen --"] + [ammo[1] for ammo in ammunition] if ammunition else ['Keine Munition']
            
            self.results_ammo_menu['menu'].delete(0, 'end')
            
            for name in ammo_names:
                self.results_ammo_menu['menu'].add_command(
                    label=name,
                    command=lambda n=name: self.results_ammo_var.set(n)
                )
            
            self.results_ammo_var.set(ammo_names[0])
            return
        
        caliber = self.db_manager.get_weapon_caliber(selected_weapon)
        if not caliber:
            return
            
        matching_ammo = self.db_manager.get_ammunition_by_caliber(caliber)
        matching_ammo_names = ["-- Munition auswählen --"] + [ammo[1] for ammo in matching_ammo] if matching_ammo else ['Keine passende Munition']
        
        self.results_ammo_menu['menu'].delete(0, 'end')
        
        for name in matching_ammo_names:
            self.results_ammo_menu['menu'].add_command(
                label=name,
                command=lambda n=name: self.results_ammo_var.set(n)
            )
        
        self.results_ammo_var.set(matching_ammo_names[0])

    def load_results_table(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        results = self.db_manager.get_results()
        
        for result in results:
            # Verwende direkt Tupel-Format
            self.results_tree.insert('', 'end', values=result)

    def apply_results_filter(self):
        weapon_filter = self.results_weapon_filter_var.get()
        ammo_filter = self.results_ammo_filter_var.get()
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        weapon_id = None
        if weapon_filter != "Alle":
            weapon_id = self.db_manager.get_weapon_id(weapon_filter)
        
        ammo_id = None
        if ammo_filter != "Alle":
            ammo_id = self.db_manager.get_ammunition_id(ammo_filter)
        
        results = self.db_manager.get_results_by_criteria(weapon_id, ammo_id)
        
        for result in results:
            result_id, weapon, ammo, distance, unit, result_value = result[:6]
            distance_display = f"{distance}{unit}"
            self.results_tree.insert('', 'end', values=(result_id, weapon, ammo, distance_display, result_value))

    def on_results_tree_select(self, event):
        selected_items = self.results_tree.selection()
        if selected_items:
            item = selected_items[0]
            item_data = self.results_tree.item(item, 'values')
            if item_data:
                self.selected_result_id = item_data[0]
                
                self.results_weapon_var.set(item_data[1])
                self.on_results_weapon_var_change()
                self.results_ammo_var.set(item_data[2])
                self.results_distance_var.set(item_data[3])
                self.results_value_var.set(item_data[4])
                
                self.update_result_button.config(state='normal')
                self.cancel_edit_button.config(state='normal')
                self.add_result_button.config(state='disabled')

    def show_results_context_menu(self, event):
        item = self.results_tree.identify_row(event.y)
        if item:
            self.results_tree.selection_set(item)
            self.on_results_tree_select(None)
            self.results_context_menu.post(event.x_root, event.y_root)

    def add_result_from_tab(self):
        try:
            weapon_name = self.results_weapon_var.get()
            ammo_name = self.results_ammo_var.get()
            distance_display = self.results_distance_var.get()
            result_value = self.results_value_var.get()
            
            if not result_value:
                messagebox.showerror("Fehler", "Ergebniswert muss angegeben werden")
                return
                
            if not validate_number(result_value):
                messagebox.showerror("Fehler", "Ergebniswert muss eine gültige ganze Zahl sein")
                return
                
            if (weapon_name in ['Keine Waffen', '-- Waffe auswählen --'] or 
                ammo_name in ['Keine Munition', 'Keine passende Munition', '-- Munition auswählen --'] or 
                distance_display in ['Keine Entfernungen', '-- Entfernung auswählen --']):
                messagebox.showerror("Fehler", "Bitte wählen Sie gültige Waffen-, Munitions- und Entfernungswerte aus")
                return
            
            weapon_caliber = self.db_manager.get_weapon_caliber(weapon_name)
            
            with self.db_manager.db as db:
                db.db_cursor.execute('SELECT caliber FROM ammunition WHERE ammunition = ?', (ammo_name,))
                ammo_caliber_record = db.db_cursor.fetchone()
                
            if not ammo_caliber_record:
                messagebox.showerror("Fehler", f"Kaliber für Munition nicht gefunden: {ammo_name}")
                return
                
            ammo_caliber = ammo_caliber_record[0]
            
            if weapon_caliber != ammo_caliber:
                messagebox.showerror("Fehler", f"Kaliber stimmt nicht überein: Waffenkaliber {weapon_caliber} stimmt nicht mit Munitionskaliber {ammo_caliber} überein")
                return
                
            self.db_manager.add_result(weapon_name, ammo_name, distance_display, result_value)
            messagebox.showinfo("Erfolg", f"Ergebnis hinzugefügt für {weapon_name} mit {ammo_name} bei {distance_display}")
            
            self.load_results_table()
            self.results_value_var.set("")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen des Ergebnisses: {e}")

    def update_result_from_tab(self):
        if not self.selected_result_id:
            messagebox.showerror("Fehler", "Kein Ergebnis ausgewählt")
            return
        
        new_value = self.results_value_var.get()
        
        if not new_value:
            messagebox.showerror("Fehler", "Neuer Wert muss angegeben werden")
            return
            
        if not validate_number(new_value):
            messagebox.showerror("Fehler", "Ergebniswert muss eine gültige ganze Zahl sein")
            return
        
        try:
            self.db_manager.update_result(self.selected_result_id, new_value)
            messagebox.showinfo("Erfolg", "Ergebnis erfolgreich aktualisiert")
            self.load_results_table()
            self.cancel_result_edit()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren des Ergebnisses: {e}")

    def remove_result_from_tree(self):
        if not self.selected_result_id:
            messagebox.showerror("Fehler", "Kein Ergebnis ausgewählt")
            return
        
        if messagebox.askyesno("Löschen bestätigen", "Sind Sie sicher, dass Sie dieses Ergebnis löschen möchten?"):
            try:
                self.db_manager.remove_result(self.selected_result_id)
                messagebox.showinfo("Erfolg", "Ergebnis erfolgreich gelöscht")
                self.load_results_table()
                self.cancel_result_edit()
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Löschen des Ergebnisses: {e}")

    def edit_result_from_tree(self):
        pass

    def cancel_result_edit(self):
        self.selected_result_id = None
        self.results_value_var.set("")
        
        # Reset to default selections
        weapons = self.db_manager.get_weapons()
        weapon_names = ["-- Waffe auswählen --"] + [weapon[1] for weapon in weapons] if weapons else ['Keine Waffen']
        self.results_weapon_var.set(weapon_names[0])
        
        ammunition = self.db_manager.get_ammunition()
        ammo_names = ["-- Munition auswählen --"] + [ammo[1] for ammo in ammunition] if ammunition else ['Keine Munition']
        self.results_ammo_var.set(ammo_names[0])
        
        distances = self.db_manager.get_distances()
        distance_names = ["-- Entfernung auswählen --"] + [f"{dist[1]}{dist[2]}" for dist in distances] if distances else ['Keine Entfernungen']
        self.results_distance_var.set(distance_names[0])
            
        self.update_result_button.config(state='disabled')
        self.cancel_edit_button.config(state='disabled')
        self.add_result_button.config(state='normal')

    def load_weapons_table(self):
        for item in self.weapon_tree.get_children():
            self.weapon_tree.delete(item)
        
        weapons = self.db_manager.get_weapons()
        
        for weapon in weapons:
            # Verwende direkt Tupel-Format
            self.weapon_tree.insert('', 'end', values=weapon)

    def add_weapon(self):
        try:
            weapon_name = self.weapon_name_var.get().strip()
            caliber = self.caliber_var.get().strip()
            unit = self.weapon_caliber_unit_var.get()
            
            gui_settings_logger.info(f"Versuche Waffe hinzuzufügen: {weapon_name} ({caliber} {unit})")
            
            if not weapon_name:
                messagebox.showerror("Fehler", "Waffenname ist erforderlich")
                return
                
            if not caliber:
                messagebox.showerror("Fehler", "Kaliber ist erforderlich")
                return
                
            if not validate_name(weapon_name):
                messagebox.showerror("Fehler", "Waffenname enthält ungültige Zeichen")
                return
                
            if not validate_decimal(caliber):
                messagebox.showerror("Fehler", "Kaliber muss eine gültige Zahl sein")
                return
                
            caliber_with_unit = f"{caliber} {unit}"
            
            self.db_manager.add_weapon(weapon_name, caliber_with_unit)
            messagebox.showinfo("Erfolg", f"Waffe hinzugefügt: {weapon_name}")
            
            gui_settings_logger.info(f"Waffe erfolgreich hinzugefügt: {weapon_name}")
            
            self.weapon_name_var.set("")
            self.caliber_var.set("")
            
            self.load_weapons_table()
            
            self.main_window.refresh_components()
            
        except Exception as e:
            gui_settings_logger.error(f"Fehler beim Hinzufügen der Waffe '{weapon_name}': {e}")
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Waffe: {str(e)}")

    def load_ammo_table(self):
        for item in self.ammo_tree.get_children():
            self.ammo_tree.delete(item)
        
        ammunition = self.db_manager.get_ammunition()
        
        for ammo in ammunition:
            # Verwende direkt Tupel-Format
            self.ammo_tree.insert('', 'end', values=ammo)

    def load_distances_table(self):
        for item in self.distance_tree.get_children():
            self.distance_tree.delete(item)
        
        distances = self.db_manager.get_distances()
        
        for distance in distances:
            # Verwende direkt Tupel-Format
            self.distance_tree.insert('', 'end', values=distance)

    def add_distance(self):
        try:
            distance_value = self.distance_value_var.get().strip()
            unit = self.distance_unit_var.get()
            
            if not distance_value:
                messagebox.showerror("Fehler", "Entfernung ist erforderlich")
                return
                
            if not validate_decimal(distance_value):
                messagebox.showerror("Fehler", "Entfernung muss eine gültige Zahl sein")
                return
            
            self.db_manager.add_distance(distance_value, unit)
            messagebox.showinfo("Erfolg", f"Entfernung hinzugefügt: {distance_value} {unit}")
            
            self.distance_value_var.set("")
            
            self.load_distances_table()
            
            self.main_window.refresh_components()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Entfernung: {str(e)}")

    def load_results_table(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        results = self.db_manager.get_results()
        
        for result in results:
            # Verwende direkt Tupel-Format
            self.results_tree.insert('', 'end', values=result)

    def add_result(self):
        try:
            result_value = self.result_value_var.get().strip()
            description = self.result_description_var.get().strip()
            
            if not result_value:
                messagebox.showerror("Fehler", "Ergebnis ist erforderlich")
                return
                
            if not description:
                messagebox.showerror("Fehler", "Beschreibung ist erforderlich")
                return
            
            if not validate_decimal(result_value):
                messagebox.showerror("Fehler", "Ergebnis muss eine gültige Zahl sein")
                return
            
            self.db_manager.add_result(result_value, description)
            messagebox.showinfo("Erfolg", f"Ergebnis hinzugefügt: {result_value} ({description})")
            
            self.result_value_var.set("")
            self.result_description_var.set("")
            
            self.load_results_table()
            
            self.main_window.refresh_components()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen des Ergebnisses: {str(e)}")

    def on_weapon_select(self, event):
        try:
            selected_item = self.weapon_tree.selection()[0]
            values = self.weapon_tree.item(selected_item, 'values')
            self.selected_weapon_id = values[0]
        except IndexError:
            pass

    def on_ammo_select(self, event):
        try:
            selected_item = self.ammo_tree.selection()[0]
            values = self.ammo_tree.item(selected_item, 'values')
            self.selected_ammo_id = values[0]
        except IndexError:
            pass

    def on_distance_select(self, event):
        try:
            selected_item = self.distance_tree.selection()[0]
            values = self.distance_tree.item(selected_item, 'values')
            self.selected_distance_id = values[0]
        except IndexError:
            pass

    def remove_weapon(self):
        if self.selected_weapon_id is None:
            messagebox.showerror("Fehler", "Keine Waffe ausgewählt")
            return
        
        confirm = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie diese Waffe löschen möchten?")
        if not confirm:
            return
        
        try:
            self.db_manager.remove_weapon(self.selected_weapon_id)
            messagebox.showinfo("Erfolg", "Waffe erfolgreich gelöscht")
            
            self.selected_weapon_id = None
            
            self.load_weapons_table()
            
            self.main_window.refresh_components()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Löschen der Waffe: {str(e)}")

    def add_ammo(self):
        try:
            ammo_name = self.ammo_name_var.get().strip()
            caliber = self.ammo_caliber_var.get().strip()
            unit = self.ammo_caliber_unit_var.get()
            
            if not ammo_name:
                messagebox.showerror("Fehler", "Munitionsname ist erforderlich")
                return
                
            if not caliber:
                messagebox.showerror("Fehler", "Kaliber ist erforderlich")
                return
                
            if not validate_name(ammo_name):
                messagebox.showerror("Fehler", "Munitionsname enthält ungültige Zeichen")
                return
                
            if not validate_decimal(caliber):
                messagebox.showerror("Fehler", "Kaliber muss eine gültige Zahl sein")
                return
                
            caliber_with_unit = f"{caliber} {unit}"
            
            self.db_manager.add_ammunition(ammo_name, caliber_with_unit)
            messagebox.showinfo("Erfolg", f"Munition hinzugefügt: {ammo_name}")
            
            self.ammo_name_var.set("")
            self.ammo_caliber_var.set("")
            
            self.load_ammo_table()
            
            self.main_window.refresh_components()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Hinzufügen der Munition: {str(e)}")

    def remove_ammo(self):
        if not self.selected_ammo_id:
            messagebox.showerror("Fehler", "Keine Munition ausgewählt")
            return
    
        selected_items = self.ammo_tree.selection()
        if not selected_items:
            return
            
        item = selected_items[0]
        values = self.ammo_tree.item(item, 'values')
        if not values:
            return
        
        ammo_name = values[1]
        
        if not messagebox.askyesno("Löschen bestätigen", f"Sind Sie sicher, dass Sie die Munition '{ammo_name}' löschen möchten?"):
            return
            
        try:
            self.db_manager.remove_ammunition(ammo_name)
            messagebox.showinfo("Erfolg", f"Munition entfernt: {ammo_name}")
            
            self.load_ammo_table()
            
            self.selected_ammo_id = None
            
            self.main_window.refresh_components()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Entfernen der Munition: {str(e)}")

    def remove_distance(self):
        if self.selected_distance_id is None:
            messagebox.showerror("Fehler", "Keine Entfernung ausgewählt")
            return
        
        confirm = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie diese Entfernung löschen möchten?")
        if not confirm:
            return
        
        try:
            self.db_manager.remove_distance(self.selected_distance_id)
            messagebox.showinfo("Erfolg", "Entfernung erfolgreich gelöscht")
            
            self.selected_distance_id = None
            
            self.load_distances_table()
            
            self.main_window.refresh_components()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Löschen der Entfernung: {str(e)}")

    def remove_result(self):
        if self.selected_result_id is None:
            messagebox.showerror("Fehler", "Kein Ergebnis ausgewählt")
            return
        
        confirm = messagebox.askyesno("Bestätigung", "Sind Sie sicher, dass Sie dieses Ergebnis löschen möchten?")
        if not confirm:
            return
        
        try:
            self.db_manager.remove_result(self.selected_result_id)
            messagebox.showinfo("Erfolg", "Ergebnis erfolgreich gelöscht")
            
            self.selected_result_id = None
            
            self.load_results_table()
            
            self.main_window.refresh_components()
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Löschen des Ergebnisses: {str(e)}")

    def show_weapon_context_menu(self, event):
        try:
            self.weapon_tree.selection_set(self.weapon_tree.identify_row(event.y))
            self.weapon_context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            pass

    def show_ammo_context_menu(self, event):
        try:
            self.ammo_tree.selection_set(self.ammo_tree.identify_row(event.y))
            self.ammo_context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            pass

    def show_distance_context_menu(self, event):
        try:
            self.distance_tree.selection_set(self.distance_tree.identify_row(event.y))
            self.distance_context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            pass

    def show_result_context_menu(self, event):
        try:
            self.results_tree.selection_set(self.results_tree.identify_row(event.y))
            self.results_context_menu.post(event.x_root, event.y_root)
        except Exception as e:
            pass
    
    def close(self):
        self.window.destroy()
