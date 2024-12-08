[Setup]
AppName=NCERT Learn IDE
AppVersion=1.0
DefaultDirName="C:\NCERT Learn IDE"
DefaultGroupName=NCERT Learn IDE
OutputDir=.
OutputBaseFilename=NCERT Learn IDE Installer
DisableProgramGroupPage=yes
DisableWelcomePage=no
AppPublisher=Muhammed Shafin P
AppContact=hejhdiss@gmail.com
UninstallFilesDir={app}
AppCopyright=Muhammed Shafin P
AllowCancelDuringInstall=yes
DirExistsWarning=yes
VersionInfoProductName=NCERT Learn IDE
VersionInfoCompany=Muhammed Shafin P
VersionInfoProductVersion=1.0
VersionInfoCopyright=Muhammed Shafin P
WizardStyle=modern
Compression=lzma2
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SolidCompression=yes
SetupIconFile="C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\logo.ico"
UninstallDisplayIcon="C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\un.ico"
PrivilegesRequired=Admin
CreateUninstallRegKey=no


[Languages]
Name: en; MessagesFile: "compiler:Default.isl"
Name: nl; MessagesFile: "compiler:Languages\Dutch.isl"
Name: de; MessagesFile: "compiler:Languages\German.isl"

[Messages]
en.BeveledLabel=English
nl.BeveledLabel=Nederlands
de.BeveledLabel=Deutsch

[Files]
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\all things wanted only\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\logo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\un.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\terminal.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\c.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\c++.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\reset.ico"; DestDir: "{app}"; Flags: ignoreversion






[Icons]
; Create Start Menu and Desktop Shortcuts
Name: "{userdesktop}\NCERT Learn IDE"; Filename: "{app}\launcher.exe"; IconFilename: "{app}\logo.ico"; IconIndex: 0
Name: "{userprograms}\NCERT Learn IDE\NCERT Learn IDE"; Filename: "{app}\launcher.exe"; IconFilename: "{app}\logo.ico"; IconIndex: 0
Name: "{userdesktop}\Uninstall NCERT Learn IDE"; Filename: "{uninstallexe}"; IconFilename: "{app}\un.ico"; IconIndex: 0
Name: "{userprograms}\NCERT Learn IDE\Uninstall NCERT Learn IDE"; Filename: "{uninstallexe}"; IconFilename: "{app}\un.ico"; IconIndex: 0
Name: "{userdesktop}\NCERT Learn IDE Terminal"; Filename: "{app}\terminal.exe"; IconFilename: "{app}\terminal.ico"; IconIndex: 0
Name: "{userprograms}\NCERT Learn IDE\NCERT Learn IDE Terminal"; Filename: "{app}\terminal.exe"; IconFilename: "{app}\terminal.ico"; IconIndex: 0
Name: "{userdesktop}\NCERT Learn IDE C++ Runner"; Filename: "{app}\compiled_cpp_program.exe"; IconFilename: "{app}\c++.ico"; IconIndex: 0
Name: "{userprograms}\NCERT Learn IDE\NCERT Learn IDE C++ Runner"; Filename: "{app}\compiled_cpp_program.exe"; IconFilename: "{app}\c++.ico"; IconIndex: 0
Name: "{userdesktop}\NCERT Learn IDE C Runner"; Filename: "{app}\compiled_c_program.exe"; IconFilename: "{app}\c.ico"; IconIndex: 0
Name: "{userprograms}\NCERT Learn IDE\NCERT Learn IDE C Runner"; Filename: "{app}\compiled_c_program.exe"; IconFilename: "{app}\c.ico"; IconIndex: 0
Name: "{userdesktop}\NCERT Learn IDE Reset Python Environmet"; Filename: "{app}\pythonresolve.exe"; IconFilename: "{app}\reset.ico"; IconIndex: 0
Name: "{userprograms}\NCERT Learn IDE\NCERT Learn IDE Reset NCERT Learn IDE Python Environmet"; Filename: "{app}\pythonresolve.exe"; IconFilename: "{app}\reset.ico"; IconIndex: 0

[Run]
; Automatically run the IDE after installation
Filename: "{app}\launcher.exe"; Description: "Run NCERT Learn IDE"; Flags: nowait postinstall skipifsilent
Filename: "{app}\maincreator.exe"; Description: "Setup NCERT Learn IDE Python Environment"; Flags: nowait postinstall skipifsilent


[UninstallDelete]
; Clean up installed files and directories
Type: filesandordirs; Name: "{app}"

[Code]

var
  AppName: string;

procedure InitializeWizard();
begin
  // Initialize any setup messages or processes here if needed
  AppName := 'NCERT Learn IDE';

end;



procedure DeinitializeSetup();
begin
  // Message after installation is complete
  MsgBox('NCERT Learn IDE setup complete.' + #13#10 + 'Developed by Muhammed Shafin P.', mbInformation, MB_OK);
end;
procedure DeinitializeUninstall();
begin

end;

