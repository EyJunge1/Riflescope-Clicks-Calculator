import os
import sqlite3
import sys
from tkinter import messagebox
import tkinter as tk
import time

from .config import AppSettings
from .database import DatabaseManager
from .gui import MainWindow
from .core import (
    main_logger, 
    startup_logger, 
    directory_logger, 
    db_initialization_logger,
    sample_data_logger,
    error_recovery_logger
)
from .models import WeaponModel, AmmunitionModel, DistanceModel, ResultModel

def setup_directories():
    """Setup required directories with enhanced error handling and logging"""
    directory_logger.info("Starte Verzeichnis-Setup")
    
    try:
        directories = [
            (AppSettings.get_db_dir(), "Datenbankverzeichnis"),
            (AppSettings.get_icons_dir(), "Icons-Verzeichnis"),
            (AppSettings.get_logs_dir(), "Logs-Verzeichnis")
        ]
    except Exception as e:
        directory_logger.error(f"Fehler beim Ermitteln der Verzeichnispfade: {e}")
        messagebox.showerror("Konfigurationsfehler", 
            f"Fehler beim Ermitteln der Verzeichnispfade: {str(e)}")
        return False
    
    failed_directories = []
    
    for dir_path, description in directories:
        try:
            directory_logger.debug(f"Erstelle/Überprüfe {description}: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            directory_logger.info(f"{description} erfolgreich erstellt/überprüft: {dir_path}")
            
        except PermissionError as e:
            error_msg = f"Berechtigungsfehler beim Erstellen des {description}: {e}"
            directory_logger.error(error_msg)
            failed_directories.append((description, "Berechtigung"))
            messagebox.showerror("Berechtigungsfehler", 
                f"Kann das {description} nicht erstellen.\n"
                f"Pfad: {dir_path}\n"
                f"Versuchen Sie, als Administrator auszuführen.")
            
        except FileExistsError as e:
            error_msg = f"Datei mit gleichem Namen existiert bereits für {description}: {e}"
            directory_logger.error(error_msg)
            failed_directories.append((description, "Dateikonflikt"))
            messagebox.showerror("Dateikonflikt", 
                f"Eine Datei mit dem Namen des {description} existiert bereits.\n"
                f"Pfad: {dir_path}")
            
        except OSError as e:
            error_msg = f"OS-Fehler beim Erstellen des {description}: {e}"
            directory_logger.error(error_msg)
            failed_directories.append((description, "OS-Fehler"))
            messagebox.showerror("Verzeichnisfehler", 
                f"Fehler beim Erstellen des {description}:\n"
                f"Pfad: {dir_path}\n"
                f"Fehler: {str(e)}")
        
        except Exception as e:
            error_msg = f"Unerwarteter Fehler beim Erstellen des {description}: {e}"
            directory_logger.error(error_msg, exc_info=True)
            failed_directories.append((description, "Unbekannt"))
            messagebox.showerror("Unerwarteter Fehler", 
                f"Unerwarteter Fehler beim Erstellen des {description}:\n"
                f"Pfad: {dir_path}\n"
                f"Fehler: {str(e)}")
    
    if failed_directories:
        directory_logger.warning(f"Fehlgeschlagene Verzeichnisse: {failed_directories}")
        error_recovery_logger.info("Versuche Fallback-Strategien für fehlgeschlagene Verzeichnisse")
        # Hier könnten Fallback-Strategien implementiert werden
        return False
    
    directory_logger.info("Verzeichnis-Setup erfolgreich abgeschlossen")
    return True

def initialize_database():
    """Initialize database with comprehensive error handling and logging"""
    db_initialization_logger.info("Starte Datenbank-Initialisierung")
    
    try:
        db_path = AppSettings.get_db_path()
        db_initialization_logger.info(f"Datenbankpfad: {db_path}")
        
        # Check if database directory exists
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            db_initialization_logger.warning(f"Datenbankverzeichnis existiert nicht: {db_dir}")
            try:
                os.makedirs(db_dir, exist_ok=True)
                db_initialization_logger.info(f"Datenbankverzeichnis erstellt: {db_dir}")
            except Exception as e:
                db_initialization_logger.error(f"Fehler beim Erstellen des Datenbankverzeichnisses: {e}")
                messagebox.showerror("Datenbankverzeichnis-Fehler", 
                    f"Konnte Datenbankverzeichnis nicht erstellen:\n{str(e)}")
                return None
        
    except Exception as e:
        db_initialization_logger.error(f"Fehler beim Ermitteln des Datenbankpfads: {e}")
        messagebox.showerror("Konfigurationsfehler", 
            f"Fehler beim Ermitteln des Datenbankpfads: {str(e)}")
        return None
    
    try:
        db_manager = DatabaseManager(db_path)
        db_initialization_logger.info("Datenbankmanager erfolgreich erstellt")
        
    except ImportError as e:
        db_initialization_logger.error(f"Fehler beim Importieren von Datenbankmodulen: {e}")
        messagebox.showerror("Modulimport-Fehler", 
            f"Erforderliche Datenbankmodule fehlen: {str(e)}")
        return None
        
    except TypeError as e:
        db_initialization_logger.error(f"Falscher Typ für Datenbankpfad: {e}")
        messagebox.showerror("Konfigurationsfehler", 
            f"Ungültiger Datenbankpfad: {str(e)}")
        return None
        
    except Exception as e:
        db_initialization_logger.error(f"Unerwarteter Fehler beim Erstellen des Datenbankmanagers: {e}", exc_info=True)
        messagebox.showerror("Datenbankmanager-Fehler", 
            f"Unerwarteter Fehler beim Erstellen des Datenbankmanagers:\n{str(e)}")
        return None
    
    try:
        db_manager.initialize_database()
        db_initialization_logger.info("Datenbank erfolgreich initialisiert")
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e).lower():
            db_initialization_logger.error(f"Datenbank ist gesperrt: {e}")
            messagebox.showerror("Datenbankzugriff gesperrt", 
                f"Die Datenbank wird von einem anderen Prozess verwendet.\n"
                f"Schließen Sie andere Instanzen der Anwendung und versuchen Sie es erneut.")
        elif "disk" in str(e).lower() or "space" in str(e).lower():
            db_initialization_logger.error(f"Speicherplatzproblem: {e}")
            messagebox.showerror("Speicherplatz-Fehler", 
                f"Nicht genügend Speicherplatz für die Datenbank:\n{str(e)}")
        else:
            db_initialization_logger.error(f"Datenbankzugriffsfehler: {e}")
            messagebox.showerror("Datenbankzugriffsfehler", 
                f"Fehler beim Zugriff auf die Datenbank:\n{str(e)}")
        return None
        
    except sqlite3.DatabaseError as e:
        db_initialization_logger.error(f"Datenbankdatei könnte beschädigt sein: {e}")
        response = messagebox.askyesno("Datenbankstruktur-Fehler", 
            f"Die Datenbankdatei könnte beschädigt sein:\n{str(e)}\n\n"
            f"Möchten Sie versuchen, eine neue Datenbank zu erstellen?\n"
            f"(Die alte Datei wird umbenannt)")
        
        if response:
            try:
                backup_path = f"{db_path}.backup_{int(time.time())}"
                os.rename(db_path, backup_path)
                db_initialization_logger.info(f"Beschädigte Datenbank gesichert als: {backup_path}")
                return initialize_database()  # Recursive call for new database
            except Exception as backup_error:
                db_initialization_logger.error(f"Fehler beim Sichern der beschädigten Datenbank: {backup_error}")
                messagebox.showerror("Backup-Fehler", 
                    f"Konnte beschädigte Datenbank nicht sichern: {str(backup_error)}")
        return None
        
    except sqlite3.Error as e:
        db_initialization_logger.error(f"SQLite-Fehler bei der Initialisierung: {e}")
        messagebox.showerror("Datenbankfehler", 
            f"SQLite-Fehler bei der Initialisierung:\n{str(e)}")
        return None
        
    except Exception as e:
        db_initialization_logger.error(f"Unerwarteter Fehler bei der Datenbankinitialisierung: {e}", exc_info=True)
        messagebox.showerror("Unerwarteter Datenbankfehler", 
            f"Unerwarteter Fehler bei der Datenbankinitialisierung:\n{str(e)}")
        return None
    
    db_initialization_logger.info("Datenbank-Initialisierung erfolgreich abgeschlossen")
    return db_manager

