import sqlite3
from abc import ABC, abstractmethod
from ..core import db_entities_logger

# Abstrakte Basisklasse für alle Datenbankentitäten
class DatabaseEntity(ABC):
    def __init__(self, db_cursor):
        # Initialisierung mit einem Datenbankcursor
        if db_cursor is None:
            raise ValueError("Datenbankcursor darf nicht None sein")
        self.db_cursor = db_cursor
        db_entities_logger.debug(f"DatabaseEntity initialisiert: {self.__class__.__name__}")
    
    @abstractmethod
    def insert(self, *args, **kwargs):
        # Abstrakte Methode zum Einfügen von Datensätzen
        pass
    
    @abstractmethod
    def remove(self, *args, **kwargs):
        # Abstrakte Methode zum Entfernen von Datensätzen
        pass
    
    @abstractmethod
    def get_all(self, *args, **kwargs):
        # Abstrakte Methode zum Abrufen aller Datensätze
        pass

# Klasse zur Verwaltung von Waffen in der Datenbank
class Weapon(DatabaseEntity):
    def insert(self, weapon, caliber):
        # Fügt eine neue Waffe in die Datenbank ein
        try:
            if not weapon or not caliber:
                raise ValueError("Sowohl Waffe als auch Kaliber müssen Werte haben.")
            
            db_entities_logger.debug(f"Füge Waffe ein: {weapon} ({caliber})")
            self.db_cursor.execute('INSERT INTO weapons (weapon, caliber) VALUES (?, ?)', (weapon, caliber))
            weapon_id = self.db_cursor.lastrowid
            db_entities_logger.info(f"Waffe erfolgreich eingefügt mit ID {weapon_id}: {weapon}")
            return weapon_id
        except sqlite3.Error as e:
            db_entities_logger.error(f"Datenbankfehler beim Einfügen der Waffe '{weapon}': {e}")
            raise

    def remove(self, weapon_id=None, weapon_name=None):
        # Entfernt eine Waffe anhand der ID oder des Namens
        try:
            if weapon_id is not None:
                self.db_cursor.execute('DELETE FROM weapons WHERE id = ?', (weapon_id,))
                db_entities_logger.info(f"Waffe mit ID {weapon_id} entfernt.")
            elif weapon_name is not None:
                self.db_cursor.execute('DELETE FROM weapons WHERE weapon = ?', (weapon_name,))
                db_entities_logger.info(f"Waffe mit Namen '{weapon_name}' entfernt.")
            else:
                raise ValueError("Entweder weapon_id oder weapon_name muss angegeben werden.")
        except sqlite3.Error as e:
            db_entities_logger.error(f"Datenbankfehler beim Entfernen der Waffe: {e}")
            raise

    def get_all(self):
        # Ruft alle Waffen aus der Datenbank ab
        try:
            self.db_cursor.execute('SELECT * FROM weapons')
            results = self.db_cursor.fetchall()
            db_entities_logger.debug(f"Anzahl der gefundenen Waffen: {len(results)}")
            return results
        except sqlite3.Error as e:
            db_entities_logger.error(f"Datenbankfehler beim Abrufen der Waffen: {e}")
            raise
    
    def get_by_id(self, weapon_id):
        # Ruft eine Waffe anhand ihrer ID ab
        try:
            self.db_cursor.execute('SELECT * FROM weapons WHERE id = ?', (weapon_id,))
            result = self.db_cursor.fetchone()
            db_entities_logger.debug(f"Waffe abgerufen: {result}")
            return result
        except sqlite3.Error as e:
            db_entities_logger.error(f"Datenbankfehler beim Abrufen der Waffe mit ID {weapon_id}: {e}")
            raise

# Klasse zur Verwaltung von Munition in der Datenbank
class Ammunition(DatabaseEntity):
    def insert(self, ammunition, caliber):
        # Fügt neue Munition in die Datenbank ein
        try:
            if not ammunition or not caliber:
                raise ValueError("Sowohl Munition als auch Kaliber müssen Werte haben.")
            self.db_cursor.execute('INSERT INTO ammunition (ammunition, caliber) VALUES (?, ?)', (ammunition, caliber))
            return self.db_cursor.lastrowid
        except sqlite3.Error as e:
            raise

    def remove(self, ammo_id=None, ammo_name=None):
        # Entfernt Munition anhand der ID oder des Namens
        try:
            if ammo_id is not None:
                self.db_cursor.execute('DELETE FROM ammunition WHERE id = ?', (ammo_id,))
            elif ammo_name is not None:
                self.db_cursor.execute('DELETE FROM ammunition WHERE ammunition = ?', (ammo_name,))
            else:
                raise ValueError("Entweder ammo_id oder ammo_name muss angegeben werden.")
        except sqlite3.Error as e:
            raise

    def get_all(self):
        # Ruft alle Munitionsarten aus der Datenbank ab
        try:
            self.db_cursor.execute('SELECT * FROM ammunition')
            return self.db_cursor.fetchall()
        except sqlite3.Error as e:
            raise
    
    def get_by_id(self, ammo_id):
        # Ruft Munition anhand ihrer ID ab
        try:
            self.db_cursor.execute('SELECT * FROM ammunition WHERE id = ?', (ammo_id,))
            return self.db_cursor.fetchone()
        except sqlite3.Error as e:
            raise

