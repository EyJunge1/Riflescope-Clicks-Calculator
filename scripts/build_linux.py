#!/usr/bin/env python3
"""
🐧 LINUX BUILD SCRIPT FÜR RIFLESCOPE CALCULATOR 🐧

Spezialisierter Build für Linux-Systeme
Erstellt Native Binary + Distribution Packages

🚀 LINUX FEATURES:
- Native Linux Binary Erstellung
- x86_64 + ARM Support
- AppImage Vorbereitung
- .deb/.rpm Package Vorbereitung
- Distribution-spezifische Optimierungen

📋 VERWENDUNG:
    python scripts/build_linux.py                   # Standard Build
    python scripts/build_linux.py --appimage        # AppImage-ready
    python scripts/build_linux.py --portable        # + Portable .tar.gz
"""

import os
import subprocess
import sys
import platform
import shutil
from pathlib import Path
import argparse

# Importiere gemeinsame Build-Klassen
sys.path.append(str(Path(__file__).parent))
from build import BuildConfig, CrossPlatformBuildManager

class LinuxBuildManager(CrossPlatformBuildManager):
    """Spezialisierter Linux Build Manager"""
    
    def __init__(self):
        super().__init__()
        
        # Überprüfe dass wir auf Linux sind (optional)
        if not self.platform_info['is_linux']:
            print("⚠️ Hinweis: Linux Build auf nicht-Linux System")
            print("   Cross-Compilation wird versucht...")
        
        # Detaillierte Linux-Info
        self.detect_linux_details()
    
    def detect_linux_details(self):
        """Detaillierte Linux-System-Erkennung"""
        self.linux_info = {
            'distribution': 'unknown',
            'version': 'unknown',
            'package_manager': 'unknown',
            'architecture': platform.machine()
        }
        
        try:
            # Distribution ermitteln
            if Path('/etc/os-release').exists():
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('ID='):
                            self.linux_info['distribution'] = line.split('=')[1].strip().strip('"')
                        elif line.startswith('VERSION_ID='):
                            self.linux_info['version'] = line.split('=')[1].strip().strip('"')
            
            # Package Manager ermitteln
            package_managers = {
                'apt': ['ubuntu', 'debian', 'mint'],
                'yum': ['rhel', 'centos', 'fedora'],
                'dnf': ['fedora'],
                'pacman': ['arch'],
                'zypper': ['opensuse', 'sles']
            }
            
            for pm, distros in package_managers.items():
                if self.linux_info['distribution'] in distros:
                    self.linux_info['package_manager'] = pm
                    break
            
            print(f"🐧 Linux System: {self.linux_info['distribution']} {self.linux_info['version']}")
            print(f"   Architektur: {self.linux_info['architecture']}")
            print(f"   Package Manager: {self.linux_info['package_manager']}")
            
        except Exception as e:
            print(f"⚠️ Linux-Erkennung fehlgeschlagen: {e}")
    
    def check_linux_requirements(self):
        """Überprüft Linux-spezifische Build-Voraussetzungen"""
        print("🔍 Überprüfe Linux Build-Voraussetzungen...")
        
        # Basis-Requirements
        super().check_requirements()
        
        # Linux-spezifische System-Packages prüfen
        system_packages = ['python3-tk']
        missing_packages = []
        
        for package in system_packages:
            # Vereinfachte Prüfung - bei Fehlern wird Hinweis gegeben
            try:
                if package == 'python3-tk':
                    import tkinter
                    print(f"✓ {package} (tkinter) verfügbar")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} fehlt")
        
        if missing_packages:
            print(f"\n💡 Installiere fehlende Pakete:")
            if self.linux_info['package_manager'] == 'apt':
                print(f"   sudo apt-get install {' '.join(missing_packages)}")
            elif self.linux_info['package_manager'] in ['yum', 'dnf']:
                print(f"   sudo {self.linux_info['package_manager']} install {' '.join(missing_packages)}")
            elif self.linux_info['package_manager'] == 'pacman':
                print(f"   sudo pacman -S {' '.join(missing_packages)}")
            else:
                print(f"   Installiere mit deinem Package Manager: {' '.join(missing_packages)}")
        
        return True
    
    def create_linux_spec_file(self, appimage=False):
        """Erstellt Linux-optimierte PyInstaller spec-Datei"""
        print(f"📝 Erstelle Linux-optimierte spec-Datei (AppImage: {appimage})...")
        
        version_info = self.get_version_info()
        icon_path = self.get_platform_icon()
        
        spec_content = f'''# Linux PyInstaller Spec für Riflescope Calculator
# Optimiert für {self.linux_info['distribution']} {self.linux_info['version']}
# Architektur: {self.linux_info['architecture']}

import os
import sys
from pathlib import Path

# Konfiguration
APP_NAME = "{self.config.APP_NAME}"
PROJECT_ROOT = Path(r"{self.project_root}")

# Linux-spezifische Datenfiles
datas = [
    (str(PROJECT_ROOT / "src"), "src"),
]

# Optionale Verzeichnisse
optional_dirs = [
    ("icons", "icons"),
    ("database", "database"),
]

for src_dir, dst_dir in optional_dirs:
    src_path = PROJECT_ROOT / src_dir
    if src_path.exists() and any(src_path.iterdir()):
        datas.append((str(src_path), dst_dir))

# Linux-optimierte Hidden imports
hiddenimports = [
    # GUI Framework
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    
    # Linux-spezifisch
    'distutils.util',
    'pwd',  # Unix user info
    'grp',  # Unix group info
    
    # Database
    'sqlite3',
    
    # Application modules
    'src.main',
    'src.config',
    'src.core',
    'src.database',
    'src.gui',
    'src.utils',
    'src.models',
]

# Linux-spezifische Exclusions
excludes = [
    'matplotlib', 'numpy', 'pandas', 'scipy',
    'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
    'win32api', 'win32con',  # Windows-spezifisch
    'Foundation', 'AppKit', 'Cocoa',  # macOS-spezifisch
    'django', 'flask', 'tornado',
    'unittest', 'pytest',
]

block_cipher = None

a = Analysis(
    [str(PROJECT_ROOT / "run.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)'''

        if appimage:
            spec_content += '''

# AppImage preparation
collect = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=APP_NAME + "_AppImage"
)'''
        
        # Spec-Datei schreiben
        suffix = "_appimage" if appimage else "_native"
        spec_file_path = self.project_root / self.config.SPEC_DIR / f"{self.config.APP_NAME}_linux{suffix}.spec"
        spec_file_path.parent.mkdir(exist_ok=True)
        
        with open(spec_file_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print(f"✓ Linux Spec-Datei erstellt: {spec_file_path}")
        return spec_file_path
    
    def build_linux_binary(self, appimage=False):
        """Erstellt Linux Binary"""
        print(f"🔨 Erstelle Linux Binary (AppImage: {appimage})...")
        
        # Erstelle spec-Datei
        spec_file = self.create_linux_spec_file(appimage)
        
        # PyInstaller ausführen
        cmd = ['pyinstaller', str(spec_file), '--log-level=WARN']
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Linux Binary erfolgreich erstellt!")
                
                # Ausführbar machen
                if appimage:
                    binary_dir = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}_AppImage"
                    binary_path = binary_dir / self.config.APP_NAME
                else:
                    binary_path = self.project_root / self.config.DIST_DIR / self.config.APP_NAME
                
                if binary_path.exists():
                    os.chmod(binary_path, 0o755)
                    print("✓ Binary als ausführbar markiert")
                
                return True
            else:
                print(f"❌ Linux Build fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Linux Build-Fehler: {e}")
            return False
    
    def create_appimage_structure(self):
        """Erstellt AppImage-Verzeichnisstruktur"""
        print("📦 Erstelle AppImage-Struktur...")
        
        appdir = self.project_root / self.config.BUILD_DIR / "AppDir"
        
        # Basis-Struktur
        dirs = ["usr/bin", "usr/share/applications", "usr/share/icons/hicolor/256x256/apps"]
        for dir_path in dirs:
            (appdir / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Binary kopieren
        binary_src = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}_AppImage" / self.config.APP_NAME
        binary_dst = appdir / "usr/bin" / self.config.APP_NAME
        
        if binary_src.exists():
            shutil.copy2(binary_src, binary_dst)
            os.chmod(binary_dst, 0o755)
        
        # Desktop-Datei erstellen
        desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.config.APP_DISPLAY_NAME}
