strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_LogonSession",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_LogonSession instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "AuthenticationPackage: " & objItem.AuthenticationPackage
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "InstallDate: " & objItem.InstallDate
    Wscript.Echo "LogonId: " & objItem.LogonId
    Wscript.Echo "LogonType: " & objItem.LogonType
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "StartTime: " & objItem.StartTime
    Wscript.Echo "Status: " & objItem.Status
Next