# Klasse zur Verwaltung von Entfernungen in der Datenbank
class Distance(DatabaseEntity):
    def insert(self, distance, unit):
        try:
            if not distance or not unit:
                raise ValueError("Both distance and unit must have values.")
            self.db_cursor.execute('INSERT INTO distances (distance, unit) VALUES (?, ?)', (distance, unit))
            return self.db_cursor.lastrowid
        except sqlite3.Error as e:
            raise

    def remove(self, distance_id=None, distance_value=None):
        try:
            if distance_id is not None:
                self.db_cursor.execute('DELETE FROM distances WHERE id = ?', (distance_id,))
            elif distance_value is not None:
                self.db_cursor.execute('DELETE FROM distances WHERE distance = ?', (distance_value,))
            else:
                raise ValueError("Either distance_id or distance_value must be provided.")
        except sqlite3.Error as e:
            raise

    def get_all(self):
        try:
            self.db_cursor.execute('SELECT * FROM distances')
            return self.db_cursor.fetchall()
        except sqlite3.Error as e:
            raise
    
    def get_by_id(self, distance_id):
        try:
            self.db_cursor.execute('SELECT * FROM distances WHERE id = ?', (distance_id,))
            return self.db_cursor.fetchone()
        except sqlite3.Error as e:
            raise

# Klasse zur Verwaltung von Ergebnissen in der Datenbank
class Result(DatabaseEntity):
    def insert(self, weapon_id, ammunition_id, distance_id, result_value):
        try:
            if not all([weapon_id, ammunition_id, distance_id, result_value]):
                raise ValueError("All values (weapon_id, ammunition_id, distance_id, result_value) must be provided.")
            self.db_cursor.execute(
                'INSERT INTO results (weapon_id, ammunition_id, distance_id, result) VALUES (?, ?, ?, ?)',
                (weapon_id, ammunition_id, distance_id, result_value)
            )
            return self.db_cursor.lastrowid
        except sqlite3.Error as e:
            raise

    def remove(self, result_id):
        try:
            if not result_id:
                raise ValueError("Result ID must be provided.")
            self.db_cursor.execute('DELETE FROM results WHERE id = ?', (result_id,))
        except sqlite3.Error as e:
            raise

    def get_all(self):
        try:
            query = '''
            SELECT r.id, w.weapon, a.ammunition, d.distance, d.unit, r.result
            FROM results r
            JOIN weapons w ON r.weapon_id = w.id
            JOIN ammunition a ON r.ammunition_id = a.id
            JOIN distances d ON r.distance_id = d.id
            '''
            self.db_cursor.execute(query)
            return self.db_cursor.fetchall()
        except sqlite3.Error as e:
            raise
    
    def get_by_id(self, result_id):
        try:
            query = '''
            SELECT r.id, w.weapon, a.ammunition, d.distance, d.unit, r.result
            FROM results r
            JOIN weapons w ON r.weapon_id = w.id
            JOIN ammunition a ON r.ammunition_id = a.id
            JOIN distances d ON r.distance_id = d.id
            WHERE r.id = ?
            '''
            self.db_cursor.execute(query, (result_id,))
            return self.db_cursor.fetchone()
        except sqlite3.Error as e:
            raise
    
    def get_by_weapon_ammo_distance(self, weapon_id, ammo_id, distance_id):
        try:
            query = '''
            SELECT r.id, w.weapon, a.ammunition, d.distance, d.unit, r.result
            FROM results r
            JOIN weapons w ON r.weapon_id = w.id
            JOIN ammunition a ON r.ammunition_id = a.id
            JOIN distances d ON r.distance_id = d.id
            WHERE r.weapon_id = ? AND r.ammunition_id = ? AND r.distance_id = ?
            '''
            self.db_cursor.execute(query, (weapon_id, ammo_id, distance_id))
            return self.db_cursor.fetchone()
        except sqlite3.Error as e:
            raise

    def update(self, result_id, result_value):
        try:
            if not result_id or not result_value:
                raise ValueError("Result ID and value must be provided.")
            self.db_cursor.execute('UPDATE results SET result = ? WHERE id = ?', (result_value, result_id))
            return result_id
        except sqlite3.Error as e:
            raise

    def get_by_criteria(self, weapon_id=None, ammo_id=None, distance_id=None):
        try:
            query = '''
            SELECT r.id, w.weapon, a.ammunition, d.distance, d.unit, r.result, w.id, a.id, d.id
            FROM results r
            JOIN weapons w ON r.weapon_id = w.id
            JOIN ammunition a ON r.ammunition_id = a.id
            JOIN distances d ON r.distance_id = d.id
            WHERE 1=1
            '''
            params = []
            
            if weapon_id is not None:
                query += " AND w.id = ?"
                params.append(weapon_id)
            if ammo_id is not None:
                query += " AND a.id = ?"
                params.append(ammo_id)
            if distance_id is not None:
                query += " AND d.id = ?"
                params.append(distance_id)
                
            self.db_cursor.execute(query, params)
            return self.db_cursor.fetchall()
        except sqlite3.Error as e:
            raise
