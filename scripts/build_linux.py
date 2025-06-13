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
    
    def create_appimage(self):
        """Erstellt AppImage"""
        print("📦 Erstelle AppImage...")
        
        # AppDir-Struktur erstellen
        appdir = self.create_appimage_structure()
        if not appdir:
            return False
        
        # AppImage Tool herunterladen/verwenden
        appimage_tool = self.get_appimagetool()
        if not appimage_tool:
            print("⚠️ AppImageTool nicht verfügbar")
            return False
        
        appimage_path = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}-linux-{self.linux_info['architecture']}.AppImage"
        
        try:
            cmd = [str(appimage_tool), str(appdir), str(appimage_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Ausführbar machen
                os.chmod(appimage_path, 0o755)
                print(f"✅ AppImage erstellt: {appimage_path}")
                return True
            else:
                print(f"❌ AppImage-Erstellung fehlgeschlagen: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ AppImage-Fehler: {e}")
            return False
    
    def get_appimagetool(self):
        """Lädt AppImageTool herunter oder findet es"""
        tool_path = self.project_root / self.config.BUILD_DIR / "appimagetool"
        
        if tool_path.exists():
            return tool_path
        
        # Versuche von System zu finden
        try:
            result = subprocess.run(['which', 'appimagetool'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Download AppImageTool
        print("📥 Lade AppImageTool herunter...")
        try:
            import urllib.request
            
            url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
            urllib.request.urlretrieve(url, tool_path)
            os.chmod(tool_path, 0o755)
            
            print("✓ AppImageTool heruntergeladen")
            return tool_path
            
        except Exception as e:
            print(f"❌ Download fehlgeschlagen: {e}")
            return None
    
    def create_deb_package(self):
        """Erstellt .deb Paket"""
        print("📦 Erstelle .deb Paket...")
        
        # DEBIAN-Struktur erstellen
        deb_dir = self.project_root / self.config.BUILD_DIR / "deb_package"
        debian_dir = deb_dir / "DEBIAN"
        usr_bin = deb_dir / "usr" / "bin"
        usr_share_apps = deb_dir / "usr" / "share" / "applications"
        usr_share_icons = deb_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
        
        for dir_path in [debian_dir, usr_bin, usr_share_apps, usr_share_icons]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Binary kopieren
        binary_src = self.project_root / self.config.DIST_DIR / self.config.APP_NAME
        binary_dst = usr_bin / self.config.APP_NAME
        
        if binary_src.exists():
            shutil.copy2(binary_src, binary_dst)
            os.chmod(binary_dst, 0o755)
        else:
            print("❌ Binary nicht gefunden")
            return False
        
        # Control-Datei
        control_content = f"""Package: {self.config.APP_NAME}
Version: {self.config.APP_VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: {self.config.APP_AUTHOR} <noreply@example.com>
Description: {self.config.APP_DESCRIPTION}
 Professional Riflescope Click Calculator for precise shooting.
 Supports multiple calibers and distance calculations.
"""
        
        with open(debian_dir / "control", 'w') as f:
            f.write(control_content)
        
        # Desktop-Datei
        desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.config.APP_DISPLAY_NAME}
Comment={self.config.APP_DESCRIPTION}
Exec={self.config.APP_NAME}
Icon={self.config.APP_NAME}
Categories=Utility;Sports;
Terminal=false
"""
        
        with open(usr_share_apps / f"{self.config.APP_NAME}.desktop", 'w') as f:
            f.write(desktop_content)
        
        # Icon kopieren
        icon_src = self.get_platform_icon()
        if icon_src and Path(icon_src).exists():
            shutil.copy2(icon_src, usr_share_icons / f"{self.config.APP_NAME}.png")
        
        # .deb bauen
        deb_file = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}_{self.config.APP_VERSION}_amd64.deb"
        
        try:
            cmd = ['dpkg-deb', '--build', str(deb_dir), str(deb_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ .deb Paket erstellt: {deb_file}")
                return True
            else:
                print(f"❌ .deb-Erstellung fehlgeschlagen: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("⚠️ dpkg-deb nicht verfügbar, überspringe .deb-Erstellung")
            return False
        except Exception as e:
            print(f"❌ .deb-Fehler: {e}")
            return False
    
    def create_rpm_package(self):
        """Erstellt .rpm Paket"""
        print("📦 Erstelle .rpm Paket...")
        
        # RPM SPEC-Datei erstellen
        spec_content = f"""%define _topdir {self.project_root / self.config.BUILD_DIR / "rpm"}
%define _builddir %{{_topdir}}/BUILD
%define _sourcedir %{{_topdir}}/SOURCES
%define _rpmdir %{{_topdir}}/RPMS
%define _srcrpmdir %{{_topdir}}/SRPMS

Name: {self.config.APP_NAME}
Version: {self.config.APP_VERSION}
Release: 1
Summary: {self.config.APP_DESCRIPTION}
License: MIT
Group: Applications/Engineering
Source0: %{{name}}-%{{version}}.tar.gz

%description
{self.config.APP_DESCRIPTION}
Professional Riflescope Click Calculator for precise shooting.

%prep
%setup -q

%build
# Nothing to build - binary already compiled

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/icons/hicolor/256x256/apps

cp {self.config.APP_NAME} $RPM_BUILD_ROOT/usr/bin/
cp {self.config.APP_NAME}.desktop $RPM_BUILD_ROOT/usr/share/applications/
cp {self.config.APP_NAME}.png $RPM_BUILD_ROOT/usr/share/icons/hicolor/256x256/apps/

%files
/usr/bin/{self.config.APP_NAME}
/usr/share/applications/{self.config.APP_NAME}.desktop
/usr/share/icons/hicolor/256x256/apps/{self.config.APP_NAME}.png

%changelog
* Wed Dec 06 2024 {self.config.APP_AUTHOR} - {self.config.APP_VERSION}-1
- Initial package
"""
        
        # RPM-Verzeichnisstruktur
        rpm_topdir = self.project_root / self.config.BUILD_DIR / "rpm"
        for subdir in ["BUILD", "SOURCES", "RPMS", "SRPMS", "SPECS"]:
            (rpm_topdir / subdir).mkdir(parents=True, exist_ok=True)
        
        spec_file = rpm_topdir / "SPECS" / f"{self.config.APP_NAME}.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        # Source-Tarball erstellen
        try:
            self.create_rpm_source_tarball(rpm_topdir / "SOURCES")
            
            # RPM bauen
            cmd = ['rpmbuild', '-ba', str(spec_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # RPM-Datei finden und kopieren
                rpm_file = None
                rpms_dir = rpm_topdir / "RPMS" / "x86_64"
                for rpm in rpms_dir.glob("*.rpm"):
                    rpm_file = rpm
                    break
                
                if rpm_file:
                    final_rpm = self.project_root / self.config.DIST_DIR / f"{self.config.APP_NAME}-{self.config.APP_VERSION}-1.x86_64.rpm"
                    shutil.copy2(rpm_file, final_rpm)
                    print(f"✅ .rpm Paket erstellt: {final_rpm}")
                    return True
                else:
                    print("❌ RPM-Datei nicht gefunden")
                    return False
            else:
                print(f"❌ .rpm-Erstellung fehlgeschlagen: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("⚠️ rpmbuild nicht verfügbar, überspringe .rpm-Erstellung")
            return False
        except Exception as e:
            print(f"❌ .rpm-Fehler: {e}")
            return False
    
    def create_rpm_source_tarball(self, sources_dir):
        """Erstellt Source-Tarball für RPM"""
        import tarfile
        
        tarball_path = sources_dir / f"{self.config.APP_NAME}-{self.config.APP_VERSION}.tar.gz"
        
        with tarfile.open(tarball_path, 'w:gz') as tar:
            # Binary
            binary_path = self.project_root / self.config.DIST_DIR / self.config.APP_NAME
            if binary_path.exists():
                tar.add(binary_path, arcname=f"{self.config.APP_NAME}-{self.config.APP_VERSION}/{self.config.APP_NAME}")
            
            # Desktop-Datei
            desktop_content = f"""[Desktop Entry]
Type=Application
Name={self.config.APP_DISPLAY_NAME}
Comment={self.config.APP_DESCRIPTION}
Exec={self.config.APP_NAME}
Icon={self.config.APP_NAME}
Categories=Utility;Sports;
Terminal=false
"""
            
            import io
            desktop_info = tarfile.TarInfo(f"{self.config.APP_NAME}-{self.config.APP_VERSION}/{self.config.APP_NAME}.desktop")
            desktop_data = desktop_content.encode('utf-8')
            desktop_info.size = len(desktop_data)
            tar.addfile(desktop_info, io.BytesIO(desktop_data))
            
            # Icon
            icon_src = self.get_platform_icon()
            if icon_src and Path(icon_src).exists():
                tar.add(icon_src, arcname=f"{self.config.APP_NAME}-{self.config.APP_VERSION}/{self.config.APP_NAME}.png")

def main():
    """Linux Build Hauptfunktion"""
    parser = argparse.ArgumentParser(description='Linux Build für Riflescope Calculator')
    
    parser.add_argument('--clean', action='store_true', help='Bereinige vor Build')
    parser.add_argument('--test', action='store_true', help='Führe Tests durch')
    parser.add_argument('--portable', action='store_true', help='Erstelle Portable .tar.gz')
    parser.add_argument('--appimage', action='store_true', help='Erstelle AppImage')
    parser.add_argument('--deb', action='store_true', help='Erstelle .deb Paket')
    parser.add_argument('--rpm', action='store_true', help='Erstelle .rpm Paket')
    parser.add_argument('--quick', action='store_true', help='Nur Binary (schnell)')
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
        
        # 5. Verifikation
        if not args.no_verify and not builder.verify_executable():
            print("⚠️ Verifikation fehlgeschlagen")
        
        # 6. Zusätzliche Pakete (nur wenn nicht quick)
        if not args.quick:
            if args.appimage and not builder.create_appimage():
                print("⚠️ AppImage-Erstellung fehlgeschlagen")
            
            if args.deb and not builder.create_deb_package():
                print("⚠️ .deb-Erstellung fehlgeschlagen")
            
            if args.rpm and not builder.create_rpm_package():
                print("⚠️ .rpm-Erstellung fehlgeschlagen")
            
            if args.portable and not builder.create_linux_portable():
                print("⚠️ Portable-Paket fehlgeschlagen")
        
        # 7. Build-Report
        builder.create_build_report()
        
        # 8. Cleanup
        if not args.keep_files:
            builder.cleanup_build_files()
        
        print("\n🎉 Linux Build erfolgreich abgeschlossen!")
        
        # Zeige erstellte Dateien
        dist_dir = builder.project_root / builder.config.DIST_DIR
        created_files = []
        for pattern in [builder.config.APP_NAME, "*.AppImage", "*.deb", "*.rpm", "*.tar.gz"]:
            created_files.extend(dist_dir.glob(pattern))
        
        if created_files:
            print(f"\n📦 Erstellte Dateien:")
            for file_path in created_files:
                if file_path.is_file():
                    file_size = file_path.stat().st_size // (1024 * 1024)
                    print(f"   {file_path.name} ({file_size} MB)")
        
        # Linux-spezifische Hinweise
        binary_name = builder.config.APP_NAME
        print(f"\n📋 Linux Nächste Schritte:")
        print(f"1. Teste: ./dist/{binary_name}")
        if args.appimage:
            print(f"2. AppImage bereit für Distribution")
        if args.deb:
            print(f"3. .deb Paket für Debian/Ubuntu bereit")
        if args.rpm:
            print(f"4. .rpm Paket für Fedora/RHEL bereit")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Linux Build-Fehler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
