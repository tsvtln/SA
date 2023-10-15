
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from cim_fan"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
'WScript.Echo objItem.setSpeed(800)
   Wscript.echo "ActiveCooling:"  & objItem.ActiveCooling
Wscript.echo "Availability:"  & objItem.Availability
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "ConfigManagerErrorCode:"  & objItem.ConfigManagerErrorCode
Wscript.echo "ConfigManagerUserConfig:"  & objItem.ConfigManagerUserConfig
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "DesiredSpeed:"  & objItem.DesiredSpeed
Wscript.echo "DeviceID:"  & objItem.DeviceID
Wscript.echo "ErrorCleared:"  & objItem.ErrorCleared
Wscript.echo "ErrorDescription:"  & objItem.ErrorDescription
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "LastErrorCode:"  & objItem.LastErrorCode
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "PNPDeviceID:"  & objItem.PNPDeviceID
Wscript.echo "PowerManagementCapabilities:"  & objItem.PowerManagementCapabilities
Wscript.echo "PowerManagementSupported:"  & objItem.PowerManagementSupported
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "StatusInfo:"  & objItem.StatusInfo
Wscript.echo "SystemCreationClassName:"  & objItem.SystemCreationClassName
Wscript.echo "SystemName:"  & objItem.SystemName
Wscript.echo "VariableSpeed:"  & objItem.VariableSpeed
Next