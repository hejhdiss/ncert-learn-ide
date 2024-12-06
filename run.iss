[Setup]
AppName=NCERT Learn IDE
AppVersion=1.0
DefaultDirName={pf}\NCERT Learn IDE
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
CreateUninstallRegKey=true
SolidCompression=yes
SetupIconFile=C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\logo.ico
UninstallDisplayIcon=C:\Users\Muhammed Shafin P\OneDrive\Documents\some python in fleet\ncert_learn_ide\un.ico
PrivilegesRequired=Admin
[Tasks]
Name: "add_to_path"; Description: "Add Python and GCC directories to PATH"; GroupDescription: "Environment Variables"; Flags: unchecked


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


[Registry]
; Add Python executable path to the environment variable
Root: HKCU; Subkey: "Environment"; ValueName: "NCERT_PYTHON"; ValueType: string; ValueData: "{app}\python\python.exe"; Flags: uninsdeletevalue preservestringtype

; Append Python directories to PATH without overwriting existing values
Root: HKCU; Subkey: "Environment"; ValueName: "PATH"; ValueType: expandsz; ValueData: "{app}\python\Scripts;{app}\python;{app}\gcc\bin;{olddata}"; Tasks: add_to_path; Flags: preservestringtype uninsdeletevalue 



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

[Run]
; Automatically run the IDE after installation
Filename: "{app}\launcher.exe"; Description: "Run NCERT Learn IDE"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up installed files and directories
Type: filesandordirs; Name: "{app}"

[Code]
var
  AuthorMessage: string;
procedure DeinitializeSetup();
begin
  MsgBox('NCERT Learn IDE setup complete.' + #13#10 + AuthorMessage, mbInformation, MB_OK);
  AuthorMessage := 'NCERT Learn IDE developed by Muhammed Shafin P.' + #13#10 +
                   'Thank you for using NCERT Learn IDE!';
  MsgBox(AuthorMessage, mbInformation, MB_OK);
end;

procedure InitializeUninstallProgressForm();
begin
end;

procedure DeinitializeUninstall();
begin
end;

