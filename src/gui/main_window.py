import os
import tkinter as tk
from tkinter import messagebox, ttk
from ..config import AppSettings
from ..utils.calculator import ClickCalculator
from ..utils.validators import validate_number
from ..core import gui_main_logger
from .components import (
    ResultDisplay, 
    CurrentPositionInput, 
    WeaponSelector, 
    AmmunitionSelector, 
    DistanceSelector,
    create_tooltip
)
from .settings_window import SettingsWindow

# Hauptfenster der Anwendung
class MainWindow:
    def __init__(self, db_manager):
        gui_main_logger.info("Initialisiere Hauptfenster")
        self.db_manager = db_manager
        
        # Initialize window
        self._create_main_window()
        
        # Setup window properties
        self._setup_window_properties()
        
        # Setup UI components
        self._setup_ui_components()
        
        gui_main_logger.info("Hauptfenster erfolgreich initialisiert")
    
    def _create_main_window(self):
        """Create the main tkinter window"""
        self.root = tk.Tk()
        self.root.title(AppSettings.APP_TITLE)
        self.root.geometry(AppSettings.MAIN_WINDOW_SIZE)
        self.root.resizable(False, False)
        
        # Store project root for icon loading
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    def _setup_window_properties(self):
        """Setup window styling, icon, and positioning"""
        self.setup_style()
        self.load_icon()
        self.center_window()
    
    def _setup_ui_components(self):
        """Setup all UI components"""
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.setup_components()

    def setup_style(self):
        # Konfiguriert den visuellen Stil der Anwendung
        self.style = ttk.Style()
        
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
        
        # Use settings from AppSettings
        bg_color = AppSettings.BACKGROUND_COLOR
        accent_color = AppSettings.ACCENT_COLOR
        button_color = AppSettings.BUTTON_COLOR
        
        # Konfiguration des Stils für verschiedene Widgets
        self.root.configure(bg=bg_color)
        
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, font=('Segoe UI', 10))
        self.style.configure('TButton', background=button_color, foreground='white', 
                            font=('Segoe UI', 10, 'bold'), borderwidth=0)
        self.style.map('TButton', 
                     background=[('active', accent_color), ('pressed', '#2c5e87')])
        
        # Benutzerdefinierte Stile für spezielle Widgets
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=accent_color)
        self.style.configure('Result.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#333333')
        self.style.configure('Big.TButton', font=('Segoe UI', 12, 'bold'))
    
    def center_window(self):
        self.root.update_idletasks()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f'+{x}+{y}')
    
    def load_icon(self):
        # Priorität auf target_icon.ico
        icon_locations = [
            os.path.join(self.project_root, "icons", "target_icon.ico"),
            os.path.join(AppSettings.get_icons_dir(), "target_icon.ico"),
            os.path.join("icons", "target_icon.ico"),
            "target_icon.ico"
        ]
        
        for icon_path in icon_locations:
            if os.path.exists(icon_path):
                try:
                    self.root.iconbitmap(icon_path)
                    gui_main_logger.info(f"Icon erfolgreich geladen: {icon_path}")
                    return
                except tk.TclError as e:
                    gui_main_logger.warning(f"Icon konnte nicht geladen werden: {icon_path} - {e}")
                    continue
        
        gui_main_logger.warning("Kein gültiges Icon gefunden (target_icon.ico)")
    
    def setup_components(self):
        for i in range(3):
            self.main_frame.columnconfigure(i, weight=1)
        
        title_label = ttk.Label(self.main_frame, text=AppSettings.APP_NAME, style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="n")
        
        selection_frame = ttk.LabelFrame(self.main_frame, text="Auswahl", padding="10 5 10 5")
        selection_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        for i in range(3):
            selection_frame.columnconfigure(i, weight=1)
        
        position_frame = ttk.LabelFrame(self.main_frame, text="Aktuelle Position", padding="10 5 10 5")
        position_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        result_frame = ttk.LabelFrame(self.main_frame, text="Ergebnis", padding="10 5 10 5")
        result_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        self.ammo_selector = AmmunitionSelector(selection_frame, row=1, column=0, padx=5, pady=5, db_manager=self.db_manager)
        
        self.weapon_selector = WeaponSelector(selection_frame, row=0, column=0, padx=5, pady=5, 
                                           db_manager=self.db_manager, ammo_selector=self.ammo_selector)
        
        self.distance_selector = DistanceSelector(selection_frame, row=2, column=0, padx=5, pady=5, db_manager=self.db_manager)
        
        if self.weapon_selector.weapon_names and self.weapon_selector.weapon_names[0] != 'Keine Waffen':
            self.weapon_selector.on_weapon_var_change()
        
        self.position_input = CurrentPositionInput(position_frame, row=0, column=0, padx=5, pady=5)
        
        self.result_display = ResultDisplay(result_frame, row=0, column=0, padx=5, pady=5, result='0')
        
        action_frame = ttk.Frame(self.main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=10)
        
        calculate_button = ttk.Button(action_frame, text='Klicks berechnen', 
                                    command=self.calculate_clicks, style='Big.TButton')
        calculate_button.pack(fill='x')
        
        create_tooltip(calculate_button, "Berechnen Sie die Anpassung der Zielfernrohrklicks basierend auf Ihren Auswahl")
        
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=10)
        button_frame.columnconfigure(0, weight=1)
        
        settings_button = ttk.Button(button_frame, text='Einstellungen', width=15,
                                   command=self.open_settings_window)
        settings_button.grid(row=0, column=0, padx=5, pady=5)
        
        create_tooltip(settings_button, "Konfigurieren Sie Waffen, Munition und Entfernungen")
        
        quit_frame = ttk.Frame(self.main_frame)
        quit_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)
        quit_frame.columnconfigure(0, weight=1)
        
        quit_button = ttk.Button(quit_frame, text='Beenden', width=15, command=self.root.quit)
        quit_button.grid(row=0, column=0, pady=5)
        
        self.main_frame.update()
    
    def calculate_clicks(self):
        # Berechnet die Klicks basierend auf der aktuellen Position und dem gespeicherten Zielwert
        gui_main_logger.debug("Starte Klickberechnung")
        
        try:
            # Erfassen der Eingabewerte
            current_position = self.position_input.get_position()
            weapon_name = self.weapon_selector.get_selected_weapon()
            ammo_name = self.ammo_selector.get_selected_ammunition()
            distance_display = self.distance_selector.get_selected_distance()
            
            gui_main_logger.debug(f"Eingabewerte - Position: {current_position}, Waffe: {weapon_name}, Munition: {ammo_name}, Entfernung: {distance_display}")
            
            # Überprüfung der Eingabewerte
            if not current_position:
                messagebox.showerror("Fehler", "Bitte geben Sie Ihre aktuelle Position ein")
                return
                
            if not validate_number(current_position):
                messagebox.showerror("Fehler", "Die aktuelle Position darf nur Ziffern enthalten")
                return
                
            if weapon_name == 'Keine Waffen' or ammo_name == 'Keine Munition' or distance_display == 'Keine Entfernungen':
                messagebox.showerror("Fehler", "Bitte wählen Sie gültige Waffen-, Munitions- und Entfernungswerte aus")
                return
                
            # Abrufen des gespeicherten Ergebnisses für die Kombination
            result = self.db_manager.get_result_by_weapon_ammo_distance(
                weapon_name, ammo_name, distance_display)
            
            if not result:
                messagebox.showerror("Fehler", 
                                   f"Kein Ergebnis für die Kombination aus {weapon_name}, {ammo_name}, bei {distance_display} gefunden")
                return
                
            target_position = result[5]
            
            # Aktualisieren der Ergebnisanzeige
            self.result_display.update_result(target_position)
            
            # Berechnen und Anzeigen der Klicks und der Richtung
            clicks, direction = ClickCalculator.calculate_clicks(current_position, target_position)
            
            gui_main_logger.info(f"Klickberechnung erfolgreich: {clicks} Klicks {direction if direction else 'keine Änderung'}")
            
            self.result_display.update_clicks(clicks, direction)
            
        except Exception as e:
            gui_main_logger.error(f"Fehler bei der Klickberechnung: {e}", exc_info=True)
            messagebox.showerror("Fehler", f"Fehler bei der Klickberechnung: {str(e)}")
    
    def open_settings_window(self):
        gui_main_logger.info("Öffne Einstellungsfenster")
        settings = SettingsWindow(self.root, self.db_manager, self)
        
    def refresh_components(self):
        gui_main_logger.debug("Aktualisiere GUI-Komponenten")
        self.weapon_selector.refresh()
        self.ammo_selector.refresh()
        self.distance_selector.refresh()
        gui_main_logger.debug("GUI-Komponenten erfolgreich aktualisiert")
    
    def run(self):
        gui_main_logger.info("Starte GUI-Hauptschleife")
        self.root.mainloop()
        gui_main_logger.info("GUI-Hauptschleife beendet")
