#!/usr/bin/env python3
"""
🎯 RIFLESCOPE CALCULATOR - UNIVERSAL BUILD ORCHESTRATOR 🎯

Zentraler Build-Startpunkt für alle Plattformen
Optimiert für Windows mit vollständiger Installer-Unterstützung

🚀 VERFÜGBARE BUILDS:
- 🪟 Windows → .exe + .zip + Installer (NSIS/MSI)
- 🍎 macOS → .app + .dmg (geplant)
- 🐧 Linux → Binary + .deb/.rpm (geplant)

📋 QUICK START - WINDOWS:
    python scripts/build.py --windows                       # Standard: .exe + .zip
    python scripts/build.py --windows --all                 # Alle Windows Pakete
    python scripts/build.py --windows --installer           # .exe + .zip + NSIS Installer
    python scripts/build.py --windows --portable-only       # Nur .zip (schnell)
    python scripts/build.py --windows --exe-only            # Nur .exe (sehr schnell)

🎯 EMPFOHLENE BEFEHLE:
    python scripts/build.py --windows --all                 # Vollständige Distribution
    python scripts/build.py --windows                       # Standard Build (schnell)
"""

import os
import sys
import subprocess
import platform
import argparse
import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class BuildOrchestrator:
    """Zentraler Build Orchestrator für alle Plattformen"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"
        self.dist_dir = self.project_root / "dist"
        
        # Platform Info
        self.current_platform = platform.system().lower()
        self.is_windows = self.current_platform == 'windows'
        self.is_macos = self.current_platform == 'darwin'
        self.is_linux = self.current_platform == 'linux'
        
        # App Info
        self.APP_NAME = "Riflescope Calculator"
        self.APP_VERSION = "1.0.0"
        
        # Build Start Time
        self.build_start = time.time()
        
        print("🎯 RIFLESCOPE CALCULATOR - BUILD ORCHESTRATOR")
        print("=" * 55)
        print(f"📅 Build Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🖥️  System: {self.get_platform_emoji()} {platform.system()} {platform.release()}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"📁 Projekt: {self.project_root.name}")
        
        # Ensure dist directory exists
        self.dist_dir.mkdir(exist_ok=True)
    
    def get_platform_emoji(self):
        """Platform Emoji für bessere Übersicht"""
        emojis = {
            'windows': '🪟',
            'darwin': '🍎', 
            'linux': '🐧'
        }
        return emojis.get(self.current_platform, '💻')
    
    def print_available_builds(self):
        """Zeige verfügbare Build-Optionen"""
        print(f"\n🚀 VERFÜGBARE BUILDS:")
        print("-" * 25)
        
        if self.is_windows:
            print("✅ Windows Build (Nativ)")
            print("   • .exe Executable")
            print("   • .zip Portable Package") 
            print("   • NSIS Installer (.exe)")
            print("   • MSI Installer (experimentell)")
        else:
            print("🔄 Windows Build (Cross-Platform)")
            print("   • .exe Executable")
            print("   • .zip Portable Package")
            print("   • Installer (eingeschränkt)")
            print()
            print("💡 FERTIGE WINDOWS BUILDS VERFÜGBAR:")
            print("   📦 Setup: https://github.com/EyJunge1/Riflescope-Clicks-Calculator/releases/download/windows/riflescope-calculator-setup-x64.exe")
            print("   🚀 Executable: https://github.com/EyJunge1/Riflescope-Clicks-Calculator/releases/download/windows/riflescope-calculator.exe")
            print("   📁 Portable ZIP: https://github.com/EyJunge1/Riflescope-Clicks-Calculator/releases/download/windows/riflescope-calculator-portable-x64.zip")
        
        if not self.is_macos:
            print("🔮 macOS Build (Bald verfügbar)")
            print("   • Support für andere Betriebssysteme wird bald hinzugefügt!")
        else:
            print("🔮 macOS Build (In Entwicklung)")
        
        if not self.is_linux:
            print("🔮 Linux Build (Bald verfügbar)")
            print("   • Support für andere Betriebssysteme wird bald hinzugefügt!")
        else:
            print("🔮 Linux Build (In Entwicklung)")
        
        if not self.is_windows:
            print(f"\n⚠️  Aktuell werden nur Windows-Builds vollständig unterstützt.")
            print(f"   Andere Betriebssysteme (macOS, Linux) werden bald unterstützt!")
            print(f"   Erkanntes System: {platform.system()} {platform.release()}")
    
    def check_windows_builder(self) -> bool:
        """Prüfe Windows Build Script"""
        windows_script = self.scripts_dir / "build_windows.py"
        
        if not windows_script.exists():
            print(f"\n❌ Windows Build Script nicht gefunden!")
            print(f"   Erwartet: {windows_script}")
            return False
        
        print(f"\n✅ Windows Builder verfügbar: {windows_script.name}")
        return True
    
    def show_build_recommendations(self):
        """Zeige Build-Empfehlungen basierend auf System"""
        print(f"\n💡 BUILD-EMPFEHLUNGEN:")
        print("-" * 25)
        
        if self.is_windows:
            print("🎯 OPTIMAL (Windows Nativ):")
            print("   python scripts/build.py --windows --all")
            print("   → Erstellt: .exe + .zip + NSIS Installer")
            print()
            print("⚡ SCHNELL:")
            print("   python scripts/build.py --windows")
            print("   → Erstellt: .exe + .zip")
            print()
            print("🚀 NUR EXECUTABLE:")
            print("   python scripts/build.py --windows --exe-only")
            print("   → Erstellt: .exe")
        else:
            print("⚠️  CROSS-PLATFORM Build:")
            print("   python scripts/build.py --windows")
            print("   → Empfohlen für nicht-Windows Systeme")
            print()
            print("💡 FÜR BESTE ERGEBNISSE:")
            print("   → Build auf Windows-System durchführen")
    
    def execute_windows_build(self, build_options: Dict) -> bool:
        """Führe Windows Build durch"""
        print(f"\n🪟 STARTE WINDOWS BUILD")
        print("=" * 30)
        
        if not self.check_windows_builder():
            return False
        
        # Show cross-platform warning
        if not self.is_windows:
            print(f"\n⚠️  CROSS-PLATFORM WARNUNG:")
            print(f"   Windows Build auf {platform.system()} System")
            print(f"   Installer-Features können eingeschränkt sein")
            
            try:
                choice = input(f"\n   Fortfahren? (j/N): ").strip().lower()
                if choice not in ['j', 'ja', 'y', 'yes']:
                    print("   Build abgebrochen.")
                    return False
            except KeyboardInterrupt:
                print("\n   Build abgebrochen.")
                return False
        
        # Build Windows-spezifische Kommando-Argumente
        cmd = [sys.executable, str(self.scripts_dir / "build_windows.py")]
        
        # Füge Build-Optionen hinzu
        if build_options.get('installer'):
            cmd.append('--installer')
        if build_options.get('msi'):
            cmd.append('--msi')
        if build_options.get('portable'):
            cmd.append('--portable')
        if build_options.get('all_packages'):
            cmd.append('--all')
        if build_options.get('sign'):
            cmd.append('--sign')
        if build_options.get('clean'):
            cmd.append('--clean')
        if build_options.get('quick'):
            cmd.append('--quick')
        
        # Zeige Build-Konfiguration
        print(f"\n🔧 BUILD KONFIGURATION:")
        print(f"   Executable: {'✓' if True else '✗'}")
        print(f"   Portable ZIP: {'✓' if build_options.get('portable', True) else '✗'}")
        print(f"   NSIS Installer: {'✓' if build_options.get('installer') else '✗'}")
        print(f"   MSI Installer: {'✓' if build_options.get('msi') else '✗'}")
        print(f"   Code Signing: {'✓' if build_options.get('sign') else '✗'}")
        print(f"   Clean Build: {'✓' if build_options.get('clean') else '✗'}")
        
        try:
            print(f"\n🚀 Starte Windows Build Script...")
            print(f"📝 Kommando: {' '.join(cmd)}")
            
            # Führe Windows Build aus
            result = subprocess.run(cmd, cwd=self.project_root)
            
            if result.returncode == 0:
                print(f"\n✅ Windows Build erfolgreich!")
                return True
            else:
                print(f"\n❌ Windows Build fehlgeschlagen (Exit Code: {result.returncode})")
                return False
                
        except KeyboardInterrupt:
            print(f"\n⚠️ Build durch Benutzer abgebrochen")
            return False
        except Exception as e:
            print(f"\n❌ Unerwarteter Build-Fehler: {e}")
            return False
    
    def show_build_results(self, success: bool):
        """Zeige Build-Ergebnisse"""
        build_time = time.time() - self.build_start
        
        print(f"\n" + "=" * 55)
        print(f"📊 BUILD ZUSAMMENFASSUNG")
        print("=" * 55)
        
        if success:
            print(f"✅ Build erfolgreich abgeschlossen!")
        else:
            print(f"❌ Build mit Fehlern beendet!")
        
        print(f"⏱️  Build Zeit: {build_time:.1f} Sekunden")
        print(f"📅 Abgeschlossen: {datetime.now().strftime('%H:%M:%S')}")
        
        # Zeige erstellte Dateien
        if self.dist_dir.exists():
            created_files = []
            total_size = 0
            
            # Sammle alle relevanten Dateien
            for pattern in ["*.exe", "*.zip", "*.msi", "*.dmg", "*.deb", "*.rpm"]:
                created_files.extend(self.dist_dir.glob(pattern))
            
            if created_files:
                print(f"\n📦 ERSTELLTE DATEIEN:")
                print("-" * 20)
                
                for file_path in sorted(created_files):
                    size = file_path.stat().st_size
                    total_size += size
                    
                    if size > 1024 * 1024:  # MB
                        size_str = f"{size / (1024 * 1024):.1f} MB"
                    else:  # KB
                        size_str = f"{size / 1024:.1f} KB"
                    
                    file_type = self.get_file_type_emoji(file_path.suffix)
                    print(f"   {file_type} {file_path.name} ({size_str})")
                
                print(f"\n💾 Gesamt Größe: {total_size / (1024 * 1024):.1f} MB")
            else:
                print(f"\n⚠️ Keine Build-Ausgaben gefunden in {self.dist_dir}")
        
        print(f"\n📁 Ausgabe-Verzeichnis: {self.dist_dir}")
        
        if success:
            print(f"\n🎉 {self.APP_NAME} v{self.APP_VERSION} erfolgreich gebaut!")
            if self.is_windows:
                print(f"🎯 Bereit für Windows-Distribution!")
        else:
            print(f"\n💡 Prüfe die Fehlermeldungen oben für Details")
    
    def get_file_type_emoji(self, extension: str) -> str:
        """Emoji für Dateitypen"""
        emoji_map = {
            '.exe': '🚀',
            '.zip': '📦',
            '.msi': '🔧',
            '.dmg': '💿',
            '.deb': '📋',
            '.rpm': '📄'
        }
        return emoji_map.get(extension.lower(), '📄')
    
    def run_build(self, build_options: Dict) -> bool:
        """Hauptfunktion für Build-Durchführung"""
        
        # Zeige verfügbare Builds
        self.print_available_builds()
        
        # Zeige Empfehlungen
        self.show_build_recommendations()
        
        # Führe passenden Build durch
        if build_options.get('platform') == 'windows' or build_options.get('windows') or self.is_windows:
            return self.execute_windows_build(build_options)
        elif build_options.get('platform') == 'macos' or build_options.get('macos') or self.is_macos:
            print(f"\n🔮 macOS Build noch nicht implementiert")
            return False
        elif build_options.get('platform') == 'linux' or build_options.get('linux') or self.is_linux:
            print(f"\n🔮 Linux Build noch nicht implementiert")
            return False
        else:
            # Auto-detect und fallback zu Windows wenn kein spezifisches OS angegeben
            print(f"\n🤖 Kein spezifisches OS angegeben. Verwende --windows, --macos oder --linux")
            print(f"   Beispiel: python scripts/build.py --windows")
            return False

def parse_arguments():
    """Parse Kommandozeilen-Argumente"""
    parser = argparse.ArgumentParser(
        description='🎯 Riflescope Calculator - Universal Build Orchestrator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 EMPFOHLENE VERWENDUNG:

WINDOWS BUILDS:
  python scripts/build.py --windows                       # Standard: .exe + .zip
  python scripts/build.py --windows --all                 # Alle Windows Pakete 
  python scripts/build.py --windows --installer           # .exe + .zip + NSIS
  python scripts/build.py --windows --exe-only            # Nur .exe
  python scripts/build.py --windows --portable-only       # Nur .zip

MACOS BUILDS (Geplant):
  python scripts/build.py --macos                         # Standard: .app + .dmg
  python scripts/build.py --macos --all                   # Alle macOS Pakete

LINUX BUILDS (Geplant):
  python scripts/build.py --linux                         # Standard: Binary + .deb
  python scripts/build.py --linux --all                   # Alle Linux Pakete

SPEZIAL OPTIONEN:
  python scripts/build.py --windows --clean --all         # Clean + Vollbuild
  python scripts/build.py --platform windows --all        # Alternative Syntax
        """
    )
    
    # Platform Selection (Primary method)
    platform_group = parser.add_mutually_exclusive_group()
    platform_group.add_argument('--windows', action='store_true', 
                       help='🪟 Windows Build (.exe + .zip + Installer)')
    platform_group.add_argument('--macos', action='store_true', 
                       help='🍎 macOS Build (.app + .dmg) [Geplant]')
    platform_group.add_argument('--linux', action='store_true', 
                       help='🐧 Linux Build (Binary + .deb/.rpm) [Geplant]')
    
    # Alternative Platform Selection (Legacy support)
    parser.add_argument('--platform', choices=['windows', 'macos', 'linux'], 
                       help='Ziel-Plattform (Alternative zu --windows/--macos/--linux)')
    
    # Universal Build Options (work with all platforms)
    parser.add_argument('--all', action='store_true', 
                       help='🎯 Alle Pakete für gewählte Plattform')
    parser.add_argument('--clean', action='store_true', 
                       help='🧹 Clean Build (lösche vorherige Builds)')
    
    # Windows-specific Quick Options
    windows_group = parser.add_argument_group('Windows Optionen')
    windows_group.add_argument('--exe-only', action='store_true', 
                       help='🚀 Nur Executable (.exe)')
    windows_group.add_argument('--portable-only', action='store_true', 
                       help='📦 Nur Portable Package (.zip)')
    windows_group.add_argument('--installer', action='store_true', 
                       help='Inkludiere NSIS Installer')
    windows_group.add_argument('--msi', action='store_true', 
                       help='Inkludiere MSI Installer')
    windows_group.add_argument('--sign', action='store_true', 
                       help='🔐 Code-Signing aktivieren')
    windows_group.add_argument('--no-portable', action='store_true', 
                       help='Überspringe Portable .zip')
    
    # Development Options
    dev_group = parser.add_argument_group('Entwickler Optionen')
    dev_group.add_argument('--debug', action='store_true', 
                       help='Debug-Modus')
    dev_group.add_argument('--verbose', action='store_true', 
                       help='Verbose Ausgabe')
    
    return parser.parse_args()

