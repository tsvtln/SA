strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\WMI") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM WMI_Query",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "WMI_Query instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Active: " & objItem.Active
    Wscript.Echo "InstanceName: " & objItem.InstanceName
    Wscript.Echo "QDATA: " & objItem.QDATA
Next