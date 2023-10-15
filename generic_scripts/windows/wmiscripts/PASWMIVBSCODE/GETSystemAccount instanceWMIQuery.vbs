strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_SystemAccount",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_SystemAccount instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "Domain: " & objItem.Domain
    Wscript.Echo "InstallDate: " & objItem.InstallDate
    Wscript.Echo "LocalAccount: " & objItem.LocalAccount
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "SID: " & objItem.SID
    Wscript.Echo "SIDType: " & objItem.SIDType
    Wscript.Echo "Status: " & objItem.Status
Next