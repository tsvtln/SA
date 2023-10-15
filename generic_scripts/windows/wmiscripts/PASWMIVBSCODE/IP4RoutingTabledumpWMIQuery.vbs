strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_IP4RouteTable",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_IP4RouteTable instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Age: " & objItem.Age
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "Destination: " & objItem.Destination
    Wscript.Echo "Information: " & objItem.Information
    Wscript.Echo "InstallDate: " & objItem.InstallDate
    Wscript.Echo "InterfaceIndex: " & objItem.InterfaceIndex
    Wscript.Echo "Mask: " & objItem.Mask
    Wscript.Echo "Metric1: " & objItem.Metric1
    Wscript.Echo "Metric2: " & objItem.Metric2
    Wscript.Echo "Metric3: " & objItem.Metric3
    Wscript.Echo "Metric4: " & objItem.Metric4
    Wscript.Echo "Metric5: " & objItem.Metric5
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "NextHop: " & objItem.NextHop
    Wscript.Echo "Protocol: " & objItem.Protocol
    Wscript.Echo "Status: " & objItem.Status
    Wscript.Echo "Type: " & objItem.Type
Next