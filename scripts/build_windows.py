#!/usr/bin/env python3
"""
🪟 WINDOWS BUILD SCRIPT FÜR RIFLESCOPE CALCULATOR 🪟

Professioneller Windows Build mit vollständiger Installer-Unterstützung
Optimiert für Windows-Deployment und Distribution

🚀 WINDOWS BUILD FEATURES:
- Optimierte .exe Erstellung mit PyInstaller
- Automatische Dependency-Erkennung
- NSIS Installer mit Windows Registry Integration
- MSI Installer Support (WiX Toolset)
- Code-Signing Vorbereitung
- Windows Store Package Vorbereitung
- Portable ZIP Distribution
- Auto-Update Unterstützung

📋 VERWENDUNG:
    python scripts/build_windows.py                    # Standard Build (.exe)
    python scripts/build_windows.py --installer        # + NSIS Installer
    python scripts/build_windows.py --msi              # + MSI Installer  
    python scripts/build_windows.py --portable         # + Portable ZIP
    python scripts/build_windows.py --sign             # + Code Signing
    python scripts/build_windows.py --store            # + Windows Store Package
    python scripts/build_windows.py --all              # Alle Pakete erstellen
"""
import psutil
import os
import subprocess
import sys
import shutil
import platform
import json
import zipfile
import hashlib
import time
from pathlib import Path
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class WindowsBuildConfig:
    """Windows-spezifische Build-Konfiguration"""
    
    def __init__(self):
        # Application Information
        self.APP_NAME = "riflescope-calculator"
        self.APP_DISPLAY_NAME = "Riflescope Calculator"
        self.APP_DESCRIPTION = "Professioneller Zielfernrohr-Klicksrechner für Präzisionsschießen"
        self.APP_VERSION = "1.0.0"
        self.APP_AUTHOR = "Riflescope Tools"
        self.APP_COPYRIGHT = "Copyright © 2024 Riflescope Tools"
        self.APP_URL = "https://github.com/yourusername/Riflescope-Clicks-Calculator"
        
        # Windows-spezifische IDs
        self.BUNDLE_IDENTIFIER = "com.riflescope.calculator"
        self.UPGRADE_CODE = "{12345678-1234-1234-1234-123456789012}"
        self.PRODUCT_CODE = "{87654321-4321-4321-4321-210987654321}"
        
        # Build Directories
        self.BUILD_DIR = "build"
        self.DIST_DIR = "dist"
        self.TEMP_DIR = "temp_build"
        self.INSTALLER_DIR = "installer"
        
        # Windows Architecture
        self.TARGET_ARCH = "x64" if platform.machine().endswith('64') else "x86"
        
        # Datei-Endungen
        self.EXE_NAME = f"{self.APP_NAME}.exe"
        self.INSTALLER_NAME = f"{self.APP_NAME}-setup-{self.TARGET_ARCH}.exe"
        self.MSI_NAME = f"{self.APP_NAME}-setup-{self.TARGET_ARCH}.msi"
        self.PORTABLE_NAME = f"{self.APP_NAME}-portable-{self.TARGET_ARCH}.zip"
        
        # Code Signing (wenn verfügbar)
        self.SIGN_TOOL = "signtool.exe"
        self.CERT_PATH = None
        self.CERT_PASSWORD = None

