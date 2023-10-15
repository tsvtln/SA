strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_AccountSID",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_AccountSID instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Element: " & objItem.Element
    Wscript.Echo "Setting: " & objItem.Setting
Next