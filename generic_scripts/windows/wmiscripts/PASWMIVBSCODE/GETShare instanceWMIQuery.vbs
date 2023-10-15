strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_Share",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_Share instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "AccessMask: " & objItem.AccessMask
    Wscript.Echo "AllowMaximum: " & objItem.AllowMaximum
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "InstallDate: " & objItem.InstallDate
    Wscript.Echo "MaximumAllowed: " & objItem.MaximumAllowed
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "Path: " & objItem.Path
    Wscript.Echo "Status: " & objItem.Status
    Wscript.Echo "Type: " & objItem.Type
Next