def main():
    """Haupt-Build-Funktion"""
    try:
        # Parse Argumente
        args = parse_arguments()
        
        # Initialize Orchestrator
        orchestrator = BuildOrchestrator()
        
        # Bestimme Ziel-Plattform
        target_platform = None
        if args.windows:
            target_platform = 'windows'
        elif args.macos:
            target_platform = 'macos'
        elif args.linux:
            target_platform = 'linux'
        elif args.platform:
            target_platform = args.platform
        
        # Validiere Plattform-Auswahl
        if not target_platform:
            print("❌ Keine Ziel-Plattform angegeben!")
            print("   Verwende: --windows, --macos, --linux oder --platform <name>")
            print("   Beispiel: python scripts/build.py --windows")
            return 1
        
        # Validiere Windows-spezifische Optionen
        windows_options = [args.exe_only, args.portable_only, args.installer, 
                          args.msi, args.sign, args.no_portable]
        if any(windows_options) and target_platform != 'windows':
            print(f"⚠️ Windows-spezifische Optionen werden ignoriert (Ziel: {target_platform})")
        
        # Bestimme Build-Optionen basierend auf Argumenten
        build_options = {
            'platform': target_platform,
            target_platform: True,  # Setze Platform-Flag
        }
        
        # Windows-spezifische Optionen (nur wenn Windows Build)
        if target_platform == 'windows':
            if args.all:
                build_options.update({
                    'installer': True,
                    'msi': True, 
                    'portable': True,
                    'all_packages': True
                })
            elif args.exe_only:
                build_options.update({
                    'portable': False,
                    'quick': True
                })
            elif args.portable_only:
                build_options.update({
                    'portable': True,
                    'exe_only': False,
                    'skip_exe': True
                })
            else:
                # Standard Windows Build: .exe + .zip
                build_options.update({
                    'portable': not args.no_portable,
                })
            
            # Individual Windows Options
            if args.installer:
                build_options['installer'] = True
            if args.msi:
                build_options['msi'] = True
            if args.sign:
                build_options['sign'] = True
        
        # Universal Options
        if args.clean:
            build_options['clean'] = True
        if args.debug:
            build_options['debug'] = True
        if args.verbose:
            build_options['verbose'] = True
        
        # Zeige finale Build-Konfiguration
        print(f"\n🔧 FINALE BUILD-KONFIGURATION:")
        print("-" * 35)
        print(f"   🎯 Ziel-Plattform: {target_platform.title()}")
        for key, value in build_options.items():
            if value and key != target_platform:
                print(f"   ✓ {key.replace('_', ' ').title()}")
        
        # Führe Build durch
        success = orchestrator.run_build(build_options)
        
        # Zeige Ergebnisse
        orchestrator.show_build_results(success)
        
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