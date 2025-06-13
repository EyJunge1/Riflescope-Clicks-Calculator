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

| Betriebssystem | Minimum | Empfohlen | Zusätzliche Hinweise |
|----------------|---------|-----------|---------------------|
| **🪟 Windows** | Windows 10 | Windows 11 | x64 und ARM64 unterstützt |
| **🍎 macOS** | macOS 10.15+ | macOS 13+ | Intel und Apple Silicon (M1/M2/M3/M4) |
| **🐧 Linux** | Ubuntu 20.04+ | Ubuntu 24.04+ | x86_64, ARM64, Wayland & X11 |

## 💾 Installations-Optionen

### 🏆 Option 1: Fertige Anwendung (Empfohlen)

> ⚡ **Schnellste Installation** - Ein Download, sofort einsatzbereit

#### 📦 Direkte Downloads

| Plattform | Download | Größe | Installer-Typ |
|-----------|----------|-------|---------------|
| 🪟 **Windows** | [Setup.exe](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-setup-x64.exe) | 25 MB | MSI Installer |
| 🪟 **Windows (Portable)** | [Portable.zip](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-portable-x64.zip) | 23 MB | Keine Installation |
| 🍎 **macOS** | [App.dmg](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-macos.dmg) | 28 MB | Universal Binary |
| 🐧 **Linux** | [AppImage](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-linux-x86_64.AppImage) | 27 MB | Portable |
| 🐧 **Linux (deb)** | [.deb](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator_1.0.0_amd64.deb) | 25 MB | Debian/Ubuntu |
| 🐧 **Linux (rpm)** | [.rpm](https://github.com/yourusername/Riflescope-Clicks-Calculator/releases/latest/download/riflescope-calculator-1.0.0-1.x86_64.rpm) | 25 MB | Fedora/RHEL |

---

### 🐍 Option 2: Python-Ausführung

> 🔧 **Für Entwickler** - Neueste Features, Anpassungen möglich

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

#### Als Python Package
```bash
# Installation via pip (lokal)
pip install .

# Installation aus GitHub
pip install git+https://github.com/yourusername/Riflescope-Clicks-Calculator.git

# Starten
riflescope-calculator
# oder
python -m riflescope_calculator
```

---

### ⚙️ Option 4: Eigene Builds erstellen

> 🛠️ **Vollständige Kontrolle** - Anpassbare Builds für Distribution

#### Universal Build System
```bash
# Interaktive Platform-Auswahl
python scripts/build.py

# Automatisch für aktuelles System
python scripts/build.py --recommended

# Spezifische Plattformen
python scripts/build.py --windows --installer --portable
python scripts/build.py --macos --universal --portable  
python scripts/build.py --linux --appimage --portable

# Alle Plattformen mit allen Optionen
python scripts/build.py --all --installer --portable --test
```

#### Build-Optionen im Detail

| Option | Beschreibung | Windows | macOS | Linux |
|--------|--------------|:-------:|:-----:|:-----:|
| `--installer` | MSI/PKG/DEB Installer | ✅ | ✅ | ✅ |
| `--portable` | ZIP/TAR.GZ Archive | ✅ | ✅ | ✅ |
| `--universal` | Universal Binary | ❌ | ✅ | ❌ |
| `--appimage` | AppImage Format | ❌ | ❌ | ✅ |
| `--signed` | Code Signing | ✅ | ✅ | ❌ |
| `--optimized` | Size/Speed optimiert | ✅ | ✅ | ✅ |
| `--debug` | Debug-Symbole | ✅ | ✅ | ✅ |

---

## 📞 Support & Updates

### 🔄 Automatische Updates

- **Windows**: Über Windows Update oder integrierte Update-Funktion
- **macOS**: Über Mac App Store oder Sparkle Framework
- **Linux**: Über Package Manager oder integrierte Update-Funktion

### 🐛 Support Kanäle

- 🚨 **Kritische Bugs**: [Security Issues](https://github.com/yourusername/Riflescope-Clicks-Calculator/security/advisories)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/Riflescope-Clicks-Calculator/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/Riflescope-Clicks-Calculator/discussions/new?category=ideas)
- 📖 **Dokumentation**: [Wiki](https://github.com/yourusername/Riflescope-Clicks-Calculator/wiki)

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## ⚠️ Disclaimer

Dieser Rechner dient ausschließlich Bildungs- und Freizeitzwecken. Überprüfen Sie alle Berechnungen und befolgen Sie stets die ordnungsgemäßen Waffensicherheitsverfahren. Der Autor übernimmt keine Verantwortung für den Missbrauch dieser Software.
