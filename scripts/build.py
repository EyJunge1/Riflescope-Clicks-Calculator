#!/usr/bin/env python3
"""
🎯 RIFLESCOPE CALCULATOR - BUILD SCRIPT 🎯

Einfacher Build-Script für Windows EXE-Erstellung
Erstellt eine ausführbare .exe-Datei Ihrer Riflescope Calculator Anwendung

📋 VERWENDUNG:
    python scripts/build.py                    # Standard Build
    python scripts/build.py --clean            # Clean Build (lösche vorherige Builds)
    python scripts/build.py --portable         # Zusätzlich Portable ZIP erstellen
    python scripts/build.py --installer        # Zusätzlich NSIS Installer erstellen
    python scripts/build.py --all              # Alle Pakete erstellen

🎯 AUSGABE:
    dist/riflescope-calculator.exe             # Hauptprogramm
    dist/riflescope-calculator-portable.zip    # Portable Version (optional)
    dist/riflescope-calculator-setup.exe       # Installer (optional)
"""

import os
import sys
import subprocess
import platform
import argparse
import shutil
import time
import zipfile
from pathlib import Path
from datetime import datetime

class RiflescopeBuilder:
    """Einfacher Builder für Riflescope Calculator"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.src_dir = self.project_root / "src"
        self.run_file = self.project_root / "run.py"
        
        # App-Informationen
        self.app_name = "riflescope-calculator"
        self.app_display_name = "Riflescope Calculator"
        self.app_version = "1.0.0"
        self.exe_name = f"{self.app_name}.exe"
        
        # Build-Zeit
        self.build_start = time.time()
        
        print("🎯 Riflescope Calculator - Build Script")
        print("=" * 45)
        print(f"📅 Build Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🖥️  System: {platform.system()} {platform.release()}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📁 Projekt: {self.project_root.name}")
    
    def log(self, message: str, status: str = "INFO"):
        """Einfaches Logging"""
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "PROGRESS": "🔄"
        }
        icon = icons.get(status, "•")
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{icon} [{timestamp}] {message}")
    
    def check_requirements(self) -> bool:
        """Prüfe Systemvoraussetzungen"""
        self.log("Prüfe Systemvoraussetzungen", "PROGRESS")
        
        # Python Version
        if sys.version_info < (3, 7):
            self.log("Python 3.7+ erforderlich", "ERROR")
            return False
        
        # Prüfe wichtige Dateien
        if not self.run_file.exists():
            self.log("run.py nicht gefunden", "ERROR")
            return False
        
        if not self.src_dir.exists():
            self.log("src-Verzeichnis nicht gefunden", "ERROR")
            return False
        
        self.log("Systemvoraussetzungen OK", "SUCCESS")
        return True
    
    def install_pyinstaller(self) -> bool:
        """Installiere PyInstaller falls nicht vorhanden"""
        try:
            import PyInstaller
            self.log("PyInstaller bereits installiert", "SUCCESS")
            return True
        except ImportError:
            self.log("Installiere PyInstaller...", "PROGRESS")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "pyinstaller"
                ], check=True, capture_output=True)
                self.log("PyInstaller erfolgreich installiert", "SUCCESS")
                return True
            except subprocess.CalledProcessError:
                self.log("PyInstaller Installation fehlgeschlagen", "ERROR")
                return False
    
    def prepare_build_dirs(self):
        """Bereite Build-Verzeichnisse vor"""
        self.log("Bereite Build-Verzeichnisse vor", "PROGRESS")
        
        # Erstelle Verzeichnisse
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        self.log("Build-Verzeichnisse bereit", "SUCCESS")
    
    def get_icon_path(self) -> str:
        """Ermittle Icon-Pfad"""
        icon_paths = [
            self.project_root / "icons" / "target_icon.ico",
            self.project_root / "target_icon.ico"
        ]
        
        for icon_path in icon_paths:
            if icon_path.exists():
                self.log(f"Icon gefunden: {icon_path.name}", "SUCCESS")
                return str(icon_path)
        
        self.log("Kein Icon gefunden - verwende Standard", "WARNING")
        return ""
    
    def build_exe(self) -> bool:
        """Erstelle EXE mit PyInstaller"""
        self.log("Erstelle EXE mit PyInstaller", "PROGRESS")
        
        icon_path = self.get_icon_path()
        
        # PyInstaller Kommando
        cmd = [
            "pyinstaller",
            "--onefile",                    # Einzelne EXE-Datei
            "--windowed",                   # Kein Konsolen-Fenster
            "--name", self.app_name,        # Name der EXE
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
            "--specpath", str(self.build_dir),
            "--clean",                      # Clean Build
            "--noconfirm",                  # Überschreibe ohne Nachfrage
        ]
        
        # Icon hinzufügen falls vorhanden
        if icon_path:
            cmd.extend(["--icon", icon_path])
        
        # Zusätzliche Daten einbinden
        cmd.extend([
            "--add-data", f"{self.src_dir};src",
        ])
        
        # Icons-Verzeichnis falls vorhanden
        icons_dir = self.project_root / "icons"
        if icons_dir.exists():
            cmd.extend(["--add-data", f"{icons_dir};icons"])
        
        # Hauptdatei
        cmd.append(str(self.run_file))
        
        try:
            self.log("Starte PyInstaller...", "PROGRESS")
            start_time = time.time()
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 Minuten Timeout
            )
            
            build_time = time.time() - start_time
            
            if result.returncode == 0:
                self.log(f"EXE erfolgreich erstellt ({build_time:.1f}s)", "SUCCESS")
                return True
            else:
                self.log("PyInstaller fehlgeschlagen", "ERROR")
                if result.stderr:
                    print(f"\nFehler-Details:\n{result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log("PyInstaller Timeout (>5min)", "ERROR")
            return False
        except Exception as e:
            self.log(f"PyInstaller Fehler: {e}", "ERROR")
            return False
    
    def verify_exe(self) -> bool:
        """Prüfe erstellte EXE"""
        self.log("Prüfe erstellte EXE", "PROGRESS")
        
        exe_path = self.dist_dir / self.exe_name
        
        if not exe_path.exists():
            self.log(f"EXE nicht gefunden: {self.exe_name}", "ERROR")
            return False
        
        # Dateigröße prüfen
        size_bytes = exe_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        if size_bytes < 1024:  # Kleiner als 1KB
            self.log("EXE verdächtig klein (<1KB)", "ERROR")
            return False
        
        self.log(f"EXE OK ({size_mb:.1f}MB)", "SUCCESS")
        return True
    
    def create_portable_zip(self) -> bool:
        """Erstelle Portable ZIP"""
        self.log("Erstelle Portable ZIP", "PROGRESS")
        
        exe_path = self.dist_dir / self.exe_name
        zip_path = self.dist_dir / f"{self.app_name}-portable.zip"
        
        if not exe_path.exists():
            self.log("EXE für ZIP nicht gefunden", "ERROR")
            return False
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # EXE hinzufügen
                zipf.write(exe_path, self.exe_name)
                
                # README hinzufügen
                readme_content = f"""{self.app_display_name} - Portable Version

