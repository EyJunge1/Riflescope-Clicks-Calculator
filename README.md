# Zielfernrohr-Klicksrechner (Riflescope Clicks Calculator)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

Ein präzises Tool zur Berechnung der erforderlichen Klicks am Zielfernrohr basierend auf Waffe, Munition und Entfernung für Präzisionsschießen.

## 🎯 Features

### Hauptfunktionen
- **🔢 Klickberechnung**: Automatische Berechnung der erforderlichen Zielfernrohr-Anpassungen
- **🔫 Waffen-Management**: Verwaltung verschiedener Waffen mit Kaliberdaten
- **🎯 Munitions-Management**: Verwaltung verschiedener Munitionstypen
- **📏 Entfernungs-Management**: Konfiguration verschiedener Schussentfernungen
- **💾 Ergebnis-Speicherung**: Persistente Speicherung von Einstellungen und Berechnungen

### Technische Features
- **🗄️ SQLite-Datenbank**: Lokale Datenspeicherung ohne externe Abhängigkeiten
- **🖼️ GUI-Interface**: Benutzerfreundliche grafische Oberfläche mit tkinter
- **🌍 Cross-Platform**: Läuft auf Windows, macOS und Linux
- **🍎 Apple Silicon Support**: Native Unterstützung für M1/M2/M3 Macs
- **📝 Umfassendes Logging**: Detaillierte Protokollierung für Debugging und Analyse

## 🚀 Installation & Verwendung

### Option 1: Fertige Executables (Empfohlen)
Laden Sie die fertige Anwendung für Ihr System herunter:

- **🪟 Windows**: `RiflescopeCalculator.exe` oder `RiflescopeCalculator-Setup.exe`
- **🍎 macOS**: `Riflescope Clicks Calculator.app` 
- **🐧 Linux**: `RiflescopeCalculator` Binary

Einfach herunterladen und starten - keine Installation erforderlich!

### Option 2: Python-Installation (Entwickler)
```bash
# Repository klonen
git clone https://github.com/username/riflescope-clicks-calculator.git
cd riflescope-clicks-calculator

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Anwendung starten
python run.py
```

## 📖 Erste Schritte

1. **Starten Sie die Anwendung**
2. **Konfigurieren Sie Ihre Ausrüstung** über das Einstellungen-Menü:
   - Waffe hinzufügen (Kaliber, Eigenschaften)
   - Munitionstypen definieren
   - Schussentfernungen festlegen
3. **Erstellen Sie Ergebnisse** für Waffen-/Munitions-/Entfernungskombinationen
4. **Berechnen Sie Klicks** basierend auf aktueller Position und Zielentfernung

## 🔨 Executable erstellen

Das Projekt enthält ein universelles Build-Script für alle Plattformen:

```bash
# Einfaches Executable für aktuelle Plattform
python scripts/build_executable.py

# Mit Tests und Bereinigung
python scripts/build_executable.py --clean --test

# Portable Pakete erstellen
python scripts/build_executable.py --portable

# Windows Installer erstellen
python scripts/build_executable.py --installer

# Komplette Distribution (alles)
python scripts/build_executable.py --all
```

### Build-Voraussetzungen:
- Python 3.7+ 
- PyInstaller wird automatisch installiert
- Windows: pywin32 wird automatisch installiert
- macOS: macholib wird automatisch installiert
- Linux: Keine zusätzlichen Dependencies

### Unterstützte Build-Ausgaben:
- **🪟 Windows**: `.exe` + NSIS Setup-Installer
- **🍎 macOS**: `.app` Bundle (Intel + Apple Silicon)
- **🐧 Linux**: Native Binary + `.tar.gz` Pakete

### Build-Troubleshooting:
```bash
# Bei Build-Problemen:
python scripts/build_executable.py --clean --test --keep-files

# Diagnose-Tools verwenden:
python debug/diagnostic.py
python debug/standalone_tests.py
```

## 🧪 Testing & Debugging

### Test-System
```bash
# Alle Tests ausführen
python tests/run_all_tests.py

# Nur Unit-Tests
python tests/run_all_tests.py --unit

# Schnelle Funktionalitätsprüfung
python tests/run_all_tests.py --quick

# Manuelle Komponententests
python tests/run_all_tests.py --manual
```

### Debug-Tools
```bash
# Systemdiagnose bei Problemen
python debug/diagnostic.py

# Komponententests ohne GUI
python debug/standalone_tests.py

# App mit erweiterten Debug-Informationen
python debug/debug_run.py
```

## 📁 Projektstruktur

