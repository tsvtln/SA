Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_Keyboard.deviceID='ACPI\PNP0303\4&1D6F7EAE&0'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "IsLocked: " & objItem.IsLocked
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "Layout: " & objItem.Layout
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NumberOfFunctionKeys: " & objItem.NumberOfFunctionKeys
 wscript.echo "Password: " & objItem.Password
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
wscript.echo " "

