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
wmiQuery = "Select * from Win32_PointingDevice"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "DeviceInterface: " & objItem.DeviceInterface
 wscript.echo "DoubleSpeedThreshold: " & objItem.DoubleSpeedThreshold
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "Handedness: " & objItem.Handedness
 wscript.echo "HardwareType: " & objItem.HardwareType
 wscript.echo "InfFileName: " & objItem.InfFileName
 wscript.echo "InfSection: " & objItem.InfSection
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "IsLocked: " & objItem.IsLocked
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NumberOfButtons: " & objItem.NumberOfButtons
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PointingType: " & objItem.PointingType
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "QuadSpeedThreshold: " & objItem.QuadSpeedThreshold
 wscript.echo "Resolution: " & objItem.Resolution
 wscript.echo "SampleRate: " & objItem.SampleRate
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "Synch: " & objItem.Synch
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
wscript.echo " "
next
