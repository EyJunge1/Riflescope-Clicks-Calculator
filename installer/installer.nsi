!define APP_NAME "Riflescope Calculator"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "Riflescope Tools"
!define APP_EXE "riflescope-calculator.exe"
!define APP_DESCRIPTION "Professioneller Zielfernrohr-Klicksrechner für Präzisionsschießen"
!define APP_URL "https://github.com/yourusername/Riflescope-Clicks-Calculator"

# Installer Eigenschaften
Name "${APP_NAME}"
OutFile "..\dist\riflescope-calculator-setup-x64.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
RequestExecutionLevel admin
ShowInstDetails show
ShowUnInstDetails show

# Version Info
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "${APP_NAME}"
VIAddVersionKey "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey "LegalCopyright" "Copyright © 2024 Riflescope Tools"
VIAddVersionKey "FileDescription" "${APP_DESCRIPTION}"
VIAddVersionKey "FileVersion" "1.0.0"

# Moderne UI
!include "MUI2.nsh"

# UI Konfiguration
!define MUI_ABORTWARNING
!define MUI_ICON "..\icons\target_icon.ico"
!define MUI_UNICON "..\icons\target_icon.ico"

# Installer Seiten
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
  File "..\dist\${APP_EXE}"
  
  # Registry Einträge
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
  
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Desktop Verknüpfung" SecDesktop
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
SectionEnd

Section "Startmenü Einträge" SecStartMenu
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
SectionEnd

# Uninstaller
Section "Uninstall"
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\uninstall.exe"
  
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  RMDir "$INSTDIR"
  
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd

# Section Descriptions
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} "Hauptprogramm (erforderlich)"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} "Desktop Verknüpfung erstellen"
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} "Startmenü Einträge erstellen"
!insertmacro MUI_FUNCTION_DESCRIPTION_END