# 🎯 Riflescope Clicks Calculator

Ein professioneller Zielfernrohr-Klicksrechner für präzises Schießen mit deutscher Benutzeroberfläche.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 Beschreibung

Diese Anwendung hilft Schützen dabei, die korrekten Zielfernrohr-Anpassungen zu berechnen, um ihre Waffe zu nullen oder für verschiedene Schussentfernungen zu kompensieren. Der Rechner konvertiert zwischen MOA (Minute of Angle), MIL (Milliradian) und Klickwerten basierend auf den Spezifikationen Ihres Zielfernrohrs.

## ✨ Features

- 🎯 **Präzise Klickberechnung** - Berechnung der benötigten Zielfernrohr-Anpassungen
- 🔫 **Waffen-Management** - Verwaltung verschiedener Waffen und deren Kaliber
- 🎯 **Munitions-Datenbank** - Speicherung und Verwaltung von Munitionsdaten
- 📏 **Entfernungs-Konfiguration** - Flexible Entfernungseinstellungen (Meter/Yards)
- 💾 **Ergebnis-Speicherung** - Speichern und Abrufen von Berechnungsergebnissen
- 🖥️ **Intuitive GUI** - Benutzerfreundliche Tkinter-Oberfläche
- 🗃️ **SQLite-Datenbank** - Lokale Datenspeicherung ohne externe Abhängigkeiten
- 📱 **Cross-Platform** - Läuft auf Windows, macOS und Linux

## 🎯 Unterstützte Einheiten

- **MOA (Minute of Angle)**: 1 MOA ≈ 1.047 Zoll bei 100 Yards
- **MIL (Milliradian)**: 1 MIL = 3.6 Zoll bei 100 Yards
- **Klicks**: Abhängig von der Zielfernrohr-Spezifikation

## 📋 Systemanforderungen

- **Python**: 3.8 oder höher (nur für Python-Ausführung)
- **Betriebssystem**: Windows 10+, macOS 10.13+, oder moderne Linux-Distribution
- **RAM**: Mindestens 512 MB
- **Speicher**: 50 MB freier Speicherplatz

## 🚀 Installation & Start

Sie haben zwei Hauptoptionen zur Verwendung der Anwendung:

### 🐍 Option 1: Python-Ausführung (Entwicklung/Source)

**Für Entwickler oder wenn Sie den Quellcode bearbeiten möchten:**

```bash
# Repository klonen
git clone https://github.com/yourusername/Riflescope-Clicks-Calculator.git
cd Riflescope-Clicks-Calculator

# Optional: Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # Linux/macOS
# oder
venv\Scripts\activate     # Windows

# Abhängigkeiten installieren (meist nicht nötig - Standard-Bibliotheken)
pip install -r requirements.txt

# 🎯 ANWENDUNG STARTEN
python run.py
```

### 📦 Option 2: Executable erstellen (Distribution)

**Für die Erstellung eigenständiger Executables ohne Python-Installation:**

```bash
# Repository klonen (falls noch nicht geschehen)
git clone https://github.com/yourusername/Riflescope-Clicks-Calculator.git
cd Riflescope-Clicks-Calculator


# 🛠️ EXECUTABLE ERSTELLEN UND STARTEN

# Interaktive Platform-Auswahl
python scripts/build.py

# Oder spezifische Plattform:
python scripts/build.py --windows    # Windows .exe
python scripts/build.py --macos      # macOS .app
python scripts/build.py --linux      # Linux Binary

# Nach dem Build finden Sie die Executables in:
# Windows: dist/riflescope-calculator.exe
# macOS: dist/Riflescope Calculator.app
# Linux: dist/riflescope-calculator
```

## 🎮 Verwendung

### Erste Schritte

1. **Waffe hinzufügen**: Gehen Sie zu `Einstellungen → Waffen` und fügen Sie Ihre Waffe hinzu
2. **Munition konfigurieren**: Fügen Sie passende Munition zu Ihrem Kaliber hinzu
3. **Entfernungen einstellen**: Konfigurieren Sie Ihre Schussentfernungen
4. **Ergebnisse speichern**: Geben Sie Nullungs-Ergebnisse für Ihre Kombinationen ein

### Hauptfunktionen

#### 1. Klicks berechnen
```
1. Wählen Sie Waffe, Munition und Entfernung
2. Geben Sie Ihre aktuelle Zielfernrohr-Position ein
3. Klicken Sie "Klicks berechnen"
4. Erhalten Sie die Anpassungsrichtung und Klickanzahl
```

#### 2. Daten verwalten
- **Waffen**: Name und Kaliber (z.B. ".308 Win", "6.5 mm")
- **Munition**: Munitionstyp und kompatibles Kaliber
- **Entfernungen**: Schussentfernungen in Meter oder Yards
- **Ergebnisse**: Gespeicherte Nullungs-Positionen

### Beispiel-Workflow

```
🔫 Waffe: "Precision Rifle" (.308 Win)
🎯 Munition: "Match Grade HPBT" (.308 Win)  
📏 Entfernung: 200m
📍 Aktuelle Position: 15 Klicks
🎯 Zielposition: 23 Klicks
➡️ Ergebnis: 8 Klicks nach rechts
```

## 🔧 Build-System (Für Entwickler)

Das Projekt bietet ein umfassendes Cross-Platform Build-System:

### Schnellstart Build

```bash
# 🎯 EINFACHSTER WEG - Interaktive Auswahl
python scripts/build.py

# Folgen Sie dem interaktiven Menü:
# 1. 🪟 Windows Build (.exe + Installer)
# 2. 🍎 macOS Build (.app Bundle)  
# 3. 🐧 Linux Build (Native Binary)
# 4. 🌍 Alle Plattformen
```

### Erweiterte Build-Optionen

