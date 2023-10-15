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
wmiQuery = "Select * from Win32_DesktopMonitor"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "Bandwidth: " & objItem.Bandwidth
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "DisplayType: " & objItem.DisplayType
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "IsLocked: " & objItem.IsLocked
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "MonitorManufacturer: " & objItem.MonitorManufacturer
 wscript.echo "MonitorType: " & objItem.MonitorType
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PixelsPerXLogicalInch: " & objItem.PixelsPerXLogicalInch
 wscript.echo "PixelsPerYLogicalInch: " & objItem.PixelsPerYLogicalInch
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "ScreenHeight: " & objItem.ScreenHeight
 wscript.echo "ScreenWidth: " & objItem.ScreenWidth
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
wscript.echo " "
next
