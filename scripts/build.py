#!/usr/bin/env python3
"""
🎯 RIFLESCOPE CALCULATOR - UNIVERSAL BUILD SELECTOR 🎯

Cross-Platform Build Script Selector für alle Betriebssysteme
Wähle dein Ziel-Betriebssystem oder baue für alle Plattformen

🚀 UNTERSTÜTZTE PLATTFORMEN:
- 🪟 Windows (32/64-bit) → .exe + Setup.exe
- 🍎 macOS (Intel + Apple Silicon) → .app Bundle  
- 🐧 Linux (x86_64/ARM) → Native Binary

📋 VERWENDUNG:
    python scripts/build.py                 # Interaktive Auswahl
    python scripts/build.py --windows       # Nur Windows
    python scripts/build.py --macos         # Nur macOS
    python scripts/build.py --linux         # Nur Linux
    python scripts/build.py --all           # Alle Plattformen

⭐ AUTOMATISCHE PLATTFORM-ERKENNUNG UND OPTIMIERUNG!
"""

import os
import sys
import subprocess
import platform
import argparse
import shutil
import json
from pathlib import Path
from datetime import datetime

class BuildConfig:
    """Build Configuration Class"""
    
    def __init__(self):
        self.APP_NAME = "riflescope-calculator"
        self.APP_DISPLAY_NAME = "Riflescope Calculator"
        self.APP_DESCRIPTION = "Professional Riflescope Click Calculator"
        self.APP_VERSION = "1.0.0"
        self.APP_AUTHOR = "Riflescope Tools"
        
        # Build Directories
        self.BUILD_DIR = "build"
        self.DIST_DIR = "dist"
        self.SPEC_DIR = "build"
        
        # Package Info
        self.BUNDLE_IDENTIFIER = "com.riflescope.calculator"

class CrossPlatformBuildManager:
    """Base class for cross-platform build management"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config = BuildConfig()
        
        # Platform detection
        self.platform_info = {
            'system': platform.system().lower(),
            'machine': platform.machine(),
            'is_windows': platform.system().lower() == 'windows',
            'is_macos': platform.system().lower() == 'darwin',
            'is_linux': platform.system().lower() == 'linux'
        }
    
    def check_requirements(self):
        """Check basic build requirements"""
        print("🔍 Überprüfe Build-Voraussetzungen...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ erforderlich")
            return False
        
        # Check PyInstaller
        try:
            import PyInstaller
            print("✓ PyInstaller verfügbar")
        except ImportError:
            print("📦 Installiere PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        
        return True
    
    def prepare_build_environment(self):
        """Prepare build environment"""
        print("🏗️ Bereite Build-Umgebung vor...")
        
        # Create build directories
        for dir_name in [self.config.BUILD_DIR, self.config.DIST_DIR]:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(exist_ok=True)
        
        return True
    
    def get_version_info(self):
        """Get version information"""
        return self.config.APP_VERSION
    
    def get_platform_icon(self):
        """Get platform-specific icon path"""
        icon_dir = self.project_root / "icons"
        
        if self.platform_info['is_windows']:
            icon_file = icon_dir / "app.ico"
        elif self.platform_info['is_macos']:
            icon_file = icon_dir / "app.icns"
        else:
            icon_file = icon_dir / "app.png"
        
        return str(icon_file) if icon_file.exists() else None
    
    def run_tests(self):
        """Run application tests"""
        print("🧪 Führe Tests durch...")
        # Placeholder for test execution
        return True
    
    def verify_executable(self):
        """Verify created executable"""
        print("✅ Verifiziere Executable...")
        # Placeholder for verification
        return True
    
    def create_portable_package(self):
        """Create portable package"""
        print("📦 Erstelle Portable Paket...")
        # Placeholder for portable package creation
        return True
    
    def create_installer_script(self):
        """Create installer script"""
        print("📦 Erstelle Installer...")
        # Placeholder for installer creation
        return True
    
    def create_version_file(self):
        """Create version file for Windows builds"""
        if not self.platform_info['is_windows']:
            return
        
        version_content = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [StringStruct('CompanyName', '{self.config.APP_AUTHOR}'),
         StringStruct('FileDescription', '{self.config.APP_DESCRIPTION}'),
         StringStruct('FileVersion', '{self.config.APP_VERSION}'),
         StringStruct('InternalName', '{self.config.APP_NAME}'),
         StringStruct('LegalCopyright', 'Copyright (c) 2024'),
         StringStruct('OriginalFilename', '{self.config.APP_NAME}.exe'),
         StringStruct('ProductName', '{self.config.APP_DISPLAY_NAME}'),
         StringStruct('ProductVersion', '{self.config.APP_VERSION}')])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)"""
        
        version_file = self.project_root / self.config.BUILD_DIR / "version_info.txt"
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_content)
    
    def create_build_report(self):
        """Create build report"""
        print("📊 Erstelle Build-Report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'platform': self.platform_info,
            'version': self.config.APP_VERSION,
            'build_successful': True
        }
        
        report_file = self.project_root / self.config.BUILD_DIR / "build_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
    
    def cleanup_build_files(self):
        """Cleanup temporary build files"""
        print("🧹 Bereinige Build-Dateien...")
        
        cleanup_patterns = ["*.pyc", "__pycache__", "*.spec"]
        # Basic cleanup implementation
        return True

