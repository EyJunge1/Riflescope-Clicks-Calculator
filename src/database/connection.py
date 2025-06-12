import sqlite3
import os
from tkinter import messagebox

# Try to import logger, but fall back to a mock if not available
try:
    from ..core import db_connection_logger
except ImportError:
    class MockLogger:
        def debug(self, msg, *args, **kwargs): pass
        def info(self, msg, *args, **kwargs): pass
        def error(self, msg, *args, **kwargs): pass
    db_connection_logger = MockLogger()

class Database:
    def __init__(self, db_name):
        # Initialisierung der Datenbankverbindung
        self.db_name = db_name
        self.db_connection = None
        self.db_cursor = None
        db_connection_logger.info(f"Database-Instanz erstellt für: {db_name}")
        
    def __enter__(self):
        # Ermöglicht die Verwendung des with-Statements für die Datenbankverbindung
        db_connection_logger.debug("Entering database context")
        self.db_connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Wird beim Verlassen des with-Blocks aufgerufen und schließt die Datenbankverbindung
        db_connection_logger.debug("Exiting database context")
        self.db_close()
        return False

    def db_connect(self):
        # Stellt eine Verbindung zur Datenbank her
        try:
            db_connection_logger.info(f"Verbinde zur Datenbank: {self.db_name}")
            self.db_connection = sqlite3.connect(self.db_name)
            self.db_cursor = self.db_connection.cursor()
            db_connection_logger.info("Datenbankverbindung erfolgreich hergestellt")
        except sqlite3.Error as e:
            db_connection_logger.error(f"Fehler bei Datenbankverbindung: {e}")
            raise

    def db_create_folder(self):
        # Erstellt den Ordner für die Datenbank, falls dieser nicht existiert
        try:
            db_dir = os.path.dirname(self.db_name)
            if not os.path.exists(db_dir):
                db_connection_logger.info(f"Erstelle Datenbankverzeichnis: {db_dir}")
                os.makedirs(db_dir)
                db_connection_logger.info("Datenbankverzeichnis erfolgreich erstellt")
        except OSError as e:
            db_connection_logger.error(f"Fehler beim Erstellen des Datenbankverzeichnisses: {e}")
            raise

    def db_create(self):
        # Erstellt die Datenbank und die erforderlichen Tabellen
        try:
            db_connection_logger.info("Initialisiere Datenbank")
            self.db_create_folder()
            self.db_connect()
            self.db_create_table(self.db_cursor)
            self.db_commit()
            db_connection_logger.info("Datenbank erfolgreich initialisiert")
        except sqlite3.Error as e:
            db_connection_logger.error(f"Fehler bei Datenbankerstellung: {e}")
            raise

    def db_create_table(self, db_cursor):
        # Erstellt die Tabellen für Waffen, Munition, Entfernungen und Ergebnisse mit verbesserten Constraints
        try:
            db_connection_logger.debug("Erstelle Datenbanktabellen")
            
            # Waffentabelle mit unique constraint für Waffennamen und Erstellungsdatum
            db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS weapons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    weapon TEXT NOT NULL, 
                    caliber TEXT NOT NULL,
                    UNIQUE(weapon)
                )
            ''')
            
            # Munitionstabelle mit unique constraint für Munitionsname und Erstellungsdatum
            db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS ammunition (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    ammunition TEXT NOT NULL, 
                    caliber TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(ammunition)
                )
            ''')
            
            # Entfernungstabelle mit unique constraint für Distanz-Einheits-Kombinationen
            db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS distances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    distance TEXT NOT NULL, 
                    unit TEXT NOT NULL,
                    UNIQUE(distance, unit)
                )
            ''')
            
            # Ergebnistabelle mit unique constraint für Waffe-Munition-Entfernung-Kombination
            # und ON DELETE CASCADE für Fremdschlüssel
            db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    weapon_id INTEGER NOT NULL, 
                    ammunition_id INTEGER NOT NULL, 
                    distance_id INTEGER NOT NULL, 
                    result TEXT NOT NULL,
                    UNIQUE(weapon_id, ammunition_id, distance_id),
                    FOREIGN KEY (weapon_id) REFERENCES weapons (id) ON DELETE CASCADE,
                    FOREIGN KEY (ammunition_id) REFERENCES ammunition (id) ON DELETE CASCADE,
                    FOREIGN KEY (distance_id) REFERENCES distances (id) ON DELETE CASCADE
                )
            ''')
            
            # Indices für bessere Abfrageleistung
            db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_weapons_caliber ON weapons(caliber)')
            db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_ammunition_caliber ON ammunition(caliber)')
            db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_distances_unit ON distances(unit)')
            db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_weapon ON results(weapon_id)')
            db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_ammo ON results(ammunition_id)')
            db_cursor.execute('CREATE INDEX IF NOT EXISTS idx_results_distance ON results(distance_id)')
            
            db_connection_logger.info("Alle Datenbanktabellen erfolgreich erstellt")
            
        except sqlite3.Error as e:
            db_connection_logger.error(f"Fehler beim Erstellen der Tabellen: {e}")
            raise

    def db_commit(self):
        # Speichert die Änderungen in der Datenbank
        try:
            if self.db_connection:
                self.db_connection.commit()
                db_connection_logger.debug("Datenbankänderungen committed")
        except sqlite3.Error as e:
            db_connection_logger.error(f"Fehler beim Commit: {e}")
            raise

    def db_close(self):
        # Schließt die Datenbankverbindung
        try:
            if self.db_connection:
                self.db_connection.close()
                self.db_connection = None
                self.db_cursor = None
                db_connection_logger.info("Datenbankverbindung geschlossen")
        except sqlite3.Error as e:
            db_connection_logger.error(f"Fehler beim Schließen der Datenbankverbindung: {e}")
            messagebox.showerror("Datenbankfehler", f"Fehler beim Schließen der Datenbankverbindung: {str(e)}")
