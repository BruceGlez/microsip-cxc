[Setup]
AppName=Microsip Tool
AppVersion=1.2.1
AppPublisher=Soluciones Informáticas González
DefaultDirName={commonpf}\MicrosipTool
DefaultGroupName=Microsip Tool
OutputBaseFilename=MicrosipToolInstaller
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\MicrosipTool\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Microsip Tool"; Filename: "{app}\MicrosipTool.exe"
Name: "{group}\Uninstall Microsip Tool"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Microsip Tool"; Filename: "{app}\MicrosipTool.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el Escritorio"; GroupDescription: "Opciones adicionales:"; Flags: unchecked

[Run]
Filename: "{app}\MicrosipTool.exe"; Description: "Ejecutar Microsip Tool"; Flags: nowait postinstall skipifsilent