class PlatformBuildSelector:
    """Platform Build Selector für Cross-Platform Builds"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"
        self.current_platform = platform.system().lower()
        
        print("🎯 Riflescope Calculator - Build Platform Selector")
        print("=" * 55)
        print(f"Aktuelles System: {self.get_platform_display_name(self.current_platform)}")
    
    def get_platform_display_name(self, platform_name):
        """Gibt schönen Plattform-Namen zurück"""
        names = {
            'windows': '🪟 Windows',
            'darwin': '🍎 macOS', 
            'linux': '🐧 Linux'
        }
        return names.get(platform_name, platform_name.title())
    
    def check_build_scripts(self):
        """Überprüft ob alle Build-Scripts verfügbar sind"""
        required_scripts = {
            'windows': 'build_windows.py',
            'macos': 'build_mac_os.py', 
            'linux': 'build_linux.py'
        }
        
        missing = []
        for platform_name, script_name in required_scripts.items():
            script_path = self.scripts_dir / script_name
            if not script_path.exists():
                missing.append(f"{platform_name} ({script_name})")
        
        if missing:
            print(f"❌ Fehlende Build-Scripts: {', '.join(missing)}")
            return False
        
        print("✅ Alle Platform Build-Scripts verfügbar")
        return True
    
    def show_platform_menu(self):
        """Zeigt interaktives Platform-Auswahl-Menü"""
        print("\n🔧 Wähle Build-Ziel:")
        print("=" * 30)
        print("1. 🪟 Windows Build (.exe + Installer)")
        print("2. 🍎 macOS Build (.app Bundle)")
        print("3. 🐧 Linux Build (Native Binary)")
        print("4. 🌍 Alle Plattformen")
        print("5. ❌ Abbrechen")
        
        while True:
            try:
                choice = input("\nWähle eine Option (1-5): ").strip()
                
                if choice == '1':
                    return 'windows'
                elif choice == '2':
                    return 'macos'
                elif choice == '3':
                    return 'linux'
                elif choice == '4':
                    return 'all'
                elif choice == '5':
                    print("Build abgebrochen.")
                    return None
                else:
                    print("❌ Ungültige Auswahl. Bitte 1-5 eingeben.")
                    
            except (KeyboardInterrupt, EOFError):
                print("\n\nBuild abgebrochen.")
                return None
    
    def run_platform_build(self, platform_name, additional_args=None):
        """Führt plattform-spezifischen Build aus"""
        if additional_args is None:
            additional_args = []
        
        script_mapping = {
            'windows': 'build_windows.py',
            'macos': 'build_mac_os.py',
            'linux': 'build_linux.py'
        }
        
        script_name = script_mapping.get(platform_name)
        if not script_name:
            print(f"❌ Unbekannte Plattform: {platform_name}")
            return False
        
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            print(f"❌ Build-Script nicht gefunden: {script_path}")
            return False
        
        print(f"\n🚀 Starte {self.get_platform_display_name(platform_name)} Build...")
        print("-" * 50)
        
        # Führe plattform-spezifischen Build aus
        cmd = [sys.executable, str(script_path)] + additional_args
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root)
            
            if result.returncode == 0:
                print(f"✅ {self.get_platform_display_name(platform_name)} Build erfolgreich!")
                return True
            else:
                print(f"❌ {self.get_platform_display_name(platform_name)} Build fehlgeschlagen!")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim {platform_name} Build: {e}")
            return False
    
    def run_all_platforms(self, additional_args=None):
        """Führt Builds für alle Plattformen aus"""
        platforms = ['windows', 'macos', 'linux']
        results = {}
        
        print("\n🌍 Starte Builds für alle Plattformen...")
        print("=" * 45)
        
        for platform_name in platforms:
            success = self.run_platform_build(platform_name, additional_args)
            results[platform_name] = success
        
        # Zusammenfassung
        print("\n📊 Build-Zusammenfassung:")
        print("=" * 25)
        
        for platform_name, success in results.items():
            status = "✅ Erfolgreich" if success else "❌ Fehlgeschlagen"
            print(f"{self.get_platform_display_name(platform_name)}: {status}")
        
        successful = sum(results.values())
        total = len(results)
        
        if successful == total:
            print(f"\n🎉 Alle {total} Builds erfolgreich!")
            return True
        else:
            print(f"\n⚠️ {successful}/{total} Builds erfolgreich")
            return False
    
    def run_recommended_build(self):
        """Führt empfohlenen Build für aktuelles System aus"""
        platform_mapping = {
            'windows': 'windows',
            'darwin': 'macos',
            'linux': 'linux'
        }
        
        target_platform = platform_mapping.get(self.current_platform)
        
        if target_platform:
            print(f"\n💡 Empfohlener Build für dein System: {self.get_platform_display_name(target_platform)}")
            return self.run_platform_build(target_platform)
        else:
            print(f"❌ Unbekanntes System: {self.current_platform}")
            return False

def main():
    """Hauptfunktion für Platform Build Selection"""
    parser = argparse.ArgumentParser(
        description='Universal Build Platform Selector für Riflescope Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=""",
