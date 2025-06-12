"""
Riflescope Clicks Calculator - Main Package

Ein präzises Tool zur Berechnung der erforderlichen Klicks am Zielfernrohr
basierend auf Waffe, Munition und Entfernung für Präzisionsschießen.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

# Hauptkomponenten für einfachen Import
from .main import main
from .config import AppSettings

__all__ = ['main', 'AppSettings']
