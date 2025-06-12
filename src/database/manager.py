import re
from tkinter import messagebox
from .connection import Database
from .entities import Weapon, Ammunition, Distance, Result
from ..core import db_manager_logger
from ..models import WeaponModel, AmmunitionModel, DistanceModel, ResultModel

# Klasse zum vereinfachten Zugriff auf die Datenbank
class DatabaseManager:
    def __init__(self, db_path):
        # Initialisierung des Datenbankmanagers mit dem Datenbankpfad
        self.db_path = db_path
        self.db = Database(db_path)
        db_manager_logger.info(f"DatabaseManager initialisiert für: {db_path}")
        
    def initialize_database(self):
        # Initialisiert die Datenbank und erstellt die Tabellen
        try:
            db_manager_logger.info("Initialisiere Datenbank")
            self.db.db_create()
            db_manager_logger.info("Datenbank erfolgreich initialisiert")
        except Exception as e:
            db_manager_logger.error(f"Fehler bei der Datenbankinitialisierung: {e}")
            messagebox.showerror("Datenbankfehler", f"Fehler bei der Initialisierung der Datenbank: {str(e)}")
    
    # Methoden zum Abrufen von Daten aus der Datenbank
    def get_weapons(self):
        # Ruft alle Waffen aus der Datenbank ab - Rückgabe als Tupel für GUI-Kompatibilität
        try:
            db_manager_logger.debug("Lade alle Waffen")
            with self.db as db:
                weapon = Weapon(db.db_cursor)
                weapons_data = weapon.get_all()
                db_manager_logger.info(f"{len(weapons_data)} Waffen geladen")
                return weapons_data  # Rückgabe als Tupel für GUI-Kompatibilität
        except Exception as e:
            db_manager_logger.error(f"Fehler beim Laden der Waffen: {e}")
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Waffen: {str(e)}")
            return []
    
    def get_ammunition(self):
        try:
            with self.db as db:
                ammo = Ammunition(db.db_cursor)
                return ammo.get_all()  # Rückgabe als Tupel für GUI-Kompatibilität
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Munition: {str(e)}")
            return []
    
    def get_distances(self):
        try:
            with self.db as db:
                distance = Distance(db.db_cursor)
                return distance.get_all()  # Rückgabe als Tupel für GUI-Kompatibilität
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Entfernungen: {str(e)}")
            return []

    def add_weapon(self, weapon_name, caliber):
        try:
            db_manager_logger.info(f"Füge Waffe hinzu: {weapon_name} ({caliber})")
            with self.db as db:
                weapon = Weapon(db.db_cursor)
                weapon_id = weapon.insert(weapon_name, caliber)
                db.db_commit()
                db_manager_logger.info(f"Waffe erfolgreich hinzugefügt mit ID: {weapon_id}")
                return weapon_id
        except Exception as e:
            db_manager_logger.error(f"Fehler beim Hinzufügen der Waffe '{weapon_name}': {e}")
            raise
    
    def remove_weapon(self, weapon_name):
        try:
            with self.db as db:
                weapon = Weapon(db.db_cursor)
                weapon.remove(weapon_name=weapon_name)
                db.db_commit()
        except Exception as e:
            raise
    
    def add_ammunition(self, ammo_name, caliber):
        try:
            with self.db as db:
                ammo = Ammunition(db.db_cursor)
                ammo_id = ammo.insert(ammo_name, caliber)
                db.db_commit()
                return ammo_id
        except Exception as e:
            raise
    
    def remove_ammunition(self, ammo_name):
        try:
            with self.db as db:
                ammo = Ammunition(db.db_cursor)
                ammo.remove(ammo_name=ammo_name)
                db.db_commit()
        except Exception as e:
            raise
    
    def add_distance(self, distance_value, unit):
        try:
            with self.db as db:
                distance = Distance(db.db_cursor)
                distance_id = distance.insert(distance_value, unit)
                db.db_commit()
                return distance_id
        except Exception as e:
            raise
    
    def remove_distance(self, distance_value):
        try:
            with self.db as db:
                distance = Distance(db.db_cursor)
                distance.remove(distance_value=distance_value)
                db.db_commit()
        except Exception as e:
            raise
    
    def add_result(self, weapon_name, ammo_name, distance_display, result_value):
        try:
            match = re.match(r'(\d+)([a-zA-Z]+)', distance_display)
            if not match:
                raise ValueError(f"Invalid distance format: {distance_display}")
                    
            distance_value, unit = match.groups()
            
            with self.db as db:
                db.db_cursor.execute('SELECT id FROM weapons WHERE weapon = ?', (weapon_name,))
                weapon_id_record = db.db_cursor.fetchone()
                
                db.db_cursor.execute('SELECT id FROM ammunition WHERE ammunition = ?', (ammo_name,))
                ammo_id_record = db.db_cursor.fetchone()
                
                db.db_cursor.execute('SELECT id FROM distances WHERE distance = ? AND unit = ?', 
                                    (distance_value, unit))
                distance_id_record = db.db_cursor.fetchone()
                
                if not all([weapon_id_record, ammo_id_record, distance_id_record]):
                    raise ValueError("Could not find all required IDs")
                    
                weapon_id = weapon_id_record[0]
                ammo_id = ammo_id_record[0]
                distance_id = distance_id_record[0]
                    
                result = Result(db.db_cursor)
                result_id = result.insert(weapon_id, ammo_id, distance_id, result_value)
                db.db_commit()
                return result_id
        except Exception as e:
            raise
    
    def get_results(self):
        try:
            with self.db as db:
                result = Result(db.db_cursor)
                return result.get_all()  # Rückgabe als Tupel für GUI-Kompatibilität
        except Exception:
            return []
    
    def get_result_by_weapon_ammo_distance(self, weapon_name, ammo_name, distance_display):
        try:
            match = re.match(r'(\d+)([a-zA-Z]+)', distance_display)
            if not match:
                return None
                    
            distance_value, unit = match.groups()
            
            with self.db as db:    
                db.db_cursor.execute('SELECT id FROM weapons WHERE weapon = ?', (weapon_name,))
                weapon_id = db.db_cursor.fetchone()
                
                db.db_cursor.execute('SELECT id FROM ammunition WHERE ammunition = ?', (ammo_name,))
                ammo_id = db.db_cursor.fetchone()
                
                db.db_cursor.execute('SELECT id FROM distances WHERE distance = ? AND unit = ?', 
                                    (distance_value, unit))
                distance_id = db.db_cursor.fetchone()
                
                if not all([weapon_id, ammo_id, distance_id]):
                    return None
                    
                result = Result(db.db_cursor)
                return result.get_by_weapon_ammo_distance(weapon_id[0], ammo_id[0], distance_id[0])
                
        except Exception as e:
            return None

    def get_ammunition_by_caliber(self, caliber):
        try:
            with self.db as db:
                db.db_cursor.execute('SELECT * FROM ammunition WHERE caliber = ?', (caliber,))
                return db.db_cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Munition nach Kaliber: {str(e)}")
            return []
    
    def get_weapon_caliber(self, weapon_name):
        try:
            with self.db as db:
                db.db_cursor.execute('SELECT caliber FROM weapons WHERE weapon = ?', (weapon_name,))
                result = db.db_cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen des Waffenkalibers: {str(e)}")
            return None

    def update_result(self, result_id, new_value):
        try:
            with self.db as db:
                result = Result(db.db_cursor)
                result.update(result_id, new_value)
                db.db_commit()
                return result_id
        except Exception as e:
            raise
    
    def remove_result(self, result_id):
        try:
            with self.db as db:
                result = Result(db.db_cursor)
                result.remove(result_id)
                db.db_commit()
        except Exception as e:
            raise
    
    def get_results_by_criteria(self, weapon_id=None, ammo_id=None, distance_id=None):
        try:
            with self.db as db:
                result = Result(db.db_cursor)
                return result.get_by_criteria(weapon_id, ammo_id, distance_id)
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Ergebnisse: {str(e)}")
            return []
    
    def get_weapon_id(self, weapon_name):
        try:
            with self.db as db:
                db.db_cursor.execute('SELECT id FROM weapons WHERE weapon = ?', (weapon_name,))
                result = db.db_cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Waffen-ID: {str(e)}")
            return None
    
    def get_ammunition_id(self, ammo_name):
        try:
            with self.db as db:
                db.db_cursor.execute('SELECT id FROM ammunition WHERE ammunition = ?', (ammo_name,))
                result = db.db_cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Munitions-ID: {str(e)}")
            return None
    
    def get_distance_id(self, distance_value, unit):
        try:
            with self.db as db:
                db.db_cursor.execute('SELECT id FROM distances WHERE distance = ? AND unit = ?', 
                                    (distance_value, unit))
                result = db.db_cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Entfernungs-ID: {str(e)}")
            return None

    # Neue Methoden für Model-Objekte (für interne Verwendung)
    def get_weapons_as_models(self):
        """Ruft alle Waffen als Model-Objekte ab"""
        try:
            with self.db as db:
                weapon = Weapon(db.db_cursor)
                weapons_data = weapon.get_all()
                # Konvertiere zu WeaponModel-Objekten
                weapons = [WeaponModel(id=w[0], weapon=w[1], caliber=w[2]) 
                          for w in weapons_data]
                return weapons
        except Exception as e:
            db_manager_logger.error(f"Fehler beim Laden der Waffen als Models: {e}")
            return []
    
    def get_ammunition_as_models(self):
        """Ruft alle Munition als Model-Objekte ab"""
        try:
            with self.db as db:
                ammo = Ammunition(db.db_cursor)
                ammo_data = ammo.get_all()
                # Konvertiere zu AmmunitionModel-Objekten
                ammunition = [AmmunitionModel(id=a[0], ammunition=a[1], caliber=a[2]) 
                             for a in ammo_data]
                return ammunition
        except Exception as e:
            db_manager_logger.error(f"Fehler beim Laden der Munition als Models: {e}")
            return []
    
    def get_distances_as_models(self):
        """Ruft alle Entfernungen als Model-Objekte ab"""
        try:
            with self.db as db:
                distance = Distance(db.db_cursor)
                distance_data = distance.get_all()
                # Konvertiere zu DistanceModel-Objekten
                distances = [DistanceModel(id=d[0], distance=d[1], unit=d[2]) 
                            for d in distance_data]
                return distances
        except Exception as e:
            db_manager_logger.error(f"Fehler beim Laden der Entfernungen als Models: {e}")
            return []
