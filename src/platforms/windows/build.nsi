Unicode true

Name "Argentum Control"
OutFile "ARC Installer.exe"
InstallDir "$PROGRAMFILES\Cartesian Co\Argentum Control"

AllowRootDirInstall true
SetCompressor lzma

!include "MUI2.nsh"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_PAGE_CUSTOMFUNCTION_PRE InstallDriver
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE English

Function InstallDriver
    nsExec::Exec '"$INSTDIR\drivers\install_driver.cmd"'
FunctionEnd

Section "Argentum Control"
SetOutPath "$INSTDIR"

File /r 'C:\Users\Test\Documents\Argentum\build\data\*'
WriteUninstaller '$INSTDIR\ARC Uninstaller.exe'


CreateShortCut "$SMPROGRAMS\Cartesian Co\Argentum Control.lnk" "$INSTDIR\gui.exe"
CreateShortCut "$SMPROGRAMS\Cartesian Co\Uninstall.lnk" "$INSTDIR\ARC Uninstaller.exe"

SectionEnd

Section "Uninstall"

Delete "$INSTDIR\*"
Delete "$SMPROGRAMS\Cartesian Co\*"
 
SectionEnd