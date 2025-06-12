#!/usr/bin/env python3
"""
Entry point for the Zielfernrohr-Klicksrechner application.
Run this file to start the application.

Optimiert für sowohl Python-Skript als auch Executable-Ausführung.
"""

import sys
import os

# Füge src-Verzeichnis zum Python-Pfad hinzu für korrekte Imports
if hasattr(sys, 'frozen'):
    # Als PyInstaller Executable ausgeführt
    import tempfile
    # Setze Umgebungsvariable für Executable-Modus
    os.environ['RIFLESCOPE_EXECUTABLE_MODE'] = '1'
    # Verwende temp-Verzeichnis für Daten
    app_data_dir = os.path.join(tempfile.gettempdir(), "RiflescopeCalculator")
    os.environ['RIFLESCOPE_DATA_DIR'] = app_data_dir
else:
    # Als Python-Skript ausgeführt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, 'src')
    if os.path.exists(src_dir) and src_dir not in sys.path:
        sys.path.insert(0, src_dir)

try:
    from src.main import main
    
    if __name__ == "__main__":
        main()
        
except Exception as e:
    print(f"Fehler beim Starten der Anwendung: {e}")
    
    # Für Executable: Warte auf Benutzereingabe
    if hasattr(sys, 'frozen'):
        print("\nDrücken Sie Enter zum Beenden...")
        try:
            input()
        except:
            pass
    
    sys.exit(1)