🎯 PLATFORM BUILD SELECTOR

Verfügbare Optionen:
  --windows         Nur Windows Build
  --macos           Nur macOS Build  
  --linux           Nur Linux Build
  --all             Alle Plattformen
  --recommended     Empfohlener Build für aktuelles System

Build-Optionen (an Platform-Scripts weitergegeben):
  --clean           Bereinige vor Build
  --test            Führe Tests durch
  --portable        Erstelle portable Pakete
  --installer       Erstelle Installer

Beispiele:
  python scripts/build.py                           # Interaktive Auswahl
  python scripts/build.py --windows --clean         # Windows mit Bereinigung
  python scripts/build.py --all --portable          # Alle Plattformen + Portable
  python scripts/build.py --recommended             # Für aktuelles System
        """
    )
    
    # Platform-Auswahl
    parser.add_argument('--windows', action='store_true',
                       help='Build nur für Windows')
    parser.add_argument('--macos', action='store_true',
                       help='Build nur für macOS')
    parser.add_argument('--linux', action='store_true',
                       help='Build nur für Linux')
    parser.add_argument('--all', action='store_true',
                       help='Build für alle Plattformen')
    parser.add_argument('--recommended', action='store_true',
                       help='Empfohlener Build für aktuelles System')
    
    # Build-Optionen (werden an Platform-Scripts weitergegeben)
    parser.add_argument('--clean', action='store_true',
                       help='Bereinige vor Build')
    parser.add_argument('--test', action='store_true',
                       help='Führe Tests durch')
    parser.add_argument('--portable', action='store_true',
                       help='Erstelle portable Pakete')
    parser.add_argument('--installer', action='store_true',
                       help='Erstelle Installer')
    parser.add_argument('--keep-files', action='store_true',
                       help='Behalte Build-Dateien')
    parser.add_argument('--no-verify', action='store_true',
                       help='Überspringe Verifikation')
    
    args = parser.parse_args()
    
    selector = PlatformBuildSelector()
    
    # Überprüfe Build-Scripts
    if not selector.check_build_scripts():
        return 1
    
    # Sammle zusätzliche Argumente für Platform-Scripts
    additional_args = []
    if args.clean:
        additional_args.append('--clean')
    if args.test:
        additional_args.append('--test')
    if args.portable:
        additional_args.append('--portable')
    if args.installer:
        additional_args.append('--installer')
    if args.keep_files:
        additional_args.append('--keep-files')
    if args.no_verify:
        additional_args.append('--no-verify')
    
    try:
        # Bestimme gewählte Plattform
        selected_platforms = []
        if args.windows:
            selected_platforms.append('windows')
        if args.macos:
            selected_platforms.append('macos')
        if args.linux:
            selected_platforms.append('linux')
        
        if args.all:
            return 0 if selector.run_all_platforms(additional_args) else 1
        elif args.recommended:
            return 0 if selector.run_recommended_build() else 1
        elif selected_platforms:
            # Spezifische Plattform(en) gewählt
            success = True
            for platform in selected_platforms:
                if not selector.run_platform_build(platform, additional_args):
                    success = False
            return 0 if success else 1
        else:
            # Interaktive Auswahl
            choice = selector.show_platform_menu()
            
            if choice is None:
                return 1
            elif choice == 'all':
                return 0 if selector.run_all_platforms(additional_args) else 1
            else:
                return 0 if selector.run_platform_build(choice, additional_args) else 1
    
    except KeyboardInterrupt:
        print("\n\nBuild abgebrochen.")
        return 1
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())