def initialize_sample_data(db_manager):
    """Initialize sample data with enhanced error handling and logging"""
    sample_data_logger.info("Starte Initialisierung der Beispieldaten")
    
    try:
        # Teste Model-Import und -Verwendung
        sample_data_logger.debug("Teste Model-Klassen...")
        test_weapon = WeaponModel(id=1, weapon="Test", caliber=".308")
        sample_data_logger.debug(f"WeaponModel Test: {test_weapon}")
        
        distances = db_manager.get_distances()
        sample_data_logger.debug(f"Vorhandene Entfernungen gefunden: {len(distances) if distances else 0}")
        
        if not distances:
            sample_data_logger.info("Datenbank ist leer. Füge initiale Entfernungsdaten hinzu...")
            
            success_count = 0
            error_count = 0
            
            for distance, unit in AppSettings.DEFAULT_DISTANCES:
                try:
                    db_manager.add_distance(distance, unit)
                    sample_data_logger.debug(f"Entfernung erfolgreich hinzugefügt: {distance} {unit}")
                    success_count += 1
                    
                except sqlite3.IntegrityError as e:
                    sample_data_logger.warning(f"Entfernung bereits vorhanden: {distance} {unit} - {e}")
                    # This is not necessarily an error, just skip
                    
                except sqlite3.Error as e:
                    sample_data_logger.error(f"Datenbankfehler beim Hinzufügen der Entfernung {distance} {unit}: {e}")
                    error_count += 1
                    
                except ValueError as e:
                    sample_data_logger.error(f"Ungültiger Wert für Entfernung {distance} {unit}: {e}")
                    error_count += 1
                    
                except Exception as e:
                    sample_data_logger.error(f"Unerwarteter Fehler beim Hinzufügen der Entfernung {distance} {unit}: {e}")
                    error_count += 1
            
            sample_data_logger.info(f"Beispieldaten-Initialisierung abgeschlossen: {success_count} erfolgreich, {error_count} Fehler")
            
            if error_count > 0 and success_count == 0:
                messagebox.showwarning("Beispieldaten-Warnung", 
                    f"Konnte keine Beispieldaten hinzufügen. Sie müssen Entfernungen manuell hinzufügen.")
        else:
            sample_data_logger.info(f"Datenbank enthält bereits {len(distances)} Entfernungen")
            # Teste Model-Konvertierung mit erster Entfernung
            if distances:
                first_distance = distances[0]
                distance_model = DistanceModel(id=first_distance[0], distance=first_distance[1], unit=first_distance[2])
                sample_data_logger.debug(f"Beispiel-Entfernung (Model): {distance_model}")
    
    except sqlite3.DatabaseError as e:
        sample_data_logger.warning(f"Datenbankfehler bei der Überprüfung vorhandener Daten: {e}")
        messagebox.showwarning("Datenbankwarnung", 
            f"Konnte vorhandene Daten nicht überprüfen: {str(e)}\n"
            "Die Anwendung wird fortgesetzt, aber Sie müssen möglicherweise Entfernungen manuell hinzufügen.")
    
    except Exception as e:
        sample_data_logger.warning(f"Unerwarteter Fehler bei der Initialisierung der Beispieldaten: {e}", exc_info=True)
        messagebox.showwarning("Dateninitialisierungs-Warnung", 
            f"Unerwarteter Fehler bei der Initialisierung der Beispieldaten: {str(e)}\n"
            "Die Anwendung wird fortgesetzt, aber Sie müssen möglicherweise Entfernungen manuell hinzufügen.")

