strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_LoadOrderGroupServiceMembers",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_LoadOrderGroupServiceMembers instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "GroupComponent: " & objItem.GroupComponent
    Wscript.Echo "PartComponent: " & objItem.PartComponent
Next