Comment={self.config.APP_DESCRIPTION}
Exec={self.config.APP_NAME}
Icon={self.config.APP_NAME}
Categories=Utility;Sports;
Terminal=false
"""
        
        desktop_file = appdir / "usr/share/applications" / f"{self.config.APP_NAME}.desktop"
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        
        # Icon kopieren
        icon_src = self.get_platform_icon()
        if icon_src:
            icon_dst = appdir / "usr/share/icons/hicolor/256x256/apps" / f"{self.config.APP_NAME}.png"
            try:
                shutil.copy2(icon_src, icon_dst)
            except:
                print("⚠️ Icon konnte nicht kopiert werden")
        
        # AppRun erstellen
        apprun_content = f"""#!/bin/bash
HERE="$(dirname "$(readlink -f "${{0}}")")"
exec "${{HERE}}/usr/bin/{self.config.APP_NAME}" "$@"
"""
        
        apprun_file = appdir / "AppRun"
        with open(apprun_file, 'w') as f:
            f.write(apprun_content)
        os.chmod(apprun_file, 0o755)
        
        print(f"✓ AppImage-Struktur erstellt: {appdir}")
        return appdir
    
    def create_linux_portable(self):
        """Erstellt Linux Portable .tar.gz"""
        print("📦 Erstelle Linux Portable Paket...")
        
        return super().create_portable_package()

def main():
    """Linux Build Hauptfunktion"""
    parser = argparse.ArgumentParser(description='Linux Build für Riflescope Calculator')
    
    parser.add_argument('--clean', action='store_true', help='Bereinige vor Build')
    parser.add_argument('--test', action='store_true', help='Führe Tests durch')
    parser.add_argument('--portable', action='store_true', help='Erstelle Portable .tar.gz')
    parser.add_argument('--appimage', action='store_true', help='AppImage-ready Build')
    parser.add_argument('--keep-files', action='store_true', help='Behalte Build-Dateien')
    parser.add_argument('--no-verify', action='store_true', help='Überspringe Verifikation')
    
    args = parser.parse_args()
    
    print("🐧 Linux Build für Riflescope Calculator")
    print("=" * 40)
    
    builder = LinuxBuildManager()
    
    try:
        # 1. Linux-spezifische Voraussetzungen
        builder.check_linux_requirements()
        
        # 2. Build-Umgebung
        builder.prepare_build_environment()
        
        # 3. Tests (optional)
        if args.test and not builder.run_tests():
            return 1
        
        # 4. Linux Binary
        if not builder.build_linux_binary(appimage=args.appimage):
            return 1
        
        # 5. AppImage-Struktur (optional)
        if args.appimage:
            builder.create_appimage_structure()
        
        # 6. Verifikation
        if not args.no_verify and not builder.verify_executable():
            print("⚠️ Verifikation fehlgeschlagen")
        
        # 7. Portable Paket
        if args.portable and not builder.create_linux_portable():
            print("⚠️ Portable-Paket fehlgeschlagen")
        
        # 8. Build-Report
        builder.create_build_report()
        
        # 9. Cleanup
        if not args.keep_files:
            builder.cleanup_build_files()
        
        print("\n🎉 Linux Build erfolgreich abgeschlossen!")
        
        # Linux-spezifische Hinweise
        binary_name = builder.config.APP_NAME
        print(f"\n📋 Linux Nächste Schritte:")
        print(f"1. Teste: ./dist/{binary_name}")
        if args.appimage:
            print(f"2. AppImage-Struktur verfügbar in build/AppDir")
            print(f"3. Erstelle AppImage mit appimagetool")
        print(f"4. Optional: Erstelle .deb/.rpm Pakete")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Linux Build-Fehler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