def main():
    """Hauptfunktion mit verbessertem Error-Handling und Logging für Cross-Platform Executable-Builds"""
    # Frühe Initialisierung für Cross-Platform Executable-Umgebung
    try:
        # Erkennung ob als Executable ausgeführt (Windows/macOS/Linux)
        if getattr(sys, 'frozen', False):
            # Als PyInstaller Executable ausgeführt (Cross-Platform)
            import tempfile
            app_data_dir = os.path.join(tempfile.gettempdir(), "RiflescopeCalculator")
            os.environ['RIFLESCOPE_DATA_DIR'] = app_data_dir
            startup_logger.info("Ausführung als Cross-Platform Executable erkannt")
        else:
            startup_logger.info("Ausführung als Python-Skript erkannt")
    except Exception as e:
        print(f"Warnung bei Executable-Erkennung: {e}")
    
    startup_logger.info("=== Starte Zielfernrohr-Klicksrechner ===")
    startup_logger.info(f"Python-Version: {sys.version}")
    startup_logger.info(f"Arbeitsverzeichnis: {os.getcwd()}")
    
    try:
        # Setup directories with enhanced error handling
        startup_logger.info("Phase 1: Verzeichnis-Setup")
        if not setup_directories():
            startup_logger.error("Verzeichnis-Setup fehlgeschlagen")
            # Für Cross-Platform Executable: Versuche mit Fallback-Konfiguration
            if getattr(sys, 'frozen', False):
                startup_logger.info("Versuche Cross-Platform Executable-Fallback-Konfiguration")
                try:
                    from .config import AppSettings
                    AppSettings.use_executable_mode()
                    if not setup_directories():
                        startup_logger.error("Auch Fallback-Konfiguration fehlgeschlagen")
                        return
                except Exception as fallback_error:
                    startup_logger.error(f"Fallback-Konfiguration fehlgeschlagen: {fallback_error}")
                    return
            else:
                error_recovery_logger.info("Versuche Anwendung mit Fallback-Konfiguration zu starten")
                return
        
        # Initialize database with enhanced error handling
        startup_logger.info("Phase 2: Datenbank-Initialisierung")
        db_manager = initialize_database()
        if db_manager is None:
            startup_logger.error("Datenbank-Initialisierung fehlgeschlagen")
            return
        
        # Initialize sample data with enhanced error handling
        startup_logger.info("Phase 3: Beispieldaten-Initialisierung")
        initialize_sample_data(db_manager)
        
        # Start GUI application with enhanced error handling
        startup_logger.info("Phase 4: GUI-Initialisierung")
        try:
            app = MainWindow(db_manager)
            startup_logger.info("Hauptfenster erfolgreich erstellt")
            
            startup_logger.info("Starte Anwendungsschleife")
            app.run()
            startup_logger.info("Anwendung normal beendet")
            
        except tk.TclError as e:
            startup_logger.error(f"Tkinter-Fehler beim Initialisieren des Anwendungsfensters: {e}")
            messagebox.showerror("GUI-Initialisierungsfehler", 
                f"Fehler beim Initialisieren der grafischen Benutzeroberfläche:\n{str(e)}\n\n"
                f"Mögliche Ursachen:\n"
                f"- Keine Anzeigeumgebung verfügbar\n"
                f"- Beschädigte GUI-Bibliotheken")
                
        except ImportError as e:
            startup_logger.error(f"Import-Fehler für GUI-Module: {e}")
            messagebox.showerror("Modul-Import-Fehler", 
                f"Erforderliche GUI-Module fehlen:\n{str(e)}")
                
        except Exception as e:
            startup_logger.error(f"Unerwarteter Fehler bei der GUI-Initialisierung: {e}", exc_info=True)
            messagebox.showerror("GUI-Fehler", 
                f"Unerwarteter Fehler bei der GUI-Initialisierung:\n{str(e)}")
    
    except KeyboardInterrupt:
        startup_logger.info("Anwendung durch Benutzer unterbrochen (Ctrl+C)")
        
    except SystemExit as e:
        startup_logger.info(f"Anwendung beendet mit Exit-Code: {e.code}")
        
    except Exception as e:
        startup_logger.critical(f"Kritischer Fehler beim Starten der Anwendung: {e}", exc_info=True)
        try:
            # Für Executable: Zeige Fehler in Console falls GUI nicht verfügbar
            if getattr(sys, 'frozen', False):
                print(f"\nKRITISCHER FEHLER: {e}")
                print("Drücken Sie Enter zum Beenden...")
                try:
                    input()
                except:
                    pass
            else:
                messagebox.showerror("Kritischer Anwendungsfehler", 
                    f"Ein kritischer Fehler ist beim Starten aufgetreten:\n{str(e)}\n\n"
                    f"Bitte überprüfen Sie die Logs für weitere Details.")
        except:
            # If even messagebox fails, print to console
            print(f"KRITISCHER FEHLER: {e}")
    
    finally:
        startup_logger.info("=== Anwendungsstart-Prozess beendet ===")

# Startet die Anwendung, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        sys.exit(1)
