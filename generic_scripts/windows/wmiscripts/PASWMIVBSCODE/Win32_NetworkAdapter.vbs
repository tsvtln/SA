Option Explicit
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_NetworkAdapter"' where NetConnectionID = 'enetLan'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AdapterType: " & objItem.AdapterType
 wscript.echo "AdapterTypeId: " & objItem.AdapterTypeId
 wscript.echo "AutoSense: " & objItem.AutoSense
 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "Index: " & objItem.Index
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "Installed: " & objItem.Installed
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "MACAddress: " & objItem.MACAddress
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MaxNumberControlled: " & objItem.MaxNumberControlled
 wscript.echo "MaxSpeed: " & objItem.MaxSpeed
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NetConnectionID: " & objItem.NetConnectionID
 wscript.echo "NetConnectionStatus: " & objItem.NetConnectionStatus
 wscript.echo "NetworkAddresses: " & objItem.NetworkAddresses
 wscript.echo "PermanentAddress: " & objItem.PermanentAddress
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "ProductName: " & objItem.ProductName
 wscript.echo "ServiceName: " & objItem.ServiceName
 wscript.echo "Speed: " & objItem.Speed
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TimeOfLastReset: " & objItem.TimeOfLastReset
wscript.echo " "
next
