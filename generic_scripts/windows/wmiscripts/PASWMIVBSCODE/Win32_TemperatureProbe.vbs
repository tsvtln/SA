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
wmiQuery = "Select * from Win32_TemperatureProbe"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Accuracy: " & objItem.Accuracy
 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "CurrentReading: " & objItem.CurrentReading
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "IsLinear: " & objItem.IsLinear
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "LowerThresholdCritical: " & objItem.LowerThresholdCritical
 wscript.echo "LowerThresholdFatal: " & objItem.LowerThresholdFatal
 wscript.echo "LowerThresholdNonCritical: " & objItem.LowerThresholdNonCritical
 wscript.echo "MaxReadable: " & objItem.MaxReadable
 wscript.echo "MinReadable: " & objItem.MinReadable
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NominalReading: " & objItem.NominalReading
 wscript.echo "NormalMax: " & objItem.NormalMax
 wscript.echo "NormalMin: " & objItem.NormalMin
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "Resolution: " & objItem.Resolution
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "Tolerance: " & objItem.Tolerance
 wscript.echo "UpperThresholdCritical: " & objItem.UpperThresholdCritical
 wscript.echo "UpperThresholdFatal: " & objItem.UpperThresholdFatal
 wscript.echo "UpperThresholdNonCritical: " & objItem.UpperThresholdNonCritical
wscript.echo " "
next
