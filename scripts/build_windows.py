#!/usr/bin/env python3
"""
🪟 WINDOWS BUILD SCRIPT FÜR RIFLESCOPE CALCULATOR 🪟

Spezialisierter Build für Windows-Systeme
Erstellt .exe Executable + Windows Installer

🚀 WINDOWS FEATURES:
- Optimierte .exe Erstellung mit PyInstaller
- Windows-spezifische Icons und Resources
- NSIS Installer-Generierung
- Version-Info Integration
- Windows Registry Integration

📋 VERWENDUNG:
    python scripts/build_windows.py                 # Standard Build
    python scripts/build_windows.py --installer     # Mit NSIS Installer
    python scripts/build_windows.py --portable      # + Portable ZIP
"""

import os
import subprocess
import sys
import shutil
import platform
from pathlib import Path
import argparse

# Importiere gemeinsame Build-Klassen
sys.path.append(str(Path(__file__).parent))
from build import BuildConfig, CrossPlatformBuildManager

class WindowsBuildManager(CrossPlatformBuildManager):
    """Spezialisierter Windows Build Manager"""
    
    def __init__(self):
        super().__init__()
        
        # Überprüfe dass wir auf Windows sind (optional)
        if not self.platform_info['is_windows']:
            print("⚠️ Hinweis: Windows Build auf nicht-Windows System")
            print("   Cross-Compilation wird versucht...")
    
    def check_windows_requirements(self):
        """Überprüft Windows-spezifische Build-Voraussetzungen"""
        print("🔍 Überprüfe Windows Build-Voraussetzungen...")
        
        # Basis-Requirements
        super().check_requirements()
        
        # Windows-spezifische Packages
        windows_packages = ['pywin32', 'pefile']
        
        for package in windows_packages:
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
    
    def create_windows_spec_file(self):
        """Erstellt Windows-optimierte PyInstaller spec-Datei"""
        print("📝 Erstelle Windows-optimierte spec-Datei...")
        
        version_info = self.get_version_info()
        icon_path = self.get_platform_icon()
        
        spec_content = f'''# Windows PyInstaller Spec für Riflescope Calculator
# Optimiert für Windows (.exe + Installer)

import os
import sys
from pathlib import Path

# Konfiguration
APP_NAME = "{self.config.APP_NAME}"
PROJECT_ROOT = Path(r"{self.project_root}")

# Windows-spezifische Datenfiles
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

# Windows-optimierte Hidden imports
hiddenimports = [
    # GUI Framework
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    
    # Windows-spezifisch
    'win32api',
    'win32con',
    'pywintypes',
    'winreg',
    
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

# Windows-spezifische Exclusions
excludes = [
    'matplotlib', 'numpy', 'pandas', 'scipy',
    'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,'''

        # Version-Info hinzufügen
        version_file = self.project_root / self.config.BUILD_DIR / "version_info.txt"
        if version_file.exists():
            spec_content += f'''
    version=r"{version_file}",'''
        
        # Icon hinzufügen
        if icon_path:
            spec_content += f'''
    icon=r"{icon_path}",'''
        
        spec_content += '''
)'''
        
        # Spec-Datei schreiben
        spec_file_path = self.project_root / self.config.SPEC_DIR / f"{self.config.APP_NAME}_windows.spec"
        spec_file_path.parent.mkdir(exist_ok=True)
        
        with open(spec_file_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        print(f"✓ Windows Spec-Datei erstellt: {spec_file_path}")
        return spec_file_path
    
    def build_windows_executable(self):
        """Erstellt Windows Executable"""
        print("🔨 Erstelle Windows Executable...")
        
        # Erstelle spec-Datei
        spec_file = self.create_windows_spec_file()
        
        # Erstelle Version-Info
        self.create_version_file()
        
        # PyInstaller ausführen
        cmd = ['pyinstaller', str(spec_file), '--log-level=WARN']
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Windows Executable erfolgreich erstellt!")
                return True
            else:
                print(f"❌ Windows Build fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Windows Build-Fehler: {e}")
            return False
    
    def create_windows_installer(self):
        """Erstellt Windows NSIS Installer"""
        print("📦 Erstelle Windows Installer...")
        
        # NSIS Script erstellen (von parent class)
        return super().create_installer_script()
    
    def create_windows_msi_installer(self):
        """Erstellt Windows MSI Installer mit WiX Toolset"""
        print("📦 Erstelle Windows MSI Installer...")
        
        # Prüfe WiX Toolset
        try:
            subprocess.run(['candle', '-?'], capture_output=True, check=True)
            print("✓ WiX Toolset verfügbar")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ WiX Toolset nicht gefunden, erstelle NSIS Installer stattdessen...")
            return self.create_nsis_installer()
        
        # WiX Source erstellen
        wxs_content = self.create_wix_source()
        wxs_file = self.project_root / self.config.BUILD_DIR / f"{self.config.APP_NAME}.wxs"
        
        with open(wxs_file, 'w', encoding='utf-8') as f:
            f.write(wxs_content)
        
        try:
            # Compile WiX
            wixobj_file = wxs_file.with_suffix('.wixobj')
            subprocess.run([
                'candle', '-out', str(wixobj_file), str(wxs_file)
            ], check=True, cwd=self.project_root)
            
            # Link MSI
            msi_file = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}-setup-x64.msi"
            subprocess.run([
                'light', '-out', str(msi_file), str(wixobj_file)
            ], check=True, cwd=self.project_root)
            
            print(f"✅ MSI Installer erstellt: {msi_file}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ MSI-Erstellung fehlgeschlagen: {e}")
            return False
    
    def create_wix_source(self):
        """Erstellt WiX XML Source für MSI"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="{self.config.APP_DISPLAY_NAME}" Language="1033" 
           Version="{self.config.APP_VERSION}" Manufacturer="{self.config.APP_AUTHOR}" 
           UpgradeCode="{{12345678-1234-1234-1234-123456789012}}">
    
    <Package InstallerVersion="200" Compressed="yes" InstallScope="perMachine" />
    
    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
    <MediaTemplate />
    
    <Feature Id="ProductFeature" Title="{self.config.APP_DISPLAY_NAME}" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
    </Feature>
  </Product>

  <Fragment>
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="{self.config.APP_DISPLAY_NAME}" />
      </Directory>
    </Directory>
  </Fragment>

  <Fragment>
    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <Component Id="MainExecutable">
        <File Id="MainExe" Source="dist\\{self.config.APP_NAME}.exe" KeyPath="yes"/>
      </Component>
    </ComponentGroup>
  </Fragment>
</Wix>'''
    
    def create_nsis_installer(self):
        """Erstellt NSIS Installer als Fallback"""
        print("📦 Erstelle NSIS Installer...")
        
        nsis_script = self.create_nsis_script()
        nsis_file = self.project_root / self.config.BUILD_DIR / f"{self.config.APP_NAME}_installer.nsi"
        
        with open(nsis_file, 'w', encoding='utf-8') as f:
            f.write(nsis_script)
        
        try:
            subprocess.run(['makensis', str(nsis_file)], check=True, cwd=self.project_root)
            print("✅ NSIS Installer erstellt")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ NSIS nicht verfügbar, überspringe Installer")
            return False
    
    def create_nsis_script(self):
        """Erstellt NSIS Script"""
        return f'''!define APP_NAME "{self.config.APP_DISPLAY_NAME}"
!define APP_VERSION "{self.config.APP_VERSION}"
!define APP_PUBLISHER "{self.config.APP_AUTHOR}"
!define APP_EXE "{self.config.APP_NAME}.exe"

Name "${{APP_NAME}}"
OutFile "dist\\${{APP_NAME}}-setup-x64.exe"
InstallDir "$PROGRAMFILES64\\${{APP_NAME}}"

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  File "dist\\${{APP_EXE}}"
  
  CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
  CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
  CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\\${{APP_EXE}}"
  Delete "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk"
  Delete "$DESKTOP\\${{APP_NAME}}.lnk"
  RMDir "$SMPROGRAMS\\${{APP_NAME}}"
  RMDir "$INSTDIR"
SectionEnd'''
    
    def create_windows_portable_zip(self):
        """Erstellt Windows Portable ZIP"""
        print("📦 Erstelle Windows Portable ZIP...")
        
        import zipfile
        
        exe_path = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}.exe"
        zip_path = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}-portable-x64.zip"
        
        if not exe_path.exists():
            print("❌ Executable nicht gefunden")
            return False
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(exe_path, f"{self.config.APP_NAME}.exe")
                
                # README für Portable
                readme_content = f"""{self.config.APP_DISPLAY_NAME} - Portable Version

