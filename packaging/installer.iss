#define MyAppName "Thorlabs Data Overview"
#ifndef MyAppVersion
#define MyAppVersion "1.0.0"
#endif
#define MyAppExeName "ThorlabsDataOverview.exe"

[Setup]
AppId={{8E3C1B6A-4C2F-4E9A-9B21-A7C4E91D00D0}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher="Thorlabs Data Overview"
DefaultDirName={autopf}\Thorlabs Data Overview
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\dist\release
OutputBaseFilename=ThorlabsDataOverview-{#MyAppVersion}-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: checkedonce

[Files]
Source: "..\dist\ThorlabsDataOverview\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
