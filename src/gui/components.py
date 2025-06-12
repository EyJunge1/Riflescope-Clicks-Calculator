import tkinter as tk
from tkinter import messagebox, ttk

# Basisklasse für alle GUI-Komponenten mit verbesserter Architektur
class BaseGUIComponent:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self._initialized = False
        self._setup_component(**kwargs)
    
    def _setup_component(self, **kwargs):
        """Override in subclasses for component-specific setup"""
        pass
    
    def refresh(self):
        """Methode zum Aktualisieren der Komponente - override in subclasses"""
        if not self._initialized:
            return
    
    def get_value(self):
        """Get current component value - override in subclasses"""
        return None
    
    def set_value(self, value):
        """Set component value - override in subclasses"""
        pass
    
    def validate(self):
        """Validate component state - override in subclasses"""
        return True
    
    def _mark_initialized(self):
        """Mark component as fully initialized"""
        self._initialized = True

# Komponente zur Anzeige der Ergebnisse
class ResultDisplay(BaseGUIComponent):
    def __init__(self, parent, row, column, padx, pady, result='0'):
        # Initialisierung der Ergebnisanzeige
        super().__init__(parent)
        
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        
        # Container für die Ergebnisanzeige
        result_container = ttk.Frame(parent)
        result_container.grid(row=row, column=column, columnspan=3, sticky='ew')
        
        result_container.columnconfigure(0, weight=1)
        
        # Label für die Zielposition
        self.result_label = ttk.Label(
            result_container, 
            text=f'Zielposition: {result}', 
            style='Result.TLabel'
        )
        self.result_label.grid(row=0, column=0, padx=padx, pady=pady)
        
        # Label für die Anzahl der Klicks
        self.clicks_label = ttk.Label(
            result_container, 
            text='Anpassung: 0 Klicks', 
            style='Result.TLabel'
        )
        self.clicks_label.grid(row=1, column=0, padx=padx, pady=pady)
        
        # Label für die Richtung der Anpassung
        self.direction_label = ttk.Label(
            result_container, 
            text='Richtung: -', 
            style='Result.TLabel'
        )
        self.direction_label.grid(row=2, column=0, padx=padx, pady=pady)
    
    def update_result(self, result):
        # Aktualisiert die angezeigte Zielposition
        self.result_label.config(text=f'Zielposition: {result}')
    
    def update_clicks(self, clicks, direction):
        # Aktualisiert die Anzeige der Klicks und der Richtung
        self.clicks_label.config(text=f'Anpassung: {clicks} Klicks')
        direction_text = direction.capitalize() if direction else '-'
        self.direction_label.config(text=f'Richtung: {direction_text}')

# Komponente für die Eingabe der aktuellen Position
class CurrentPositionInput(BaseGUIComponent):
    def __init__(self, parent, row, column, padx, pady):
        # Initialisierung der Eingabekomponente
        super().__init__(parent)
        self.position_var = tk.StringVar()
        
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        
        # Rahmen für die Eingabekomponente
        input_frame = ttk.Frame(parent)
        input_frame.grid(row=row, column=column, columnspan=3, sticky='ew')
        
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        
        # Label und Eingabefeld für die aktuelle Position
        current_position_label = ttk.Label(input_frame, text='Aktuelle Position:')
        current_position_label.grid(row=0, column=0, padx=padx, pady=pady, sticky='e')
        
        current_position_entry = ttk.Entry(input_frame, textvariable=self.position_var, width=10)
        current_position_entry.grid(row=0, column=1, padx=padx, pady=pady, sticky='w')
        
        # Hinweistext für den Benutzer
        hint_label = ttk.Label(input_frame, text='(Geben Sie die aktuelle Klickeinstellung Ihres Zielfernrohrs ein)',
                             font=('Segoe UI', 8), foreground='#666666')
        hint_label.grid(row=1, column=0, columnspan=2, padx=padx, pady=(0, pady))
    
    def get_position(self):
        # Gibt die eingegebene Position zurück
        return self.position_var.get().strip()

# Komponente zur Auswahl der Waffe
class WeaponSelector:
    def __init__(self, parent, row, column, padx, pady, db_manager, ammo_selector=None):
        self.db_manager = db_manager
        self.ammo_selector = ammo_selector
        
        ttk.Label(parent, text="Waffe:").grid(row=row, column=column, padx=padx, pady=pady, sticky='w')
        
        weapons = self.db_manager.get_weapons()
        # Verwende nur Tupel-Format
        if weapons:
            self.weapon_names = [weapon[1] for weapon in weapons]
        else:
            self.weapon_names = ['Keine Waffen']
        
        self.weapon_var = tk.StringVar()
        self.weapon_var.set(self.weapon_names[0])
        
        self.weapon_menu = ttk.OptionMenu(parent, self.weapon_var, *self.weapon_names)
        self.weapon_menu.grid(row=row, column=column+1, padx=padx, pady=pady, sticky='w')
        
        if self.ammo_selector:
            self.weapon_var.trace('w', self.on_weapon_var_change)
    
    def on_weapon_var_change(self, *args):
        selected_weapon = self.weapon_var.get()
        if self.ammo_selector:
            self.ammo_selector.update_for_weapon(selected_weapon)
    
    def on_weapon_select(self, selected_weapon):
        if self.ammo_selector:
            self.ammo_selector.update_for_weapon(selected_weapon)
    
    def select_weapon(self):
        messagebox.showinfo('Setzen', f'Ausgewählte Waffe: {self.weapon_var.get()}')
        
    def get_selected_weapon(self):
        return self.weapon_var.get()
        
    def refresh(self):
        weapons = self.db_manager.get_weapons()
        # Verwende nur Tupel-Format
        if weapons:
            self.weapon_names = [weapon[1] for weapon in weapons]
        else:
            self.weapon_names = ['Keine Waffen']
        
        self.weapon_menu['menu'].delete(0, 'end')
        
        for name in self.weapon_names:
            self.weapon_menu['menu'].add_command(
                label=name, 
                command=lambda n=name: self.weapon_var.set(n)
            )
            
        if self.weapon_names:
            self.weapon_var.set(self.weapon_names[0])