Einfach die .exe ausführen - keine Installation nötig!

Version: {self.config.APP_VERSION}
Website: https://github.com/yourusername/Riflescope-Clicks-Calculator
"""
                zipf.writestr("README.txt", readme_content)
            
            print(f"✅ Portable ZIP erstellt: {zip_path}")
            return True
            
        except Exception as e:
            print(f"❌ ZIP-Erstellung fehlgeschlagen: {e}")
            return False

def main():
    """Windows Build Hauptfunktion"""
    parser = argparse.ArgumentParser(description='Windows Build für Riflescope Calculator')
    
    parser.add_argument('--clean', action='store_true', help='Bereinige vor Build')
    parser.add_argument('--test', action='store_true', help='Führe Tests durch')
    parser.add_argument('--portable', action='store_true', help='Erstelle Portable ZIP')
    parser.add_argument('--installer', action='store_true', help='Erstelle NSIS Installer')
    parser.add_argument('--msi', action='store_true', help='Erstelle MSI Installer')
    parser.add_argument('--quick', action='store_true', help='Nur Executable (schnell)')
    parser.add_argument('--keep-files', action='store_true', help='Behalte Build-Dateien')
    parser.add_argument('--no-verify', action='store_true', help='Überspringe Verifikation')
    
    args = parser.parse_args()
    
    print("🪟 Windows Build für Riflescope Calculator")
    print("=" * 45)
    
    builder = WindowsBuildManager()
    
    try:
        # 1. Windows-spezifische Voraussetzungen
        builder.check_windows_requirements()
        
        # 2. Build-Umgebung
        builder.prepare_build_environment()
        
        # 3. Tests (optional)
        if args.test and not builder.run_tests():
            return 1
        
        # 4. Windows Executable
        if not builder.build_windows_executable():
            return 1
        
        # 5. Verifikation
        if not args.no_verify and not builder.verify_executable():
            print("⚠️ Verifikation fehlgeschlagen")
        
        # 6. Zusätzliche Pakete (nur wenn nicht quick)
        if not args.quick:
            if args.portable and not builder.create_windows_portable_zip():
                print("⚠️ Portable-ZIP fehlgeschlagen")
            
            if args.msi and not builder.create_windows_msi_installer():
                print("⚠️ MSI-Installer fehlgeschlagen")
            
            if args.installer and not builder.create_nsis_installer():
                print("⚠️ NSIS-Installer fehlgeschlagen")
        
        # 7. Build-Report
        builder.create_build_report()
        
        # 8. Cleanup
        if not args.keep_files:
            builder.cleanup_build_files()
        
        print("\n🎉 Windows Build erfolgreich abgeschlossen!")
        
        # Zeige erstellte Dateien
        dist_dir = builder.project_root / builder.config.DIST_DIR
        created_files = []
        for pattern in ["*.exe", "*.msi", "*.zip"]:
            created_files.extend(dist_dir.glob(pattern))
        
        if created_files:
            print(f"\n📦 Erstellte Dateien:")
            for file_path in created_files:
                file_size = file_path.stat().st_size // (1024 * 1024)
                print(f"   {file_path.name} ({file_size} MB)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Windows Build-Fehler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
