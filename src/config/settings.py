import os
import sys

class AppSettings:
    # Application information
    APP_NAME = "Zielfernrohr-Klicksrechner"
    APP_TITLE = "Zielfernrohr-Klicksrechner - Präzisionsschießen-Tool"
    
    # Window settings
    MAIN_WINDOW_SIZE = "420x650"
    SETTINGS_WINDOW_SIZE = "800x650"
    
    # Database settings
    DEFAULT_DB_NAME = "riflescope_clicks.db"
    
    # Default distances to add on first run
    DEFAULT_DISTANCES = [
        ("10", "m"), ("15", "m"), ("25", "m"), 
        ("50", "m"), ("100", "m"), ("200", "m"), ("300", "m")
    ]
    
    # Style settings
    BACKGROUND_COLOR = '#f0f0f0'
    ACCENT_COLOR = '#3c7eb7'
    BUTTON_COLOR = '#4a8bc2'
    
    @staticmethod
    def get_app_dir():
        return os.path.dirname(os.path.abspath(__file__))
    
    @staticmethod
    def get_project_root():
        """Get the project root directory (cross-platform compatible)"""
        # Wenn als Executable läuft, verwende Executable-Verzeichnis
        if getattr(sys, 'frozen', False):
            # PyInstaller Executable
            return os.path.dirname(sys.executable)
        else:
            # Development Mode - von src/config zurück zum root
            app_dir = AppSettings.get_app_dir()
            return os.path.abspath(os.path.join(app_dir, '..', '..'))
    
    @staticmethod
    def get_db_dir():
        project_root = AppSettings.get_project_root()
        return os.path.join(project_root, 'database')
    
    @staticmethod
    def get_icons_dir():
        project_root = AppSettings.get_project_root()
        return os.path.join(project_root, 'icons')
    
    @staticmethod
    def get_logs_dir():
        """Get the logs directory"""
        project_root = AppSettings.get_project_root()
        return os.path.join(project_root, 'logs')
    
    @staticmethod
    def get_db_path():
        return os.path.join(AppSettings.get_db_dir(), AppSettings.DEFAULT_DB_NAME)
