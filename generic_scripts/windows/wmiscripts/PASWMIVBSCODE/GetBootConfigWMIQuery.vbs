strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_BootConfiguration",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_BootConfiguration instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "BootDirectory: " & objItem.BootDirectory
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "ConfigurationPath: " & objItem.ConfigurationPath
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "LastDrive: " & objItem.LastDrive
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "ScratchDirectory: " & objItem.ScratchDirectory
    Wscript.Echo "SettingID: " & objItem.SettingID
    Wscript.Echo "TempDirectory: " & objItem.TempDirectory
Next