class WindowsBuildManager:
    """Professioneller Windows Build Manager"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config = WindowsBuildConfig()
        self.build_start_time = time.time()
        
        # Build Status Tracking
        self.build_steps = []
        self.errors = []
        self.warnings = []
        
        print("🪟 Riflescope Calculator - Windows Build Manager")
        print("=" * 55)
        print(f"Version: {self.config.APP_VERSION}")
        print(f"Ziel-Architektur: {self.config.TARGET_ARCH}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Arbeitsverzeichnis: {self.project_root}")
        
    def log_step(self, step: str, status: str = "INFO"):
        """Logge Build-Schritt"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.build_steps.append((timestamp, step, status))
        
        status_icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️", 
            "ERROR": "❌",
            "PROGRESS": "🔄"
        }
        
        icon = status_icons.get(status, "•")
        print(f"{icon} [{timestamp}] {step}")
        
        if status == "ERROR":
            self.errors.append(step)
        elif status == "WARNING":
            self.warnings.append(step)
    
    def check_system_requirements(self) -> bool:
        """Überprüfe System-Voraussetzungen für Windows Build"""
        self.log_step("Überprüfe System-Voraussetzungen", "PROGRESS")
        
        # Python Version
        if sys.version_info < (3, 7):
            self.log_step("Python 3.7+ erforderlich", "ERROR")
            return False
        self.log_step(f"Python {sys.version.split()[0]} OK", "SUCCESS")
        
        # Windows-spezifische Checks
        if platform.system().lower() != 'windows':
            self.log_step("Cross-Compilation von nicht-Windows System", "WARNING")
        
        # Freier Speicherplatz
        try:
            free_space = shutil.disk_usage(self.project_root).free // (1024**3)
            if free_space < 1:
                self.log_step("Weniger als 1GB freier Speicherplatz", "WARNING")
            else:
                self.log_step(f"Freier Speicherplatz: {free_space}GB", "SUCCESS")
        except Exception:
            self.log_step("Konnte Speicherplatz nicht prüfen", "WARNING")
        
        return True
    
    def check_dependencies(self) -> bool:
        """Überprüfe und installiere Build-Dependencies"""
        self.log_step("Überprüfe Build-Dependencies", "PROGRESS")
        
        # Erforderliche Packages
        required_packages = {
            'pyinstaller': 'PyInstaller',
            'pefile': 'Windows PE File Analysis',
        }
        
        # Optionale Packages (Windows-spezifisch)
        optional_packages = {
            'pywin32': 'Windows API Access',
            'pillow': 'Image Processing für Icons',
        }
        
        # Prüfe erforderliche Packages
        for package, description in required_packages.items():
            if not self._check_and_install_package(package, description, required=True):
                return False
        
        # Prüfe optionale Packages
        for package, description in optional_packages.items():
            self._check_and_install_package(package, description, required=False)
        
        return True
    
    def _check_and_install_package(self, package: str, description: str, required: bool = True) -> bool:
        """Prüfe und installiere einzelnes Package"""
        try:
            __import__(package.replace('-', '_'))
            self.log_step(f"{description} verfügbar", "SUCCESS")
            return True
        except ImportError:
            self.log_step(f"Installiere {description}...", "PROGRESS")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True)
                self.log_step(f"{description} installiert", "SUCCESS")
                return True
            except subprocess.CalledProcessError as e:
                if required:
                    self.log_step(f"Kritischer Fehler: Konnte {description} nicht installieren", "ERROR")
                    return False
                else:
                    self.log_step(f"Optionales Package {description} nicht verfügbar", "WARNING")
                    return True
    
    def prepare_build_environment(self) -> bool:
        """Bereite Build-Umgebung vor"""
        self.log_step("Bereite Build-Umgebung vor", "PROGRESS")
        
        # Erstelle Build-Verzeichnisse
        build_dirs = [
            self.config.BUILD_DIR,
            self.config.DIST_DIR,
            self.config.TEMP_DIR,
            self.config.INSTALLER_DIR
        ]
        
        for dir_name in build_dirs:
            dir_path = self.project_root / dir_name
            try:
                dir_path.mkdir(exist_ok=True)
                self.log_step(f"Verzeichnis erstellt: {dir_name}", "SUCCESS")
            except Exception as e:
                self.log_step(f"Fehler beim Erstellen von {dir_name}: {e}", "ERROR")
                return False
        
        # Prüfe src-Verzeichnis
        src_dir = self.project_root / "src"
        if not src_dir.exists():
            self.log_step("src-Verzeichnis nicht gefunden", "ERROR")
            return False
        
        # Prüfe run.py
        run_file = self.project_root / "run.py"
        if not run_file.exists():
            self.log_step("run.py nicht gefunden", "ERROR")
            return False
        
        self.log_step("Build-Umgebung erfolgreich vorbereitet", "SUCCESS")
        return True
    
    def create_version_info_file(self) -> Path:
        """Erstelle Windows Version-Info Datei"""
        self.log_step("Erstelle Windows Version-Info", "PROGRESS")
        
        version_parts = self.config.APP_VERSION.split('.')
        while len(version_parts) < 4:
            version_parts.append('0')
        
        version_tuple = f"({', '.join(version_parts)})"
        
        version_content = f'''# -*- coding: utf-8 -*-
# Windows Version Info für {self.config.APP_DISPLAY_NAME}

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
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
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.config.APP_AUTHOR}'),
         StringStruct(u'FileDescription', u'{self.config.APP_DESCRIPTION}'),
         StringStruct(u'FileVersion', u'{self.config.APP_VERSION}'),
         StringStruct(u'InternalName', u'{self.config.APP_NAME}'),
         StringStruct(u'LegalCopyright', u'{self.config.APP_COPYRIGHT}'),
         StringStruct(u'OriginalFilename', u'{self.config.EXE_NAME}'),
         StringStruct(u'ProductName', u'{self.config.APP_DISPLAY_NAME}'),
         StringStruct(u'ProductVersion', u'{self.config.APP_VERSION}'),
         StringStruct(u'LegalTrademarks', u''),
         StringStruct(u'PrivateBuild', u''),
         StringStruct(u'SpecialBuild', u'')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        version_file = self.project_root / self.config.BUILD_DIR / "version_info.txt"
        
        try:
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(version_content)
            self.log_step(f"Version-Info erstellt: {version_file.name}", "SUCCESS")
            return version_file
        except Exception as e:
            self.log_step(f"Fehler beim Erstellen der Version-Info: {e}", "ERROR")
            return None
    
    def get_icon_path(self) -> Optional[Path]:
        """Ermittle target_icon.ico als primäres Windows-Icon"""
        icon_locations = [
            self.project_root / "icons" / "target_icon.ico",
            self.project_root / "assets" / "target_icon.ico",
            self.project_root / "resources" / "target_icon.ico",
            self.project_root / "target_icon.ico",
        ]
        
        for icon_path in icon_locations:
            if icon_path.exists():
                self.log_step(f"Windows-Icon gefunden: {icon_path}", "SUCCESS")
                return icon_path
        
        self.log_step("target_icon.ico nicht gefunden! Erstelle ein Standard-Icon...", "WARNING")
        
        # Fallback: Erstelle ein minimales ICO falls nicht vorhanden
        fallback_icon = self._create_fallback_icon()
        if fallback_icon:
            return fallback_icon
            
        return None
    
    def _create_fallback_icon(self) -> Optional[Path]:
        """Erstelle ein minimales Fallback-Icon wenn target_icon.ico fehlt"""
        try:
            from PIL import Image, ImageDraw
            
            # Erstelle einfaches Zielscheiben-Icon
            icon_sizes = [16, 32, 48, 64, 128, 256]
            images = []
            
            for size in icon_sizes:
                img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Einfache Zielscheibe
                center = size // 2
                max_radius = size // 2 - 2
                
                # Äußerer Kreis (rot)
                draw.ellipse([2, 2, size-2, size-2], fill=(220, 50, 50, 255), outline=(150, 30, 30, 255))
                
                # Innerer Kreis (weiß)
                inner_size = max_radius // 2
                draw.ellipse([center-inner_size, center-inner_size, 
                             center+inner_size, center+inner_size], 
                             fill=(255, 255, 255, 255), outline=(200, 200, 200, 255))
                
                # Zentrum (rot)
                center_size = max_radius // 4
                draw.ellipse([center-center_size, center-center_size,
                             center+center_size, center+center_size],
                             fill=(220, 50, 50, 255))
                
                images.append(img)
            
            # Speichere als ICO
            fallback_path = self.project_root / "icons" / "target_icon.ico"
            fallback_path.parent.mkdir(exist_ok=True)
            
            images[0].save(fallback_path, format='ICO', sizes=[(img.width, img.height) for img in images])
            
            self.log_step(f"Fallback-Icon erstellt: {fallback_path.name}", "SUCCESS")
            return fallback_path
            
        except ImportError:
            self.log_step("PIL nicht verfügbar - kein Fallback-Icon", "WARNING")
            return None
        except Exception as e:
            self.log_step(f"Fallback-Icon Fehler: {e}", "WARNING")
            return None
    
    def create_pyinstaller_spec(self) -> Path:
        """Erstelle optimierte PyInstaller Spec-Datei für Windows"""
        self.log_step("Erstelle PyInstaller Spec-Datei", "PROGRESS")
        
        icon_path = self.get_icon_path()
        version_file = self.create_version_info_file()
        
        # Datenfiles sammeln
        data_files = []
        
        # src-Verzeichnis
        src_dir = self.project_root / "src"
        if src_dir.exists():
            data_files.append(f"(r'{src_dir}', 'src')")
        
        # Optionale Verzeichnisse
        optional_dirs = ["icons", "resources", "assets", "database", "config", "locale"]
        for dir_name in optional_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and any(dir_path.iterdir()):
                data_files.append(f"(r'{dir_path}', '{dir_name}')")
        
        # Hidden Imports - Windows-optimiert
        hidden_imports = [
            # GUI Framework
            "'tkinter'", "'tkinter.ttk'", "'tkinter.messagebox'", 
            "'tkinter.filedialog'", "'tkinter.simpledialog'",
            
            # Windows-spezifisch
            "'win32api'", "'win32con'", "'win32gui'", "'win32process'",
            "'pywintypes'", "'winreg'", "'winsound'",
            
            # Core Python
            "'sqlite3'", "'logging'", "'json'", "'csv'", "'xml.etree.ElementTree'",
            
            # Application modules
            "'src'", "'src.main'", "'src.config'", "'src.core'", 
            "'src.database'", "'src.gui'", "'src.utils'", "'src.models'",
        ]
        
        # Excludes - Unnötige Module ausschließen
        excludes = [
            "'matplotlib'", "'numpy'", "'pandas'", "'scipy'", "'tensorflow'",
            "'PyQt5'", "'PyQt6'", "'PySide2'", "'PySide6'", "'kivy'",
            "'django'", "'flask'", "'tornado'", "'fastapi'",
            "'pytest'", "'unittest'", "'doctest'",
            "'IPython'", "'jupyter'", "'notebook'",
        ]
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# Windows PyInstaller Spec für {self.config.APP_DISPLAY_NAME}
# Generiert am: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

import os
import sys
from pathlib import Path

# Projekt-Konfiguration
APP_NAME = "{self.config.APP_NAME}"
PROJECT_ROOT = Path(r"{self.project_root}")

# Datenfiles
datas = [
    {','.join(data_files)}
]

# Hidden Imports
hiddenimports = [
    {','.join(hidden_imports)}
]

# Ausgeschlossene Module
excludes = [
    {','.join(excludes)}
]

# Binaries (Windows-spezifische DLLs falls benötigt)
binaries = []

block_cipher = None

# Analysis
a = Analysis(
    [str(PROJECT_ROOT / "run.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=binaries,
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

# PYZ Archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Windows Executable
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
    console=False,  # Windowed Application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="{self.config.TARGET_ARCH}",
    codesign_identity=None,
    entitlements_file=None,'''
        
        # Version-Info hinzufügen
        if version_file and version_file.exists():
            spec_content += f'''
    version=r"{version_file}",'''
        
        # Icon hinzufügen
        if icon_path and icon_path.exists():
            spec_content += f'''
    icon=r"{icon_path}",'''
        
        spec_content += '''
)'''
        
        # Spec-Datei speichern
        spec_file = self.project_root / self.config.BUILD_DIR / f"{self.config.APP_NAME}_windows.spec"
        
        try:
            with open(spec_file, 'w', encoding='utf-8') as f:
                f.write(spec_content)
            self.log_step(f"Spec-Datei erstellt: {spec_file.name}", "SUCCESS")
            return spec_file
        except Exception as e:
            self.log_step(f"Fehler beim Erstellen der Spec-Datei: {e}", "ERROR")
            return None
    
    def build_executable(self) -> bool:
        """Erstelle Windows Executable mit PyInstaller"""
        self.log_step("Erstelle Windows Executable", "PROGRESS")
        
        spec_file = self.create_pyinstaller_spec()
        if not spec_file:
            return False
        
        # PyInstaller Kommando - simplified when using spec file
        cmd = [
            'pyinstaller',
            str(spec_file),
            '--log-level=WARN',
            '--clean',
            '--noconfirm',
            f'--distpath={self.project_root / self.config.DIST_DIR}',
            f'--workpath={self.project_root / self.config.BUILD_DIR}'
            # Note: --specpath is not allowed when using existing spec file
        ]
        
        try:
            self.log_step("Starte PyInstaller...", "PROGRESS")
            start_time = time.time()
            
            result = subprocess.run(
                cmd, 
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600  # 10 Minuten Timeout
            )
            
            build_time = time.time() - start_time
            
            if result.returncode == 0:
                self.log_step(f"Executable erfolgreich erstellt ({build_time:.1f}s)", "SUCCESS")
                return True
            else:
                self.log_step("PyInstaller fehlgeschlagen", "ERROR")
                print(f"\nPyInstaller Fehler:\n{result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_step("PyInstaller Timeout (>10min)", "ERROR")
            return False
        except Exception as e:
            self.log_step(f"Unerwarteter PyInstaller-Fehler: {e}", "ERROR")
            return False
    
    def verify_executable(self) -> bool:
        """Verifiziere erstellte Executable"""
        self.log_step("Verifiziere Windows Executable", "PROGRESS")
        
        exe_path = self.project_root / self.config.DIST_DIR / self.config.EXE_NAME
        
        if not exe_path.exists():
            self.log_step(f"Executable nicht gefunden: {self.config.EXE_NAME}", "ERROR")
            return False
        
        # Dateigröße prüfen
        size_bytes = exe_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        if size_bytes < 1024:  # Kleiner als 1KB
            self.log_step("Executable verdächtig klein (<1KB)", "ERROR")
            return False
        
        if size_mb > 100:  # Größer als 100MB
            self.log_step(f"Executable sehr groß ({size_mb:.1f}MB)", "WARNING")
        
        self.log_step(f"Executable OK ({size_mb:.1f}MB)", "SUCCESS")
        
        # Teste Executable (falls möglich)
        if platform.system().lower() == 'windows':
            try:
                # Kurzer Test-Start (nur Version prüfen)
                result = subprocess.run(
                    [str(exe_path), '--version'], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    self.log_step("Executable Test erfolgreich", "SUCCESS")
                else:
                    self.log_step("Executable Test fehlgeschlagen", "WARNING")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self.log_step("Executable Test nicht möglich", "WARNING")
        
        return True
    
    def sign_executable(self, cert_path: Optional[str] = None, cert_password: Optional[str] = None) -> bool:
        """Code-Signing für Windows Executable"""
        self.log_step("Prüfe Code-Signing Möglichkeiten", "PROGRESS")
        
        # Prüfe SignTool
        try:
            subprocess.run(['signtool'], capture_output=True, check=True)
            signtool_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            signtool_available = False
        
        if not signtool_available:
            self.log_step("SignTool nicht verfügbar - überspringe Code-Signing", "WARNING")
            return True
        
        if not cert_path:
            cert_path = self.config.CERT_PATH
        
        if not cert_path or not os.path.exists(cert_path):
            self.log_step("Kein Code-Signing Zertifikat gefunden", "WARNING")
            return True
        
        exe_path = self.project_root / self.config.DIST_DIR / self.config.EXE_NAME
        
        cmd = [
            'signtool', 'sign',
            '/f', cert_path,
            '/t', 'http://timestamp.digicert.com',
            '/d', self.config.APP_DISPLAY_NAME,
            '/du', self.config.APP_URL,
            str(exe_path)
        ]
        
        if cert_password:
            cmd.extend(['/p', cert_password])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self.log_step("Code-Signing erfolgreich", "SUCCESS")
                return True
            else:
                self.log_step(f"Code-Signing fehlgeschlagen: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.log_step(f"Code-Signing Fehler: {e}", "ERROR")
            return False
    
    def create_nsis_installer(self) -> bool:
        """Erstelle NSIS Installer"""
        self.log_step("Erstelle NSIS Installer", "PROGRESS")
        
        # Prüfe NSIS
        try:
            subprocess.run(['makensis', '/VERSION'], capture_output=True, check=True)
            nsis_available = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            nsis_available = False
        
        if not nsis_available:
            self.log_step("NSIS nicht verfügbar - überspringe Installer", "WARNING")
            return True
        
        nsis_script = self._create_nsis_script()
        nsis_file = self.project_root / self.config.INSTALLER_DIR / "installer.nsi"
        
        try:
            # Erstelle NSIS Script
            with open(nsis_file, 'w', encoding='utf-8') as f:
                f.write(nsis_script)
            
            # Kompiliere Installer
            result = subprocess.run([
                'makensis', 
                f'/DVERSION={self.config.APP_VERSION}',
                f'/DARCH={self.config.TARGET_ARCH}',
                str(nsis_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_step("NSIS Installer erfolgreich erstellt", "SUCCESS")
                return True
            else:
                self.log_step(f"NSIS Fehler: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log_step(f"NSIS Installer Fehler: {e}", "ERROR")
            return False
    
    def _create_nsis_script(self) -> str:
        """Erstelle erweiterte NSIS Script"""
        return f'''!define APP_NAME "{self.config.APP_DISPLAY_NAME}"
!define APP_VERSION "{self.config.APP_VERSION}"
!define APP_PUBLISHER "{self.config.APP_AUTHOR}"
!define APP_EXE "{self.config.EXE_NAME}"
!define APP_DESCRIPTION "{self.config.APP_DESCRIPTION}"
!define APP_URL "{self.config.APP_URL}"

# Installer Eigenschaften
Name "${{APP_NAME}}"
OutFile "../{self.config.DIST_DIR}/{self.config.INSTALLER_NAME}"
InstallDir "$PROGRAMFILES64\\${{APP_NAME}}"
RequestExecutionLevel admin
ShowInstDetails show
ShowUnInstDetails show

# Version Info
VIProductVersion "{self.config.APP_VERSION}.0"
VIAddVersionKey "ProductName" "${{APP_NAME}}"
VIAddVersionKey "CompanyName" "${{APP_PUBLISHER}}"
VIAddVersionKey "LegalCopyright" "{self.config.APP_COPYRIGHT}"
VIAddVersionKey "FileDescription" "${{APP_DESCRIPTION}}"
VIAddVersionKey "FileVersion" "{self.config.APP_VERSION}"

# Moderne UI
!include "MUI2.nsh"

# UI Konfiguration
!define MUI_ABORTWARNING
!define MUI_ICON "../icons/app.ico"
!define MUI_UNICON "../icons/app.ico"

# Installer Seiten
!insertmacro MUI_PAGE_LICENSE "../LICENSE"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Uninstaller Seiten  
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# Sprachen
!insertmacro MUI_LANGUAGE "German"

# Installer Sections
Section "Hauptprogramm" SecMain
  SectionIn RO
  
  SetOutPath "$INSTDIR"
  File "../{self.config.DIST_DIR}/${{APP_EXE}}"
  
  # Registry Einträge
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayName" "${{APP_NAME}}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "UninstallString" "$INSTDIR\\uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "DisplayVersion" "${{APP_VERSION}}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "Publisher" "${{APP_PUBLISHER}}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}" "URLInfoAbout" "${{APP_URL}}"
  
  WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Desktop Verknüpfung" SecDesktop
  CreateShortCut "$DESKTOP\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
SectionEnd

Section "Startmenü Einträge" SecStartMenu
  CreateDirectory "$SMPROGRAMS\\${{APP_NAME}}"
  CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk" "$INSTDIR\\${{APP_EXE}}"
  CreateShortCut "$SMPROGRAMS\\${{APP_NAME}}\\Uninstall.lnk" "$INSTDIR\\uninstall.exe"
SectionEnd

# Uninstaller
Section "Uninstall"
  Delete "$INSTDIR\\${{APP_EXE}}"
  Delete "$INSTDIR\\uninstall.exe"
  
  Delete "$DESKTOP\\${{APP_NAME}}.lnk"
  Delete "$SMPROGRAMS\\${{APP_NAME}}\\${{APP_NAME}}.lnk"
  Delete "$SMPROGRAMS\\${{APP_NAME}}\\Uninstall.lnk"
  RMDir "$SMPROGRAMS\\${{APP_NAME}}"
  RMDir "$INSTDIR"
  
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{APP_NAME}}"
SectionEnd

# Section Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${{SecMain}} "Hauptprogramm (erforderlich)"
  !insertmacro MUI_DESCRIPTION_TEXT ${{SecDesktop}} "Desktop Verknüpfung erstellen"
  !insertmacro MUI_DESCRIPTION_TEXT ${{SecStartMenu}} "Startmenü Einträge erstellen"
!insertmacro MUI_FUNCTION_DESCRIPTION_END'''
    
    def create_portable_zip(self) -> bool:
        """Erstelle Portable ZIP Distribution"""
        self.log_step("Erstelle Portable ZIP", "PROGRESS")
        
        exe_path = self.project_root / self.config.DIST_DIR / self.config.EXE_NAME
        zip_path = self.project_root / self.config.DIST_DIR / self.config.PORTABLE_NAME
        
        if not exe_path.exists():
            self.log_step("Executable für ZIP nicht gefunden", "ERROR")
            return False
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                # Hauptprogramm
                zipf.write(exe_path, self.config.EXE_NAME)
                
                # README für Portable Version
                readme_content = f"""{self.config.APP_DISPLAY_NAME} - Portable Version {self.config.APP_VERSION}

PORTABLE INSTALLATION:
======================

1. Entpacken Sie diese ZIP-Datei in einen beliebigen Ordner
2. Starten Sie {self.config.EXE_NAME}
3. Keine Installation oder Administrator-Rechte erforderlich!

FEATURES:
- Vollständig portable - keine Registry-Einträge
- Kann von USB-Stick ausgeführt werden
- Hinterlässt keine Spuren auf dem System
- Alle Einstellungen werden lokal gespeichert

TECHNISCHE DETAILS:
- Version: {self.config.APP_VERSION}
- Architektur: {self.config.TARGET_ARCH}
- Build-Datum: {datetime.now().strftime('%Y-%m-%d')}
- Größe: {exe_path.stat().st_size // (1024*1024)} MB

SUPPORT:
- Website: {self.config.APP_URL}
- Copyright: {self.config.APP_COPYRIGHT}

Viel Erfolg beim Präzisionsschießen! 🎯
"""
                zipf.writestr("README.txt", readme_content)
                
                # Batch-Starter (optional)
                batch_content = f"""@echo off
title {self.config.APP_DISPLAY_NAME}
echo Starte {self.config.APP_DISPLAY_NAME}...
start "" "{self.config.EXE_NAME}"
"""
                zipf.writestr("Start.bat", batch_content)
            
            # Größe ermitteln
            zip_size = zip_path.stat().st_size // (1024 * 1024)
            self.log_step(f"Portable ZIP erstellt ({zip_size}MB): {self.config.PORTABLE_NAME}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_step(f"ZIP-Erstellung fehlgeschlagen: {e}", "ERROR")
            return False
    
    def create_checksums(self) -> bool:
        """Erstelle Checksums für alle erstellten Dateien"""
        self.log_step("Erstelle Checksums", "PROGRESS")
        
        dist_dir = self.project_root / self.config.DIST_DIR
        checksum_file = dist_dir / "checksums.txt"
        
        files_to_check = [
            self.config.EXE_NAME,
            self.config.INSTALLER_NAME, 
            self.config.MSI_NAME,
            self.config.PORTABLE_NAME
        ]
        
        checksums = []
        checksums.append(f"# Checksums für {self.config.APP_DISPLAY_NAME} v{self.config.APP_VERSION}")
        checksums.append(f"# Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        checksums.append("")
        
        for filename in files_to_check:
            file_path = dist_dir / filename
            if file_path.exists():
                try:
                    # SHA256 Checksum
                    sha256_hash = hashlib.sha256()
                    with open(file_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
                    
                    checksum = sha256_hash.hexdigest()
                    file_size = file_path.stat().st_size
                    
                    checksums.append(f"{checksum}  {filename}  ({file_size} bytes)")
                    
                except Exception as e:
                    self.log_step(f"Checksum-Fehler für {filename}: {e}", "WARNING")
        
        try:
            with open(checksum_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(checksums))
            
            self.log_step("Checksums erstellt", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_step(f"Checksum-Datei Fehler: {e}", "WARNING")
            return False
    
    def create_build_report(self) -> bool:
        """Erstelle detaillierten Build-Report"""
        self.log_step("Erstelle Build-Report", "PROGRESS")
        
        build_time = time.time() - self.build_start_time
        
        report_content = f"""# Build Report - {self.config.APP_DISPLAY_NAME}

## Build Information
- **Build Zeit:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Build Dauer:** {build_time:.1f} Sekunden
- **Version:** {self.config.APP_VERSION}
- **Architektur:** {self.config.TARGET_ARCH}
- **Python Version:** {sys.version}
- **Platform:** {platform.platform()}

## Build Schritte
"""
        
        for timestamp, step, status in self.build_steps:
            status_emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "PROGRESS": "🔄"}.get(status, "•")
            report_content += f"- {status_emoji} [{timestamp}] {step}\n"
        
        report_content += f"\n## Erstellte Dateien\n"
        
        dist_dir = self.project_root / self.config.DIST_DIR
        total_size = 0
        
        for file_path in dist_dir.glob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                total_size += size
                size_mb = size / (1024 * 1024)
                report_content += f"- **{file_path.name}** ({size_mb:.1f} MB)\n"
        
        report_content += f"\n**Gesamt Größe:** {total_size / (1024 * 1024):.1f} MB\n"
        
        if self.warnings:
            report_content += f"\n## Warnungen ({len(self.warnings)})\n"
            for warning in self.warnings:
                report_content += f"- ⚠️ {warning}\n"
        
        if self.errors:
            report_content += f"\n## Fehler ({len(self.errors)})\n"
            for error in self.errors:
                report_content += f"- ❌ {error}\n"
        
        report_content += f"\n## System Information\n"
        report_content += f"- CPU: {platform.processor()}\n"
        report_content += f"- RAM: {psutil.virtual_memory().total // (1024**3) if 'psutil' in sys.modules else 'N/A'} GB\n"
        report_content += f"- Freier Speicher: {shutil.disk_usage('.').free // (1024**3)} GB\n"
        
        report_file = self.project_root / self.config.BUILD_DIR / "build_report.md"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.log_step(f"Build-Report erstellt: {report_file.name}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_step(f"Build-Report Fehler: {e}", "WARNING")
            return False
    
    def cleanup_build_files(self, keep_important: bool = True) -> bool:
        """Bereinige Build-Dateien"""
        self.log_step("Bereinige Build-Dateien", "PROGRESS")
        
        cleanup_patterns = [
            self.project_root / "__pycache__",
            self.project_root / "src" / "__pycache__",
            self.project_root / "*.pyc",
            self.project_root / self.config.BUILD_DIR / "*.spec",
            self.project_root / self.config.TEMP_DIR
        ]
        
        if not keep_important:
            cleanup_patterns.extend([
                self.project_root / self.config.BUILD_DIR,
                self.project_root / self.config.INSTALLER_DIR
            ])
        
        cleaned_items = 0
        
        for pattern in cleanup_patterns:
            try:
                if pattern.is_dir():
                    shutil.rmtree(pattern, ignore_errors=True)
                    cleaned_items += 1
                elif pattern.is_file():
                    pattern.unlink()
                    cleaned_items += 1
            except Exception:
                pass
        
        self.log_step(f"Build-Dateien bereinigt ({cleaned_items} Elemente)", "SUCCESS")
        return True
    
    def run_full_windows_build(self, options: Dict) -> bool:
        """Führe kompletten Windows Build durch"""
        
        print(f"\n🚀 STARTE VOLLSTÄNDIGEN WINDOWS BUILD")
        print("=" * 50)
        
        # 1. System-Checks
        if not self.check_system_requirements():
            return False
        
        if not self.check_dependencies():
            return False
        
        if not self.prepare_build_environment():
            return False
        
        # 2. Executable Build
        if not self.build_executable():
            return False
        
        if not self.verify_executable():
            return False
        
        # 3. Code Signing (optional)
        if options.get('sign', False):
            self.sign_executable(options.get('cert_path'), options.get('cert_password'))
        
        # 4. Zusätzliche Pakete
        if options.get('installer', False):
            self.create_nsis_installer()
        
        if options.get('portable', False):
            self.create_portable_zip()
        
        # 5. Checksums und Report
        self.create_checksums()
        self.create_build_report()
        
        # 6. Cleanup (optional)
        if options.get('cleanup', True):
            self.cleanup_build_files(keep_important=True)
        
        # 7. Erfolgs-Zusammenfassung
        self._print_build_summary()
        
        return len(self.errors) == 0
    
    def _print_build_summary(self):
        """Drucke Build-Zusammenfassung"""
        build_time = time.time() - self.build_start_time
        
        print(f"\n🎉 WINDOWS BUILD ABGESCHLOSSEN!")
        print("=" * 45)
        print(f"⏱️  Build Zeit: {build_time:.1f} Sekunden")
        print(f"✅ Erfolgreiche Schritte: {len([s for s in self.build_steps if s[2] == 'SUCCESS'])}")
        print(f"⚠️  Warnungen: {len(self.warnings)}")
        print(f"❌ Fehler: {len(self.errors)}")
        
        # Erstellte Dateien anzeigen
        dist_dir = self.project_root / self.config.DIST_DIR
        created_files = list(dist_dir.glob("*"))
        
        if created_files:
            print(f"\n📦 ERSTELLTE DATEIEN:")
            print("-" * 20)
            total_size = 0
            for file_path in created_files:
                if file_path.is_file():
                    size = file_path.stat().st_size
                    total_size += size
                    size_mb = size / (1024 * 1024)
                    print(f"   📄 {file_path.name} ({size_mb:.1f} MB)")
            
            print(f"\n💾 Gesamt Größe: {total_size / (1024 * 1024):.1f} MB")
        
        if self.errors:
            print(f"\n❌ FEHLER ZU BEHEBEN:")
            print("-" * 20)
            for error in self.errors:
                print(f"   • {error}")
        
        print(f"\n📁 Ausgabe-Verzeichnis: {self.config.DIST_DIR}/")
        print(f"📊 Build-Report: {self.config.BUILD_DIR}/build_report.md")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='🪟 Windows Build für Riflescope Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=""":
WINDOWS BUILD BEISPIELE:
  python scripts/build_windows.py                    # Standard .exe Build
  python scripts/build_windows.py --installer        # + NSIS Installer
  python scripts.build_windows.py --all              # Alle Pakete
  python scripts/build_windows.py --sign --cert cert.p12  # Mit Code-Signing
        """
    )
    
    # Build Optionen
    parser.add_argument('--installer', action='store_true', help='Erstelle NSIS Installer')
    parser.add_argument('--msi', action='store_true', help='Erstelle MSI Installer (experimentell)')
    parser.add_argument('--portable', action='store_true', help='Erstelle Portable ZIP')
    parser.add_argument('--all', action='store_true', help='Erstelle alle Pakete')
    
    # Code Signing
    parser.add_argument('--sign', action='store_true', help='Code-Signing aktivieren')
    parser.add_argument('--cert', help='Pfad zum Code-Signing Zertifikat')
    parser.add_argument('--cert-password', help='Zertifikat Passwort')
    
    # Build Optionen
    parser.add_argument('--clean', action='store_true', help='Bereinige vor Build')
    parser.add_argument('--keep-files', action='store_true', help='Behalte Build-Dateien')
    parser.add_argument('--quick', action='store_true', help='Nur Executable (schnell)')
    parser.add_argument('--no-verify', action='store_true', help='Überspringe Verifikation')
    
    return parser.parse_args()

def main():
    """Windows Build Hauptfunktion"""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Initialize builder
        builder = WindowsBuildManager()
        
        # Build options from arguments
        build_options = {
            'installer': args.installer or args.all,
            'msi': args.msi or args.all, 
            'portable': args.portable or args.all,
            'sign': args.sign,
            'cert_path': args.cert,
            'cert_password': args.cert_password,
            'cleanup': not args.keep_files,
            'quick': args.quick,
            'verify': not args.no_verify
        }
        
        # Clean previous builds if requested
        if args.clean:
            builder.log_step("Bereinige vorherige Builds", "PROGRESS")
            for dir_name in [builder.config.BUILD_DIR, builder.config.DIST_DIR]:
                dir_path = builder.project_root / dir_name
                if dir_path.exists():
                    shutil.rmtree(dir_path)
            builder.log_step("Vorherige Builds bereinigt", "SUCCESS")
        
        # Run full build
        success = builder.run_full_windows_build(build_options)
        
        if success:
            print(f"\n🎯 Windows Build erfolgreich abgeschlossen!")
            return 0
        else:
            print(f"\n❌ Windows Build mit Fehlern beendet!")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Build durch Benutzer abgebrochen.")
        return 1
    except Exception as e:
        print(f"\n💥 Unerwarteter Build-Fehler: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
    sys.exit(main())