```bash
# Alle Plattformen auf einmal
python scripts/build.py --all

# Spezifische Plattformen mit Optionen
python scripts/build.py --windows --installer --portable
python scripts/build.py --macos --universal --portable
python scripts/build.py --linux --appimage --portable

# Platform-spezifische Build-Scripts
python scripts/build_windows.py --installer  # Windows mit Installer
python scripts/build_mac_os.py --universal   # macOS Universal Binary
python scripts/build_linux.py --appimage     # Linux AppImage-ready
```

### Build-Optionen im Detail

| Option | Beschreibung | Verfügbar für |
|--------|--------------|---------------|
| `--clean` | Bereinigung vor Build | Alle |
| `--test` | Tests vor Build ausführen | Alle |
| `--portable` | Portable Pakete (.zip/.tar.gz) | Alle |
| `--installer` | Installer erstellen | Windows, macOS |
| `--universal` | Universal Binary (Intel + Apple Silicon) | macOS |
| `--appimage` | AppImage-ready Build | Linux |
| `--keep-files` | Build-Dateien nicht löschen | Alle |
| `--no-verify` | Verifikation überspringen | Alle |

### Nach dem Build

```bash
# Build-Ergebnisse finden Sie in:
dist/                          # Haupt-Executables
├── riflescope-calculator.exe  # Windows
├── Riflescope Calculator.app/ # macOS  
└── riflescope-calculator      # Linux

# Mit --portable Option zusätzlich:
dist/portable/                 # Portable Pakete
├── riflescope-calculator-windows.zip
├── riflescope-calculator-macos.tar.gz
└── riflescope-calculator-linux.tar.gz
```

## 📁 Projektstruktur

```
Riflescope-Clicks-Calculator/
├── src/                          # Hauptquellcode
│   ├── main.py                   # Anwendungseinstieg
│   ├── config/                   # Konfiguration
│   ├── core/                     # Kern-Module (Logger, etc.)
│   ├── database/                 # Datenbankmanagement
│   ├── gui/                      # Benutzeroberfläche
│   │   ├── main_window.py        # Hauptfenster
│   │   ├── settings_window.py    # Einstellungsfenster
│   │   └── components.py         # GUI-Komponenten
│   ├── models/                   # Datenmodelle
│   └── utils/                    # Hilfsfunktionen
├── scripts/                      # Build-Scripts
│   ├── build.py                  # Universal Build Selector
│   ├── build_windows.py          # Windows Build
│   ├── build_mac_os.py           # macOS Build
│   └── build_linux.py            # Linux Build
├── icons/                        # Anwendungs-Icons
├── database/                     # Datenbank-Dateien
├── run.py                        # Start-Script
├── LICENSE                       # MIT Lizenz
└── requirements.txt              # Python Dependencies
```

## 🧪 Tests

```bash
# Tests ausführen
python -m pytest tests/

# Mit Coverage
python -m pytest tests/ --cov=src

# Spezifische Tests
python -m pytest tests/test_calculator.py
```

## 🤝 Beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/amazing-feature`)
3. Commit deine Änderungen (`git commit -m 'Add amazing feature'`)
4. Push zum Branch (`git push origin feature/amazing-feature`)
5. Öffne eine Pull Request

### Development Guidelines

- Verwende deutsche Kommentare und UI-Texte
- Folge PEP 8 für Python-Code
- Schreibe Tests für neue Features
- Aktualisiere die Dokumentation

## 📚 Technische Details

### Architektur

- **Frontend**: Tkinter (Standard Python GUI)
- **Backend**: SQLite Datenbank
- **Logging**: Strukturiertes Logging mit Rotation
- **Configuration**: Zentrale Konfigurationsverwaltung
- **Models**: Datenmodelle für Type Safety

### Datenbank Schema

```sql
-- Waffen
CREATE TABLE weapons (
    id INTEGER PRIMARY KEY,
    weapon TEXT UNIQUE,
    caliber TEXT
);

-- Munition  
CREATE TABLE ammunition (
    id INTEGER PRIMARY KEY,
    ammunition TEXT UNIQUE,
    caliber TEXT
);

-- Entfernungen
CREATE TABLE distances (
    id INTEGER PRIMARY KEY,
    distance REAL,
    unit TEXT
);

-- Ergebnisse
CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    weapon_id INTEGER,
    ammunition_id INTEGER,
    distance_id INTEGER,
    result INTEGER,
    FOREIGN KEY (weapon_id) REFERENCES weapons (id),
    FOREIGN KEY (ammunition_id) REFERENCES ammunition (id),
    FOREIGN KEY (distance_id) REFERENCES distances (id)
);
```

## 🔒 Sicherheit

- Lokale SQLite-Datenbank (keine Netzwerk-Kommunikation)
- Keine persönlichen Daten werden übertragen
- Eingabevalidierung für alle Benutzereingaben
- Sichere Datei-Operationen

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## ⚠️ Disclaimer

Dieser Rechner dient ausschließlich Bildungs- und Freizeitzwecken. Überprüfen Sie alle Berechnungen und befolgen Sie stets die ordnungsgemäßen Waffensicherheitsverfahren. Der Autor übernimmt keine Verantwortung für die Missbrauch dieser Software.

## 📞 Support

- 🐛 **Bug Reports**: Öffne ein Issue auf GitHub
- 💡 **Feature Requests**: Diskussion in GitHub Issues
- 📧 **Direkte Fragen**: Kontaktiere über GitHub

## 🏆 Danksagungen

- Python Community für die exzellenten Standard-Bibliotheken
- PyInstaller Team für Cross-Platform Executable Support
- Alle Beta-Tester und Contributor

---

**🎯 Präzises Schießen beginnt mit präzisen Berechnungen!**
