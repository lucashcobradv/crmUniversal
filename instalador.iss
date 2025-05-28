; -- INSTALADOR.ISS --
[Setup]
AppName=Universal Traduções
AppVersion=1.0
AppPublisher=Universal Traduções LTDA
DefaultDirName={commonpf}\Universal Traduções
DefaultGroupName=Universal Traduções
UninstallDisplayIcon={app}\universal_icon.ico
OutputDir=.\Instalador
OutputBaseFilename=Instalador_Universal_Traducoes
SetupIconFile=universal_icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\crm_universal.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "universal_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Universal Traduções"; Filename: "{app}\crm_universal.exe"; IconFilename: "{app}\universal_icon.ico"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Universal Traduções"; Filename: "{app}\crm_universal.exe"; IconFilename: "{app}\universal_icon.ico"

[Run]
Filename: "{app}\crm_universal.exe"; Description: "Abrir aplicativo após instalação"; Flags: postinstall nowait skipifsilent