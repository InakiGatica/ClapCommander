[Setup]
AppName=ClapCommander
AppVersion=1.0.0
AppPublisher=InakiGatica
DefaultDirName={autopf}\ClapCommander
DefaultGroupName=ClapCommander
OutputDir=installer
OutputBaseFilename=ClapCommander_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional icons:"
Name: "startup"; Description: "Start with Windows"; GroupDescription: "Startup:"

[Files]
Source: "dist\ClapCommander.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ClapCommander"; Filename: "{app}\ClapCommander.exe"
Name: "{commondesktop}\ClapCommander"; Filename: "{app}\ClapCommander.exe"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ClapCommander"; ValueData: "{app}\ClapCommander.exe"; Flags: uninsdeletevalue; Tasks: startup

[Run]
Filename: "{app}\ClapCommander.exe"; Description: "Launch ClapCommander"; Flags: nowait postinstall skipifsilent