# Komponente zur Auswahl der Munition
class AmmunitionSelector:
    def __init__(self, parent, row, column, padx, pady, db_manager):
        self.db_manager = db_manager
        
        ttk.Label(parent, text="Munition:").grid(row=row, column=column, padx=padx, pady=pady, sticky='w')
        
        ammunition = self.db_manager.get_ammunition()
        # Verwende nur Tupel-Format
        if ammunition:
            self.ammo_names = [ammo[1] for ammo in ammunition]
        else:
            self.ammo_names = ['Keine Munition']
        
        self.ammo_var = tk.StringVar()
        self.ammo_var.set(self.ammo_names[0])
        
        self.ammo_menu = ttk.OptionMenu(parent, self.ammo_var, *self.ammo_names)
        self.ammo_menu.grid(row=row, column=column+1, padx=padx, pady=pady, sticky='w')
    
    def update_for_weapon(self, weapon_name):
        if weapon_name == 'Keine Waffen':
            return
        
        caliber = self.db_manager.get_weapon_caliber(weapon_name)
        if not caliber:
            return
            
        matching_ammo = self.db_manager.get_ammunition_by_caliber(caliber)
        # Verwende nur Tupel-Format
        if matching_ammo:
            matching_ammo_names = [ammo[1] for ammo in matching_ammo]
        else:
            matching_ammo_names = ['Keine passende Munition']
        
        self.ammo_menu['menu'].delete(0, 'end')
        
        for name in matching_ammo_names:
            self.ammo_menu['menu'].add_command(
                label=name,
                command=lambda n=name: self.ammo_var.set(n)
            )
        
        if matching_ammo_names:
            self.ammo_var.set(matching_ammo_names[0])
        else:
            self.ammo_var.set('Keine passende Munition')
    
    def select_ammunition(self):
        messagebox.showinfo('Setzen', f'Ausgewählte Munition: {self.ammo_var.get()}')
        
    def get_selected_ammunition(self):
        return self.ammo_var.get()
        
    def refresh(self):
        ammunition = self.db_manager.get_ammunition()
        # Verwende nur Tupel-Format
        if ammunition:
            self.ammo_names = [ammo[1] for ammo in ammunition]
        else:
            self.ammo_names = ['Keine Munition']
        
        self.ammo_menu['menu'].delete(0, 'end')
        
        for name in self.ammo_names:
            self.ammo_menu['menu'].add_command(
                label=name, 
                command=lambda n=name: self.ammo_var.set(n)
            )
            
        if self.ammo_names:
            self.ammo_var.set(self.ammo_names[0])

# Komponente zur Auswahl der Entfernung
class DistanceSelector:
    def __init__(self, parent, row, column, padx, pady, db_manager):
        self.db_manager = db_manager
        
        ttk.Label(parent, text="Entfernung:").grid(row=row, column=column, padx=padx, pady=pady, sticky='w')
        
        distances = self.db_manager.get_distances()
        # Verwende nur Tupel-Format
        if distances:
            self.distance_names = [f"{dist[1]}{dist[2]}" for dist in distances]
        else:
            self.distance_names = ['Keine Entfernungen']
        
        self.distance_var = tk.StringVar()
        self.distance_var.set(self.distance_names[0])
        
        self.distance_menu = ttk.OptionMenu(parent, self.distance_var, *self.distance_names)
        self.distance_menu.grid(row=row, column=column+1, padx=padx, pady=pady, sticky='w')
    
    def select_distance(self):
        messagebox.showinfo('Setzen', f'Ausgewählte Entfernung: {self.distance_var.get()}')
        
    def get_selected_distance(self):
        return self.distance_var.get()
        
    def refresh(self):
        distances = self.db_manager.get_distances()
        # Verwende nur Tupel-Format
        if distances:
            self.distance_names = [f"{dist[1]}{dist[2]}" for dist in distances]
        else:
            self.distance_names = ['Keine Entfernungen']
        
        self.distance_menu['menu'].delete(0, 'end')
        
        for name in self.distance_names:
            self.distance_menu['menu'].add_command(
                label=name,
                command=lambda n=name: self.distance_var.set(n)
            )
            
        if self.distance_names:
            self.distance_var.set(self.distance_names[0])

# Add the missing tooltip creation method that was in MainWindow
def create_tooltip(widget, text):
    """Creates a tooltip for the given widget"""
    def enter(event):
        try:
            x, y, cx, cy = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
        except:
            # Fallback if bbox fails
            x = widget.winfo_rootx() + 25
            y = widget.winfo_rooty() + 25
        
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ttk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, padding=(5, 2))
        label.pack()
        
        # Store tooltip reference to destroy it later
        widget._tooltip = tooltip
        
    def leave(event):
        if hasattr(widget, '_tooltip'):
            widget._tooltip.destroy()
            delattr(widget, '_tooltip')
            
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)
