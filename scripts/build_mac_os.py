#!/usr/bin/env python3
"""
🍎 MACOS BUILD SCRIPT FÜR RIFLESCOPE CALCULATOR 🍎

Spezialisierter Build für macOS-Systeme
Erstellt .app Bundle mit Apple Silicon & Intel Support

🚀 MACOS FEATURES:
- Native .app Bundle Erstellung
- Apple Silicon (M1/M2/M3) + Intel Support
- Universal Binary Möglichkeit
- macOS-spezifische Icons und Plist
- Code-Signing Vorbereitung

📋 VERWENDUNG:
    python scripts/build_mac_os.py                  # Standard Build
    python scripts/build_mac_os.py --universal      # Universal Binary
    python scripts/build_mac_os.py --portable       # + Portable .tar.gz
"""

import os
import subprocess
import sys
import platform
from pathlib import Path
import argparse

# Importiere gemeinsame Build-Klassen
sys.path.append(str(Path(__file__).parent))
from build import BuildConfig, CrossPlatformBuildManager

class MacOSBuildManager(CrossPlatformBuildManager):
    """Spezialisierter macOS Build Manager"""
    
    def __init__(self):
        super().__init__()
        
        # Überprüfe dass wir auf macOS sind (optional)
        if not self.platform_info['is_macos']:
            print("⚠️ Hinweis: macOS Build auf nicht-macOS System")
            print("   Cross-Compilation wird versucht...")
        
        # Detaillierte Architektur-Info für macOS
        self.detect_macos_architecture()
    
    def detect_macos_architecture(self):
        """Detaillierte macOS Architektur-Erkennung"""
        if self.platform_info['is_macos']:
            try:
                # Native Architektur ermitteln
                result = subprocess.run(['uname', '-m'], capture_output=True, text=True)
                native_arch = result.stdout.strip()
                
                # Rosetta-Status prüfen (bei Apple Silicon)
                rosetta_available = False
                if native_arch == 'arm64':
                    try:
                        subprocess.run(['arch', '-x86_64', 'true'], check=True, capture_output=True)
                        rosetta_available = True
                    except:
                        pass
                
                self.macos_info = {
                    'native_arch': native_arch,
                    'is_apple_silicon': native_arch == 'arm64',
                    'is_intel': native_arch == 'x86_64',
                    'rosetta_available': rosetta_available,
                    'can_build_universal': native_arch == 'arm64' and rosetta_available
                }
                
                print(f"🍎 macOS Architektur: {native_arch}")
                if self.macos_info['is_apple_silicon']:
                    print("   Apple Silicon (M1/M2/M3) erkannt")
                    if rosetta_available:
                        print("   Rosetta verfügbar - Universal Build möglich")
                elif self.macos_info['is_intel']:
                    print("   Intel Mac erkannt")
                    
            except Exception as e:
                print(f"⚠️ Architektur-Erkennung fehlgeschlagen: {e}")
                self.macos_info = {'native_arch': 'unknown'}
    
    def check_macos_requirements(self):
        """Überprüft macOS-spezifische Build-Voraussetzungen"""
        print("🔍 Überprüfe macOS Build-Voraussetzungen...")
        
        # Basis-Requirements
        super().check_requirements()
        
        # macOS-spezifische Packages
        macos_packages = ['macholib']
        
        for package in macos_packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"✓ {package} verfügbar")
            except ImportError:
                print(f"📦 Installiere {package}...")
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", package
                    ], stdout=subprocess.DEVNULL)
                    print(f"✓ {package} installiert")
                except subprocess.CalledProcessError:
                    print(f"⚠️ Konnte {package} nicht installieren")
        
        return True
    
    def create_macos_spec_file(self, universal=False):
        """Erstellt macOS-optimierte PyInstaller spec-Datei"""
        print(f"📝 Erstelle macOS-optimierte spec-Datei (Universal: {universal})...")
        
        version_info = self.get_version_info()
        icon_path = self.get_platform_icon()
        
        # Target-Architektur bestimmen
        if universal and hasattr(self, 'macos_info') and self.macos_info.get('can_build_universal'):
            target_arch = 'universal2'
            arch_comment = "# Universal Binary für Intel + Apple Silicon"
        elif hasattr(self, 'macos_info'):
            if self.macos_info.get('is_apple_silicon'):
                target_arch = 'arm64'
                arch_comment = "# Apple Silicon (arm64)"
            elif self.macos_info.get('is_intel'):
                target_arch = 'x86_64'
                arch_comment = "# Intel (x86_64)"
            else:
                target_arch = None
                arch_comment = "# Auto-detect"
        else:
            target_arch = None
            arch_comment = "# Auto-detect"
        
        spec_content = f'''# macOS PyInstaller Spec für Riflescope Calculator
{arch_comment}

import os
import sys
from pathlib import Path

# Konfiguration
APP_NAME = "{self.config.APP_NAME}"
PROJECT_ROOT = Path(r"{self.project_root}")

# macOS-spezifische Datenfiles
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

# macOS-optimierte Hidden imports
hiddenimports = [
    # GUI Framework
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    
    # macOS-spezifisch
    'Foundation',
    'AppKit',
    'Cocoa',
    
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

# macOS-spezifische Exclusions
excludes = [
    'matplotlib', 'numpy', 'pandas', 'scipy',
    'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
    'win32api', 'win32con',  # Windows-spezifisch
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
    argv_emulation=False,'''

        if target_arch:
            spec_content += f'''
    target_arch='{target_arch}','''

        spec_content += '''
    codesign_identity=None,
    entitlements_file=None,
)

# macOS App Bundle'''

        bundle_icon = f'icon=r"{icon_path}",' if icon_path else ''
        
        # Build info_plist dictionary content
        info_plist_entries = [
            f'"CFBundleName": "{self.config.APP_DISPLAY_NAME}",',
            f'"CFBundleDisplayName": "{self.config.APP_DISPLAY_NAME}",',
            f'"CFBundleIdentifier": "com.riflescope.calculator",',
            f'"CFBundleVersion": "{version_info}",',
            f'"CFBundleShortVersionString": "{version_info}",',
            f'"CFBundleExecutable": APP_NAME,',
            f'"CFBundlePackageType": "APPL",',
            f'"CFBundleSignature": "RFSC",',
            f'"NSHighResolutionCapable": True,',
            f'"NSRequiresAquaSystemAppearance": False,',
            f'"LSMinimumSystemVersion": "10.13.0",'
        ]
        
        if target_arch == 'universal2':
            info_plist_entries.append('"LSArchitecturePriority": ["arm64", "x86_64"],')
        elif target_arch == 'arm64':
            info_plist_entries.extend([
                '"LSArchitecturePriority": ["arm64", "x86_64"],',
                '"LSRequiresNativeExecution": True,'
            ])
        elif target_arch == 'x86_64':
            info_plist_entries.append('"LSArchitecturePriority": ["x86_64", "arm64"],')
        
        info_plist_entries.extend([
            '"NSMicrophoneUsageDescription": "Für Audio-Feedback (optional)",',
            '"NSCameraUsageDescription": "Für Zielfernrohr-Kamera (optional)"'
        ])
        
        spec_content += f'''
app = BUNDLE(
    exe,
    name="{self.config.APP_DISPLAY_NAME}.app",
    {bundle_icon}
    bundle_identifier="com.riflescope.calculator",
    version="{version_info}",
    info_plist={{
        {chr(10).join("        " + entry for entry in info_plist_entries)}
    }}
)'''
        
        # Spec-Datei schreiben
        suffix = "_universal" if universal else "_native"
        spec_file_path = self.project_root / self.config.SPEC_DIR / f"{self.config.APP_NAME}_macos{suffix}.spec"
        spec_file_path.parent.mkdir(exist_ok=True)
        
        with open(spec_file_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print(f"✓ macOS Spec-Datei erstellt: {spec_file_path}")
        return spec_file_path
    
    def build_macos_app(self, universal=False):
        """Erstellt macOS .app Bundle"""
        print(f"🔨 Erstelle macOS App Bundle (Universal: {universal})...")
        
        # Erstelle spec-Datei
        spec_file = self.create_macos_spec_file(universal)
        
        # PyInstaller ausführen
        cmd = ['pyinstaller', str(spec_file), '--log-level=WARN']
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ macOS App Bundle erfolgreich erstellt!")
                return True
            else:
                print(f"❌ macOS Build fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ macOS Build-Fehler: {e}")
            return False
    
    def create_macos_dmg(self):
        """Erstellt macOS DMG Image"""
        print("📦 Erstelle macOS DMG...")
        
        app_name = f"{self.config.APP_DISPLAY_NAME}.app"
        app_path = self.project_root / self.config.DIST_DIR / app_name
        dmg_path = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}-macos.dmg"
        
        if not app_path.exists():
            print("❌ App Bundle nicht gefunden")
            return False
        
        try:
            # Temporäres DMG-Verzeichnis
            dmg_temp_dir = self.project_root / self.config.BUILD_DIR / "dmg_temp"
            dmg_temp_dir.mkdir(exist_ok=True)
            
            # App kopieren
            import shutil
            temp_app_path = dmg_temp_dir / app_name
            if temp_app_path.exists():
                shutil.rmtree(temp_app_path)
            shutil.copytree(app_path, temp_app_path)
            
            # Applications-Link erstellen
            applications_link = dmg_temp_dir / "Applications"
            if applications_link.exists():
                applications_link.unlink()
            applications_link.symlink_to("/Applications")
            
            # README erstellen
            readme_content = f"""{self.config.APP_DISPLAY_NAME}

Ziehe die App in den Applications-Ordner um sie zu installieren.

Version: {self.config.APP_VERSION}
Universal Binary für Intel & Apple Silicon

Website: https://github.com/yourusername/Riflescope-Clicks-Calculator
"""
            
            readme_file = dmg_temp_dir / "README.txt"
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # DMG erstellen
            cmd = [
                'hdiutil', 'create', '-volname', self.config.APP_DISPLAY_NAME,
                '-srcfolder', str(dmg_temp_dir),
                '-ov', '-format', 'UDZO',
                str(dmg_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ DMG erstellt: {dmg_path}")
                
                # Cleanup
                shutil.rmtree(dmg_temp_dir)
                return True
            else:
                print(f"❌ DMG-Erstellung fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ DMG-Fehler: {e}")
            return False
    
    def create_macos_portable_targz(self):
        """Erstellt macOS Portable .tar.gz"""
        print("📦 Erstelle macOS Portable .tar.gz...")
        
        import tarfile
        
        app_name = f"{self.config.APP_DISPLAY_NAME}.app"
        app_path = self.project_root / self.config.DIST_DIR / app_name
        targz_path = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}-macos-portable.tar.gz"
        
        if not app_path.exists():
            print("❌ App Bundle nicht gefunden")
            return False
        
        try:
            with tarfile.open(targz_path, 'w:gz') as tar:
                tar.add(app_path, arcname=app_name)
                
                # README hinzufügen
                readme_content = f"""{self.config.APP_DISPLAY_NAME} - Portable Version

Entpacke das Archiv und führe die .app aus.

Version: {self.config.APP_VERSION}
"""
                
                import io
                readme_info = tarfile.TarInfo('README.txt')
                readme_data = readme_content.encode('utf-8')
                readme_info.size = len(readme_data)
                tar.addfile(readme_info, io.BytesIO(readme_data))
            
            print(f"✅ Portable .tar.gz erstellt: {targz_path}")
            return True
            
        except Exception as e:
            print(f"❌ .tar.gz-Erstellung fehlgeschlagen: {e}")
            return False

def main():
    """macOS Build Hauptfunktion"""
    parser = argparse.ArgumentParser(description='macOS Build für Riflescope Calculator')
    
    parser.add_argument('--clean', action='store_true', help='Bereinige vor Build')
    parser.add_argument('--test', action='store_true', help='Führe Tests durch')
    parser.add_argument('--portable', action='store_true', help='Erstelle Portable .tar.gz')
    parser.add_argument('--dmg', action='store_true', help='Erstelle DMG')
    parser.add_argument('--universal', action='store_true', help='Universal Binary (Intel + Apple Silicon)')
    parser.add_argument('--quick', action='store_true', help='Nur App Bundle (schnell)')
    parser.add_argument('--keep-files', action='store_true', help='Behalte Build-Dateien')
    parser.add_argument('--no-verify', action='store_true', help='Überspringe Verifikation')
    
    args = parser.parse_args()
    
    print("🍎 macOS Build für Riflescope Calculator")
    print("=" * 42)
    
    builder = MacOSBuildManager()
    
    try:
        # 1. macOS-spezifische Voraussetzungen
        builder.check_macos_requirements()
        
        # 2. Build-Umgebung
        builder.prepare_build_environment()
        
        # 3. Tests (optional)
        if args.test and not builder.run_tests():
            return 1
        
        # 4. macOS App Bundle
        if not builder.build_macos_app(universal=args.universal):
            return 1
        
        # 5. Verifikation
        if not args.no_verify and not builder.verify_executable():
            print("⚠️ Verifikation fehlgeschlagen")
        
        # 6. Zusätzliche Pakete (nur wenn nicht quick)
        if not args.quick:
            if args.dmg and not builder.create_macos_dmg():
                print("⚠️ DMG-Erstellung fehlgeschlagen")
            
            if args.portable and not builder.create_macos_portable_targz():
                print("⚠️ Portable-Paket fehlgeschlagen")
        
        # 7. Build-Report
        builder.create_build_report()
        
        # 8. Cleanup
        if not args.keep_files:
            builder.cleanup_build_files()
        
        print("\n🎉 macOS Build erfolgreich abgeschlossen!")
        
        # Zeige erstellte Dateien
        dist_dir = builder.project_root / builder.config.DIST_DIR
        created_files = []
        for pattern in ["*.app", "*.dmg", "*.tar.gz"]:
            created_files.extend(dist_dir.glob(pattern))
        
        if created_files:
            print(f"\n📦 Erstellte Dateien:")
            for file_path in created_files:
                if file_path.is_dir():
                    print(f"   {file_path.name} (App Bundle)")
                else:
                    file_size = file_path.stat().st_size // (1024 * 1024)
                    print(f"   {file_path.name} ({file_size} MB)")
        
        # macOS-spezifische Hinweise
        app_name = f"{builder.config.APP_DISPLAY_NAME}.app"
        print(f"\n📋 macOS Nächste Schritte:")
        print(f"1. Teste: open 'dist/{app_name}'")
        print(f"2. Optional: codesign für Distribution")
        if args.universal:
            print(f"3. Universal Binary erstellt (Intel + Apple Silicon)")
        if args.dmg:
            print(f"4. DMG bereit für Distribution")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ macOS Build-Fehler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