INSTALLATION:
1. Entpacken Sie diese ZIP-Datei in einen beliebigen Ordner
2. Starten Sie {self.exe_name}
3. Keine Installation erforderlich!

FEATURES:
- Vollständig portable
- Kann von USB-Stick ausgeführt werden
- Keine Registry-Einträge
- Alle Einstellungen werden lokal gespeichert

Version: {self.app_version}
Build-Datum: {datetime.now().strftime('%Y-%m-%d')}

Viel Erfolg beim Präzisionsschießen! 🎯
"""
                zipf.writestr("README.txt", readme_content)
            
            zip_size = zip_path.stat().st_size / (1024 * 1024)
            self.log(f"Portable ZIP erstellt ({zip_size:.1f}MB)", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"ZIP-Erstellung fehlgeschlagen: {e}", "ERROR")
            return False
    
    def create_nsis_installer(self) -> bool:
        """Erstelle NSIS Installer"""
        self.log("Erstelle NSIS Installer", "PROGRESS")
        
        # Prüfe ob NSIS verfügbar ist
        try:
            subprocess.run(['makensis', '/VERSION'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log("NSIS nicht verfügbar - überspringe Installer", "WARNING")
            return True
        
        # Verwende existierende installer.nsi falls vorhanden
        nsis_file = self.project_root / "installer" / "installer.nsi"
        
        if not nsis_file.exists():
            self.log("installer.nsi nicht gefunden - überspringe Installer", "WARNING")
            return True
        
        try:
            result = subprocess.run([
                'makensis',
                f'/DVERSION={self.app_version}',
                str(nsis_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("NSIS Installer erfolgreich erstellt", "SUCCESS")
                return True
            else:
                self.log(f"NSIS Fehler: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"NSIS Installer Fehler: {e}", "ERROR")
            return False
    
    def cleanup_build_files(self):
        """Bereinige Build-Dateien"""
        self.log("Bereinige Build-Dateien", "PROGRESS")
        
        # Lösche .spec Datei
        spec_files = list(self.build_dir.glob("*.spec"))
        for spec_file in spec_files:
            try:
                spec_file.unlink()
            except Exception:
                pass
        
        # Lösche __pycache__ Verzeichnisse
        for pycache in self.project_root.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache)
            except Exception:
                pass
        
        self.log("Build-Dateien bereinigt", "SUCCESS")
    
    def show_results(self):
        """Zeige Build-Ergebnisse"""
        build_time = time.time() - self.build_start
        
        print(f"\n" + "=" * 50)
        print(f"🎉 BUILD ABGESCHLOSSEN!")
        print("=" * 50)
        print(f"⏱️  Build Zeit: {build_time:.1f} Sekunden")
        print(f"📅 Abgeschlossen: {datetime.now().strftime('%H:%M:%S')}")
        
        # Zeige erstellte Dateien
        if self.dist_dir.exists():
            created_files = list(self.dist_dir.glob("*"))
            
            if created_files:
                print(f"\n📦 ERSTELLTE DATEIEN:")
                print("-" * 25)
                total_size = 0
                
                for file_path in sorted(created_files):
                    if file_path.is_file():
                        size = file_path.stat().st_size
                        total_size += size
                        
                        if size > 1024 * 1024:  # MB
                            size_str = f"{size / (1024 * 1024):.1f} MB"
                        else:  # KB
                            size_str = f"{size / 1024:.1f} KB"
                        
                        file_type = "🚀" if file_path.suffix == ".exe" else "📦" if file_path.suffix == ".zip" else "📄"
                        print(f"   {file_type} {file_path.name} ({size_str})")
                
                print(f"\n💾 Gesamt Größe: {total_size / (1024 * 1024):.1f} MB")
        
        print(f"\n📁 Ausgabe-Verzeichnis: {self.dist_dir}")
        print(f"\n🎯 {self.app_display_name} v{self.app_version} erfolgreich gebaut!")
        print(f"🚀 Bereit für Windows-Distribution!")
    
    def run_build(self, options: dict) -> bool:
        """Führe kompletten Build durch"""
        
        # 1. Voraussetzungen prüfen
        if not self.check_requirements():
            return False
        
        # 2. PyInstaller installieren
        if not self.install_pyinstaller():
            return False
        
        # 3. Build-Verzeichnisse vorbereiten
        if options.get('clean'):
            self.log("Bereinige vorherige Builds", "PROGRESS")
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
            if self.dist_dir.exists():
                shutil.rmtree(self.dist_dir)
        
        self.prepare_build_dirs()
        
        # 4. EXE erstellen
        if not self.build_exe():
            return False
        
        # 5. EXE prüfen
        if not self.verify_exe():
            return False
        
        # 6. Zusätzliche Pakete
        if options.get('portable') or options.get('all'):
            self.create_portable_zip()
        
        if options.get('installer') or options.get('all'):
            self.create_nsis_installer()
        
        # 7. Aufräumen
        self.cleanup_build_files()
        
        # 8. Ergebnisse anzeigen
        self.show_results()
        
        return True

def parse_arguments():
    """Parse Kommandozeilen-Argumente"""
    parser = argparse.ArgumentParser(
        description='🎯 Riflescope Calculator - Build Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 VERWENDUNGSBEISPIELE:

STANDARD BUILD:
  python scripts/build.py                    # Nur EXE erstellen

ERWEITERTE BUILDS:
  python scripts/build.py --portable         # EXE + Portable ZIP
  python scripts/build.py --installer        # EXE + NSIS Installer
  python scripts/build.py --all              # Alle Pakete erstellen

OPTIONEN:
  python scripts/build.py --clean            # Clean Build (empfohlen)
  python scripts/build.py --clean --all      # Clean + Alle Pakete
        """
    )
    
    parser.add_argument('--clean', action='store_true', 
                       help='🧹 Bereinige vorherige Builds')
    parser.add_argument('--portable', action='store_true', 
                       help='📦 Erstelle zusätzlich Portable ZIP')
    parser.add_argument('--installer', action='store_true', 
                       help='🔧 Erstelle zusätzlich NSIS Installer')
    parser.add_argument('--all', action='store_true', 
                       help='🎯 Erstelle alle Pakete (EXE + ZIP + Installer)')
    
    return parser.parse_args()

def main():
    """Hauptfunktion"""
    try:
        # Parse Argumente
        args = parse_arguments()
        
        # Initialize Builder
        builder = RiflescopeBuilder()
        
        # Build-Optionen
        build_options = {
            'clean': args.clean,
            'portable': args.portable,
            'installer': args.installer,
            'all': args.all
        }
        
        # Zeige Build-Konfiguration
        print(f"\n🔧 BUILD-KONFIGURATION:")
        print("-" * 25)
        print(f"   EXE: ✓")
        print(f"   Portable ZIP: {'✓' if (args.portable or args.all) else '✗'}")
        print(f"   NSIS Installer: {'✓' if (args.installer or args.all) else '✗'}")
        print(f"   Clean Build: {'✓' if args.clean else '✗'}")
        
        # Führe Build durch
        success = builder.run_build(build_options)
        
        # Return entsprechenden Exit Code
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Build durch Benutzer abgebrochen (Ctrl+C)")
        return 1
    except Exception as e:
        print(f"\n💥 Kritischer Build-Fehler: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())