```
riflescope-clicks-calculator/
├── 📂 src/                     # 🎯 Hauptquellcode
│   ├── main.py                # 🚀 Haupteinstiegspunkt
│   ├── config/                # ⚙️ Konfiguration
│   ├── core/                  # 🔧 Kernkomponenten & Logging
│   ├── database/              # 🗄️ Datenbankschicht
│   ├── gui/                   # 🖼️ Benutzeroberfläche
│   └── utils/                 # 🛠️ Hilfsfunktionen
├── 📂 tests/                  # 🧪 Test-Suite
│   ├── unit/                  # Unit-Tests
│   ├── integration/           # Integrationstests
│   ├── fixtures/              # Test-Daten
│   └── utils/                 # Test-Hilfsfunktionen
├── 📂 debug/                  # 🔍 Debug-Tools
├── 📂 scripts/                # 🚀 Build-Automatisierung
│   └── build_executable.py   # Universal Build Script
├── 📂 database/               # 💾 Laufzeit-Datenbank
├── 📂 logs/                   # 📝 Log-Dateien
├── 📂 icons/                  # 🎨 Anwendungssymbole
├── 📄 run.py                  # 🚀 Anwendungs-Startpunkt
├── 📄 requirements.txt        # 📦 Python-Abhängigkeiten
└── 📄 README.md               # 📖 Diese Dokumentation
```

## 🛠️ Entwicklung

### Entwicklungsumgebung einrichten
```bash
# Repository klonen
git clone <repository-url>
cd riflescope-clicks-calculator

# Virtuelle Umgebung
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Dependencies installieren
pip install -r requirements.txt

# Tests erstellen
python tests/run_all_tests.py --setup
```

### Entwicklungs-Workflow
1. **Komponenten testen**: `python debug/standalone_tests.py`
2. **Unit-Tests schreiben**: In `tests/unit/`
3. **App testen**: `python debug/debug_run.py`
4. **Tests ausführen**: `python tests/run_all_tests.py`
5. **Build erstellen**: `python scripts/build_executable.py --test`

### Logging-System
```python
from src.core import main_logger

main_logger.info("Informationsnachricht")
main_logger.error("Fehlernachricht", exc_info=True)
main_logger.debug("Debug-Information")
```

## 🔧 Troubleshooting

### Erste Hilfe bei Problemen
```bash
# 1. Systemdiagnose
python debug/diagnostic.py

# 2. Komponententests
python debug/standalone_tests.py

# 3. Debug-Modus
python debug/debug_run.py

# 4. Test-Struktur prüfen
python tests/run_all_tests.py --setup
```

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| App startet nicht | `python debug/diagnostic.py` |
| Import-Fehler | `python debug/debug_run.py --no-gui` |
| Tests schlagen fehl | `python tests/run_all_tests.py --setup` |
| GUI-Framework fehlt | Linux: `sudo apt-get install python3-tk` |

## 🌟 Cross-Platform Support

### Windows
- ✅ Windows 7, 8, 10, 11 (32/64-bit)
- ✅ Standalone `.exe` ohne Installation
- ✅ NSIS Setup-Installer
- ✅ Portable ZIP-Paket

### macOS
- ✅ macOS 10.13+ (High Sierra oder neuer)
- ✅ Intel Macs (x86_64)
- ✅ Apple Silicon (M1/M2/M3 arm64)
- ✅ Native `.app` Bundle
- ✅ Portable `.tar.gz` Paket

### Linux
- ✅ Ubuntu 18.04+ / Debian 9+
- ✅ x86_64 und ARM64 (Raspberry Pi)
- ✅ Native Binary
- ✅ Portable `.tar.gz` Paket
- ✅ AppImage-ready Structure

## 🤝 Beitragen

### Pull Requests willkommen!
1. **Fork** das Repository
2. **Tests erstellen**: `python tests/run_all_tests.py --setup`
3. **Feature entwickeln** mit Tests
4. **Vollständige Tests**: `python tests/run_all_tests.py --all`
5. **Build testen**: `python scripts/build_executable.py --test`
6. **Pull Request** erstellen

### Entwicklungsstandards
- 🧪 Alle neuen Features benötigen Tests
- 📝 Code-Dokumentation in Deutsch
- 🌍 Cross-Platform Kompatibilität beachten
- 🔍 Debug-Tools nutzen für Problemdiagnose

## 📄 Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).

## 🎯 Zielgruppe

- **Präzisionsschützen**: Sportschießen, Jagd
- **Langstrecken-Schützen**: Wettkampf, Training
- **Militär & Polizei**: Taktische Anwendungen
- **Schießtrainer**: Ausbildung und Lehre

---

**Entwickelt mit ❤️ für Präzisionsschützen**

[![Made with Python](https://img.shields.io/badge/made%20with-Python-1f425f.svg)](https://python.org)
[![Cross Platform](https://img.shields.io/badge/cross-platform-success.svg)]()
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-ready-success.svg)]()

### 📞 Support & Kontakt

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/username/riflescope-clicks-calculator/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/username/riflescope-clicks-calculator/discussions)
- 📖 **Dokumentation**: [Wiki](https://github.com/username/riflescope-clicks-calculator/wiki)

### 🔄 Releases

| Version | Datum | Highlights |
|---------|-------|------------|
| v1.0.0 | 2024 | ✨ Erste stabile Version |
| | | 🌍 Cross-Platform Support |
| | | 🍎 Apple Silicon Support |
| | | 🔨 Universal Build System |
