Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_TemperatureProbe.DeviceID='root\cimv2 0'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
With objItem
 wscript.echo "Accuracy: " & .Accuracy
 wscript.echo "Availability: " & .Availability
 wscript.echo "Caption: " & .Caption
 wscript.echo "ConfigManagerErrorCode: " & .ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & .ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & .CreationClassName
 wscript.echo "CurrentReading: " & .CurrentReading
 wscript.echo "Description: " & .Description
 wscript.echo "DeviceID: " & .DeviceID
 wscript.echo "ErrorCleared: " & .ErrorCleared
 wscript.echo "ErrorDescription: " & .ErrorDescription
 wscript.echo "InstallDate: " & .InstallDate
 wscript.echo "IsLinear: " & .IsLinear
 wscript.echo "LastErrorCode: " & .LastErrorCode
 wscript.echo "LowerThresholdCritical: " & .LowerThresholdCritical
 wscript.echo "LowerThresholdFatal: " & .LowerThresholdFatal
 wscript.echo "LowerThresholdNonCritical: " & .LowerThresholdNonCritical
 wscript.echo "MaxReadable: " & .MaxReadable
 wscript.echo "MinReadable: " & .MinReadable
 wscript.echo "Name: " & .Name
 wscript.echo "NominalReading: " & .NominalReading
 wscript.echo "NormalMax: " & .NormalMax
 wscript.echo "NormalMin: " & .NormalMin
 wscript.echo "PNPDeviceID: " & .PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & .PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & .PowerManagementSupported
 wscript.echo "Resolution: " & .Resolution
 wscript.echo "Status: " & .Status
 wscript.echo "StatusInfo: " & .StatusInfo
 wscript.echo "SystemCreationClassName: " & .SystemCreationClassName
 wscript.echo "SystemName: " & .SystemName
 wscript.echo "Tolerance: " & .Tolerance
 wscript.echo "UpperThresholdCritical: " & .UpperThresholdCritical
 wscript.echo "UpperThresholdFatal: " & .UpperThresholdFatal
 wscript.echo "UpperThresholdNonCritical: " & .UpperThresholdNonCritical
End with
