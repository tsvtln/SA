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
wmiQuery = "Select * from Win32_POTSModem"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AnswerMode: " & objItem.AnswerMode
 wscript.echo "AttachedTo: " & objItem.AttachedTo
 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "BlindOff: " & objItem.BlindOff
 wscript.echo "BlindOn: " & objItem.BlindOn
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CompatibilityFlags: " & objItem.CompatibilityFlags
 wscript.echo "CompressionInfo: " & objItem.CompressionInfo
 wscript.echo "CompressionOff: " & objItem.CompressionOff
 wscript.echo "CompressionOn: " & objItem.CompressionOn
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "ConfigurationDialog: " & objItem.ConfigurationDialog
 wscript.echo "CountriesSupported: " & objItem.CountriesSupported
 wscript.echo "CountrySelected: " & objItem.CountrySelected
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "CurrentPasswords: " & objItem.CurrentPasswords
 wscript.echo "DCB: " & objItem.DCB
 wscript.echo "Default: " & objItem.Default
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "DeviceLoader: " & objItem.DeviceLoader
 wscript.echo "DeviceType: " & objItem.DeviceType
 wscript.echo "DialType: " & objItem.DialType
 wscript.echo "DriverDate: " & objItem.DriverDate
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorControlForced: " & objItem.ErrorControlForced
 wscript.echo "ErrorControlInfo: " & objItem.ErrorControlInfo
 wscript.echo "ErrorControlOff: " & objItem.ErrorControlOff
 wscript.echo "ErrorControlOn: " & objItem.ErrorControlOn
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "FlowControlHard: " & objItem.FlowControlHard
 wscript.echo "FlowControlOff: " & objItem.FlowControlOff
 wscript.echo "FlowControlSoft: " & objItem.FlowControlSoft
 wscript.echo "InactivityScale: " & objItem.InactivityScale
 wscript.echo "InactivityTimeout: " & objItem.InactivityTimeout
 wscript.echo "Index: " & objItem.Index
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "MaxBaudRateToPhone: " & objItem.MaxBaudRateToPhone
 wscript.echo "MaxBaudRateToSerialPort: " & objItem.MaxBaudRateToSerialPort
 wscript.echo "MaxNumberOfPasswords: " & objItem.MaxNumberOfPasswords
 wscript.echo "Model: " & objItem.Model
 wscript.echo "ModemInfPath: " & objItem.ModemInfPath
 wscript.echo "ModemInfSection: " & objItem.ModemInfSection
 wscript.echo "ModulationBell: " & objItem.ModulationBell
 wscript.echo "ModulationCCITT: " & objItem.ModulationCCITT
 wscript.echo "ModulationScheme: " & objItem.ModulationScheme
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PortSubClass: " & objItem.PortSubClass
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "Prefix: " & objItem.Prefix
 wscript.echo "Properties: " & objItem.Properties
 wscript.echo "ProviderName: " & objItem.ProviderName
 wscript.echo "Pulse: " & objItem.Pulse
 wscript.echo "Reset: " & objItem.Reset
 wscript.echo "ResponsesKeyName: " & objItem.ResponsesKeyName
 wscript.echo "RingsBeforeAnswer: " & objItem.RingsBeforeAnswer
 wscript.echo "SpeakerModeDial: " & objItem.SpeakerModeDial
 wscript.echo "SpeakerModeOff: " & objItem.SpeakerModeOff
 wscript.echo "SpeakerModeOn: " & objItem.SpeakerModeOn
 wscript.echo "SpeakerModeSetup: " & objItem.SpeakerModeSetup
 wscript.echo "SpeakerVolumeHigh: " & objItem.SpeakerVolumeHigh
 wscript.echo "SpeakerVolumeInfo: " & objItem.SpeakerVolumeInfo
 wscript.echo "SpeakerVolumeLow: " & objItem.SpeakerVolumeLow
 wscript.echo "SpeakerVolumeMed: " & objItem.SpeakerVolumeMed
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "StringFormat: " & objItem.StringFormat
 wscript.echo "SupportsCallback: " & objItem.SupportsCallback
 wscript.echo "SupportsSynchronousConnect: " & objItem.SupportsSynchronousConnect
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "Terminator: " & objItem.Terminator
 wscript.echo "TimeOfLastReset: " & objItem.TimeOfLastReset
 wscript.echo "Tone: " & objItem.Tone
 wscript.echo "VoiceSwitchFeature: " & objItem.VoiceSwitchFeature
wscript.echo " "
next
