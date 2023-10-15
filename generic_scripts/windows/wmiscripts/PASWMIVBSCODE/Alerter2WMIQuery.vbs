strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_Service WHERE Name = 'Alerter'",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_Service instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "DisplayName: " & objItem.DisplayName
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "Started: " & objItem.Started
    Wscript.Echo "State: " & objItem.State
    Wscript.Echo "Status: " & objItem.Status
    Wscript.Echo "SystemName: " & objItem.SystemName
Next