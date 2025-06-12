# Import der benötigten Bibliotheken
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, Literal, Optional, Union

# Import der Anwendungseinstellungen
from ..config import AppSettings

# Definition eines benutzerdefinierten Typs für Log-Level mittels Literal
# Dies beschränkt die möglichen Werte auf die angegebenen Strings
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class Logger:
    """
    Eine allgemeine Logger-Klasse für die API.
    
    Diese Klasse bietet Funktionen für das Logging in verschiedenen Ebenen.
    Sie unterstützt sowohl Konsolen- als auch Datei-Logging mit anpassbarem Format.
    """
    
    def __init__(
        self, 
        name: str = "riflescope_calculator_logger", 
        log_level: LogLevel = "INFO",
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_file: Optional[str] = None,
        console_output: bool = True,
        propagate: bool = False  # Neuer Parameter, um Propagation zu steuern
    ):
        """
        Initialisiert den Logger mit den gewünschten Einstellungen.
        
        Args:
            name: Name des Loggers, wird in den Log-Einträgen angezeigt
            log_level: Schwellenwert für Logging (nur Nachrichten mit diesem Level oder höher werden protokolliert)
            log_format: Formatstring für die Log-Einträge mit Platzhaltern für verschiedene Werte
            log_file: Optional - Pfad zu einer Datei, in die geloggt werden soll
            console_output: Steuert, ob Logs auch in der Konsole ausgegeben werden
            propagate: Steuert, ob Logs an Eltern-Logger weitergeleitet werden sollen
        """
        # Erzeuge eine Logger-Instanz mit dem angegebenen Namen
        self.logger = logging.getLogger(name)
        
        # Propagation kontrollieren (wichtig um doppelte Log-Einträge zu vermeiden)
        self.logger.propagate = propagate
        
        # Konvertiere den Log-Level-String in die entsprechende Logging-Konstante
        # getattr holt das entsprechende Attribut aus dem logging-Modul (z.B. logging.INFO)
        level = getattr(logging, log_level)
        self.logger.setLevel(level)
        
        # Erstelle einen Formatter, der das Aussehen der Log-Nachrichten definiert
        formatter = logging.Formatter(log_format)
        
        # Entferne alle existierenden Handler vom Logger, um Mehrfachausgaben zu vermeiden
        # Dies ist wichtig, wenn der Logger neu konfiguriert wird
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Füge einen Handler für die Konsolenausgabe hinzu, wenn gewünscht
        if console_output:
            # StreamHandler mit stdout gibt die Nachrichten in der Konsole aus
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Füge einen Handler für die Dateiausgabe hinzu, wenn eine Datei angegeben wurde
        if log_file:
            # Stelle sicher, dass das übergeordnete Verzeichnis für die Log-Datei existiert
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            # FileHandler schreibt die Log-Einträge in die angegebene Datei
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Protokolliert eine DEBUG-Nachricht. 
        DEBUG-Nachrichten enthalten detaillierte Informationen für die Diagnose von Problemen.
        """
        self.logger.debug(message, extra=extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Protokolliert eine INFO-Nachricht.
        INFO-Nachrichten bestätigen, dass Dinge wie erwartet funktionieren.
        """
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None, exc_info: bool = False) -> None:
        """
        Protokolliert eine WARNING-Nachricht.
        WARNINGS weisen auf etwas hin, das möglicherweise ein Problem darstellt oder in Zukunft zu Fehlern führen könnte.
        """
        self.logger.warning(message, extra=extra, exc_info=exc_info)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None, exc_info: bool = False) -> None:
        """
        Protokolliert eine ERROR-Nachricht.
        ERROR-Nachrichten zeigen an, dass etwas nicht funktioniert hat und behoben werden sollte.
        """
        self.logger.error(message, extra=extra, exc_info=exc_info)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None, exc_info: bool = False) -> None:
        """
        Protokolliert eine CRITICAL-Nachricht.
        CRITICAL-Nachrichten zeigen sehr schwerwiegende Fehler an, die möglicherweise zum Programmabsturz führen.
        """
        self.logger.critical(message, extra=extra, exc_info=exc_info)
    
    def exception(self, message: str, exc_info=True, extra: Optional[Dict[str, Any]] = None) -> None:
        """
        Protokolliert eine Exception mit Stacktrace.
        Verwendet man am besten innerhalb eines except-Blocks, um Details zur aufgetretenen Exception zu loggen.
        
        Args:
            message: Die zu protokollierende Nachricht
            exc_info: Wenn True, wird der aktuelle Exception-Stack hinzugefügt
            extra: Optionales Dictionary mit zusätzlichen Informationen
        """
        self.logger.exception(message, exc_info=exc_info, extra=extra)
    
    def log_request(self, method: str, path: str, status_code: int, duration_ms: float) -> None:
        """
        Protokolliert einen API-Request mit Details wie Methode, Pfad, Statuscode und Verarbeitungsdauer.
        Besonders nützlich für das Monitoring und die Analyse von API-Aufrufen.
        
        Args:
            method: HTTP-Methode des Requests (GET, POST, PUT, DELETE, etc.)
            path: Der aufgerufene API-Pfad/Endpunkt
            status_code: Der HTTP-Statuscode der Antwort
            duration_ms: Die Verarbeitungsdauer des Requests in Millisekunden
        """
        self.info(
            f"Request: {method} {path} - Status: {status_code} - Duration: {duration_ms:.2f}ms",
            extra={"method": method, "path": path, "status_code": status_code, "duration_ms": duration_ms}
        )
    
    def log_error(self, error: Exception, request_info: Optional[Dict[str, Any]] = None) -> None:
        """
        Protokolliert einen Fehler zusammen mit zusätzlichen Informationen über den Request.
        Dies hilft bei der Fehleranalyse, indem der Kontext des Fehlers besser dokumentiert wird.
        
        Args:
            error: Die aufgetretene Exception, die geloggt werden soll
            request_info: Optionales Dictionary mit zusätzlichen Informationen über den Request
        """
        # Erstelle ein Dictionary mit dem Typ des Fehlers
        extra = {"error_type": type(error).__name__}
        
        # Füge Request-Informationen hinzu, wenn vorhanden
        if request_info:
            extra.update(request_info)
        
        # Logge die Fehlermeldung mit Stacktrace und den zusätzlichen Informationen
        self.exception(f"Error: {str(error)}", extra=extra)
    
    def set_level(self, level: LogLevel) -> None:
        """
        Ändert das Log-Level des Loggers zur Laufzeit.
        Dies erlaubt eine dynamische Anpassung der Logging-Granularität ohne Neustart.
        
        Args:
            level: Das neue Log-Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger.setLevel(getattr(logging, level))
    
    def add_file_handler(self, log_file: str, level: Optional[LogLevel] = None) -> None:
        """
        Fügt einen zusätzlichen File-Handler zum Logger hinzu.
        Dies ermöglicht das Logging in mehrere Dateien gleichzeitig, z.B. allgemeine Logs und Error-Logs.
        
        Args:
            log_file: Pfad zur Log-Datei, in die geschrieben werden soll
            level: Optionales spezifisches Log-Level für diesen Handler (nur Nachrichten mit diesem Level werden geschrieben)
        """
        # Stelle sicher, dass das Verzeichnis für die Log-Datei existiert
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Erstelle einen neuen FileHandler für die angegebene Log-Datei
        file_handler = logging.FileHandler(log_file)
        
        # Verwende einen Standard-Formatter für diesen Handler
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        
        if level:
            file_handler.setLevel(getattr(logging, level))
            
        self.logger.addHandler(file_handler)
    
    def get_logger_instance(self) -> logging.Logger:
        """
        Gibt die zugrunde liegende Logger-Instanz zurück.
        Dies ist nützlich, wenn man direkten Zugriff auf das Logger-Objekt benötigt,
        z.B. zur Integration mit anderen Bibliotheken, die einen Standard-Logger erwarten.
        
        Returns:
            logging.Logger: Die zugrunde liegende Logger-Instanz von Python's logging-Modul
        """
        return self.logger
    
    def create_child_logger(self, suffix: str) -> 'Logger':
        """
        Erstellt einen abgeleiteten Logger mit einem hierarchischen Namen.
        Dies ermöglicht eine feingranulare Kontrolle des Loggings nach Modulen oder Komponenten,
        während die Konfiguration des Eltern-Loggers übernommen wird.
        
        Args:
            suffix: Suffix, der an den Namen des Eltern-Loggers angehängt wird
            
        Returns:
            Logger: Ein neuer Logger-Instanz mit dem Namen parent.suffix
        """
        child_name = f"{self.logger.name}.{suffix}"
        
        child_logger = Logger(
            name=child_name,
            propagate=True,
            console_output=False,
            log_file=None
        )
        
        return child_logger


# Verbesserte Logger-Initialisierung
def setup_application_logging():
    """Setup centralized application logging with enhanced error handling for executables"""
    try:
        # Erkenne Executable-Umgebung
        is_executable = getattr(sys, 'frozen', False)
        
        if is_executable:
            # Für Executable: Verwende temporäres Verzeichnis
            import tempfile
            log_dir = os.path.join(tempfile.gettempdir(), "RiflescopeCalculator", "logs")
        else:
            # Für normale Python-Ausführung
            log_dir = AppSettings.get_logs_dir()
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Main application log
        app_log_path = os.path.join(log_dir, "application.log")
        
        # Error-specific log
        error_log_path = os.path.join(log_dir, "errors.log")
        
        # Debug log (when enabled)
        debug_log_path = os.path.join(log_dir, "debug.log")
        
        return app_log_path, error_log_path, debug_log_path
    except (OSError, PermissionError) as e:
        # Fallback to current directory if logs directory creation fails
        fallback_dir = os.getcwd()
        print(f"Warning: Could not create logs directory, using fallback: {fallback_dir}")
        return (
            os.path.join(fallback_dir, "application.log"),
            os.path.join(fallback_dir, "errors.log"),
            os.path.join(fallback_dir, "debug.log")
        )

# Setup logging paths with error handling
try:
    app_log_path, error_log_path, debug_log_path = setup_application_logging()
except Exception as e:
    # Ultimate fallback
    app_log_path = "application.log"
    error_log_path = "errors.log"
    debug_log_path = "debug.log"
    print(f"Critical logging setup error: {e}")

# Verbesserte Logger-Initialisierung mit Executable-Unterstützung
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    main_logger = Logger(
        name="riflescope_calculator",
        log_level="INFO",
        log_file=app_log_path,
        propagate=False
    )

    # Add error-specific handler with error handling
    try:
        main_logger.add_file_handler(error_log_path, "ERROR")
    except Exception as e:
        print(f"Warning: Could not add error file handler: {e}")

    main_logger.info(f"Riflescope Clicks Calculator Logger initialisiert")
    main_logger.info(f"Application logs: {app_log_path}")
    main_logger.info(f"Error logs: {error_log_path}")

except Exception as e:
    # Fallback to basic console logging
    main_logger = Logger(
        name="riflescope_calculator",
        log_level="INFO",
        console_output=True,
        propagate=False
    )
    main_logger.error(f"Failed to initialize file logging: {e}")

# Child-Logger für verschiedene Module
calc_logger = main_logger.create_child_logger("calculator")
db_logger = main_logger.create_child_logger("database")
gui_logger = main_logger.create_child_logger("gui")
config_logger = main_logger.create_child_logger("config")
utils_logger = main_logger.create_child_logger("utils")
models_logger = main_logger.create_child_logger("models")

# Spezifische Child-Logger für Datenbankkomponenten
db_connection_logger = db_logger.create_child_logger("connection")
db_manager_logger = db_logger.create_child_logger("manager")
db_entities_logger = db_logger.create_child_logger("entities")
db_initialization_logger = db_logger.create_child_logger("initialization")

# Spezifische Child-Logger für GUI-Komponenten
gui_main_logger = gui_logger.create_child_logger("main_window")
gui_settings_logger = gui_logger.create_child_logger("settings_window")
gui_components_logger = gui_logger.create_child_logger("components")

# Spezifische Child-Logger für Utils-Komponenten
utils_calc_logger = utils_logger.create_child_logger("calculator")
utils_validators_logger = utils_logger.create_child_logger("validators")

# Spezifische Child-Logger für Models
models_weapon_logger = models_logger.create_child_logger("weapon")
models_ammunition_logger = models_logger.create_child_logger("ammunition")
models_distance_logger = models_logger.create_child_logger("distance")
models_result_logger = models_logger.create_child_logger("result")

# Neue Child-Logger für bessere Kategorisierung
startup_logger = main_logger.create_child_logger("startup")
directory_logger = main_logger.create_child_logger("directory_setup")
sample_data_logger = main_logger.create_child_logger("sample_data")
error_recovery_logger = main_logger.create_child_logger("error_recovery")

# Debug-Konfiguration hinzufügen
def enable_debug_logging():
    """Enable debug logging for all components with error handling"""
    try:
        import logging
        
        # Set all loggers to DEBUG level
        logging.getLogger("riflescope_calculator").setLevel(logging.DEBUG)
        
        # Add console handler if not present
        root_logger = logging.getLogger("riflescope_calculator")
        
        # Check if console handler exists
        has_console = any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers)
        
        if not has_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # Add debug file handler with error handling
        try:
            main_logger.add_file_handler(debug_log_path, "DEBUG")
            main_logger.info("Debug-Modus aktiviert")
        except Exception as e:
            main_logger.warning(f"Could not add debug file handler: {e}")
    
    except Exception as e:
        print(f"Error enabling debug logging: {e}")

# Debug mode detection
if os.getenv('DEBUG', '').lower() in ('1', 'true', 'yes'):
    enable_debug_logging()