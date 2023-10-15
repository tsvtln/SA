strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_ServiceControl",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_ServiceControl instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Arguments: " & objItem.Arguments
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "Event: " & objItem.Event
    Wscript.Echo "ID: " & objItem.ID
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "ProductCode: " & objItem.ProductCode
    Wscript.Echo "SettingID: " & objItem.SettingID
    Wscript.Echo "Wait: " & objItem.Wait
Next