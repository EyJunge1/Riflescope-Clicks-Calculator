# 🎯 Riflescope Clicks Calculator

Ein Zielfernrohr-Klicksrechner für präzises Schießen mit Benutzeroberfläche.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📖 Beschreibung

Diese Anwendung hilft Schützen dabei, die korrekten Zielfernrohr-Anpassungen zu berechnen, um ihre Waffe zu nullen oder für verschiedene Schussentfernungen zu kompensieren.

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

## 🚀 Installation & Start

### 📋 Systemvoraussetzungen

| Betriebssystem | Minimum | Empfohlen | Build-Status |
|----------------|---------|-----------|--------------|
| **🪟 Windows** | Windows 10 | Windows 11 | ✅ **Vollständig unterstützt** |
| **🍎 macOS** | macOS 10.15+ | macOS 13+ | 🔄 **Bald verfügbar** |
| **🐧 Linux** | Ubuntu 20.04+ | Ubuntu 24.04+ | 🔄 **Bald verfügbar** |

> 📢 **Aktueller Status**: Das Build-System unterstützt derzeit vollständig nur Windows. Unterstützung für macOS und Linux wird in Kürze hinzugefügt!

## 💾 Installations-Optionen

### 🏆 Option 1: Fertige Windows-Anwendung (Empfohlen)

> ⚡ **Schnellste Installation** - Ein Download, sofort einsatzbereit

#### 📦 Verfügbare Downloads

| Plattform | Download | Größe | Status |
|-----------|----------|-------|--------|
| 🪟 **Windows (Setup)** | [Setup.exe](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-setup-x64.exe) | 25 MB | ✅ **Verfügbar** |
| 🪟 **Windows (Portable)** | [Portable.zip](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-portable-x64.zip) | 23 MB | ✅ **Verfügbar** |
| 🍎 **macOS** | App.dmg | ~28 MB | 🔄 **In Entwicklung** |
| 🐧 **Linux (AppImage)** | AppImage | ~27 MB | 🔄 **In Entwicklung** |
| 🐧 **Linux (deb)** | .deb | ~25 MB | 🔄 **In Entwicklung** |
| 🐧 **Linux (rpm)** | .rpm | ~25 MB | 🔄 **In Entwicklung** |

> 💡 **Hinweis**: macOS und Linux Builds werden bald verfügbar sein. In der Zwischenzeit können Sie die Python-Version verwenden.

---

### 🐍 Option 2: Python-Ausführung (Alle Plattformen)

> 🔧 **Sofort verfügbar** - Funktioniert auf allen Plattformen

#### Schnellstart (benötigt nur Python)
```bash
# Repository klonen
git clone https://github.com/yourusername/Riflescope-Clicks-Calculator.git
cd Riflescope-Clicks-Calculator

# Direkt starten (keine Installation erforderlich)
python run.py        # Windows
python3 run.py       # Linux/macOS
```

#### Mit Virtual Environment (empfohlen)
```bash
# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Abhängigkeiten installieren (falls vorhanden)
pip install -r requirements.txt

# Starten
python run.py
```

---

### ⚙️ Option 3: Eigene Builds erstellen

> 🛠️ **Für Entwickler** - Erstelle eigene Distributionen

#### Aktuell verfügbare Builds

```bash
# Windows Build (vollständig unterstützt)
python scripts/build.py --windows                       # Standard: .exe + .zip
python scripts/build.py --windows --all                 # Alle Windows Pakete
python scripts/build.py --windows --installer           # .exe + .zip + NSIS Installer
python scripts/build.py --windows --portable-only       # Nur .zip (schnell)
python scripts/build.py --windows --exe-only            # Nur .exe (sehr schnell)
```

#### Bald verfügbare Builds

```bash
# macOS Build (in Entwicklung)
python scripts/build.py --macos                         # Standard: .app + .dmg
python scripts/build.py --macos --all                   # Alle macOS Pakete

# Linux Build (in Entwicklung)  
python scripts/build.py --linux                         # Standard: Binary + .deb
python scripts/build.py --linux --all                   # Alle Linux Pakete
```

#### Windows Build-Optionen im Detail

| Option | Beschreibung | Status |
|--------|--------------|:------:|
| `--windows` | Standard Windows Build (.exe + .zip) | ✅ |
| `--installer` | NSIS Installer erstellen | ✅ |
| `--msi` | MSI Installer erstellen | ✅ |
| `--portable-only` | Nur Portable ZIP | ✅ |
| `--exe-only` | Nur Executable | ✅ |
| `--all` | Alle Windows Pakete | ✅ |
| `--sign` | Code Signing | ✅ |
| `--clean` | Clean Build | ✅ |

#### Cross-Platform Build-Status

| Plattform | Standard | Installer | Portable | Status |
|-----------|:--------:|:---------:|:--------:|:------:|
| **🪟 Windows** | ✅ | ✅ | ✅ | **Vollständig** |
| **🍎 macOS** | 🔄 | 🔄 | 🔄 | **Bald verfügbar** |
| **🐧 Linux** | 🔄 | 🔄 | 🔄 | **Bald verfügbar** |

> 🚧 **Entwicklungshinweis**: Das Build-System wird kontinuierlich erweitert. macOS (.app, .dmg) und Linux (AppImage, .deb, .rpm) Unterstützung wird in den nächsten Versionen hinzugefügt.

---

## 📞 Support & Updates

### 🔄 Automatische Updates

- **Windows**: Über integrierte Update-Funktion oder manueller Download
- **macOS**: Wird mit macOS-Build verfügbar sein
- **Linux**: Wird mit Linux-Build verfügbar sein

### 📋 Roadmap

#### ✅ Abgeschlossen
- Windows .exe Build
- Windows .zip Portable
- Windows NSIS/MSI Installer
- Python Cross-Platform Support

#### 🔄 In Entwicklung
- macOS .app Bundle
- macOS .dmg Installer
- Linux AppImage
- Linux .deb/.rpm Pakete
- Automatische Updates für alle Plattformen

#### 📋 Geplant
- Windows Store Distribution
- Mac App Store Distribution
- Linux Package Repository
- Docker Container
- Web-basierte Version

### 🐛 Support Kanäle

- 🚨 **Kritische Bugs**: [Security Issues](https://github.com/yourusername/Riflescope-Clicks-Calculator/security/advisories)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/Riflescope-Clicks-Calculator/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/Riflescope-Clicks-Calculator/discussions/new?category=ideas)
- 📖 **Dokumentation**: [Wiki](https://github.com/yourusername/Riflescope-Clicks-Calculator/wiki)

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## ⚠️ Disclaimer

Dieser Rechner dient ausschließlich Bildungs- und Freizeitzwecken. Überprüfen Sie alle Berechnungen und befolgen Sie stets die ordnungsgemäßen Waffensicherheitsverfahren. Der Autor übernimmt keine Verantwortung für den Missbrauch dieser Software.
