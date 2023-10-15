strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_ShareToDirectory",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_ShareToDirectory instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Share: " & objItem.Share
    Wscript.Echo "SharedElement: " & objItem.SharedElement
Next