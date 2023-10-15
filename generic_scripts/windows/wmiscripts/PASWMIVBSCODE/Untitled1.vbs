
Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_PotsModem"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.echo "AnswerMode:"  & objItem.AnswerMode
Wscript.echo "AttachedTo:"  & objItem.AttachedTo
Wscript.echo "Availability:"  & objItem.Availability
Wscript.echo "BlindOff:"  & objItem.BlindOff
Wscript.echo "BlindOn:"  & objItem.BlindOn
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "CompatibilityFlags:"  & objItem.CompatibilityFlags
Wscript.echo "CompressionInfo:"  & objItem.CompressionInfo
Wscript.echo "CompressionOff:"  & objItem.CompressionOff
Wscript.echo "CompressionOn:"  & objItem.CompressionOn
Wscript.echo "ConfigManagerErrorCode:"  & objItem.ConfigManagerErrorCode
Wscript.echo "ConfigManagerUserConfig:"  & objItem.ConfigManagerUserConfig
Wscript.echo "ConfigurationDialog:"  & objItem.ConfigurationDialog
Wscript.echo "CountriesSupported:"  & objItem.CountriesSupported
Wscript.echo "CountrySelected:"  & objItem.CountrySelected
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "CurrentPasswords:"  & objItem.CurrentPasswords
Wscript.echo "DCB:"  & objItem.DCB
Wscript.echo "Default:"  & objItem.Default
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "DeviceID:"  & objItem.DeviceID
Wscript.echo "DeviceLoader:"  & objItem.DeviceLoader
Wscript.echo "DeviceType:"  & objItem.DeviceType
Wscript.echo "DialType:"  & objItem.DialType
Wscript.echo "DriverDate:"  & objItem.DriverDate
Wscript.echo "ErrorCleared:"  & objItem.ErrorCleared
Wscript.echo "ErrorControlForced:"  & objItem.ErrorControlForced
Wscript.echo "ErrorControlInfo:"  & objItem.ErrorControlInfo
Wscript.echo "ErrorControlOff:"  & objItem.ErrorControlOff
Wscript.echo "ErrorControlOn:"  & objItem.ErrorControlOn
Wscript.echo "ErrorDescription:"  & objItem.ErrorDescription
Wscript.echo "FlowControlHard:"  & objItem.FlowControlHard
Wscript.echo "FlowControlOff:"  & objItem.FlowControlOff
Wscript.echo "FlowControlSoft:"  & objItem.FlowControlSoft
Wscript.echo "InactivityScale:"  & objItem.InactivityScale
Wscript.echo "InactivityTimeout:"  & objItem.InactivityTimeout
Wscript.echo "Index:"  & objItem.Index
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "LastErrorCode:"  & objItem.LastErrorCode
Wscript.echo "MaxBaudRateToPhone:"  & objItem.MaxBaudRateToPhone
Wscript.echo "MaxBaudRateToSerialPort:"  & objItem.MaxBaudRateToSerialPort
Wscript.echo "MaxNumberOfPasswords:"  & objItem.MaxNumberOfPasswords
Wscript.echo "Model:"  & objItem.Model
Wscript.echo "ModemInfPath:"  & objItem.ModemInfPath
Wscript.echo "ModemInfSection:"  & objItem.ModemInfSection
Wscript.echo "ModulationBell:"  & objItem.ModulationBell
Wscript.echo "ModulationCCITT:"  & objItem.ModulationCCITT
Wscript.echo "ModulationScheme:"  & objItem.ModulationScheme
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "PNPDeviceID:"  & objItem.PNPDeviceID
Wscript.echo "PortSubClass:"  & objItem.PortSubClass
Wscript.echo "PowerManagementCapabilities:"  & objItem.PowerManagementCapabilities
Wscript.echo "PowerManagementSupported:"  & objItem.PowerManagementSupported
Wscript.echo "Prefix:"  & objItem.Prefix
Wscript.echo "Properties:"  & objItem.Properties
Wscript.echo "ProviderName:"  & objItem.ProviderName
Wscript.echo "Pulse:"  & objItem.Pulse
Wscript.echo "Reset:"  & objItem.Reset
Wscript.echo "ResponsesKeyName:"  & objItem.ResponsesKeyName
Wscript.echo "RingsBeforeAnswer:"  & objItem.RingsBeforeAnswer
Wscript.echo "SpeakerModeDial:"  & objItem.SpeakerModeDial
Wscript.echo "SpeakerModeOff:"  & objItem.SpeakerModeOff
Wscript.echo "SpeakerModeOn:"  & objItem.SpeakerModeOn
Wscript.echo "SpeakerModeSetup:"  & objItem.SpeakerModeSetup
Wscript.echo "SpeakerVolumeHigh:"  & objItem.SpeakerVolumeHigh
Wscript.echo "SpeakerVolumeInfo:"  & objItem.SpeakerVolumeInfo
Wscript.echo "SpeakerVolumeLow:"  & objItem.SpeakerVolumeLow
Wscript.echo "SpeakerVolumeMed:"  & objItem.SpeakerVolumeMed
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "StatusInfo:"  & objItem.StatusInfo
Wscript.echo "StringFormat:"  & objItem.StringFormat
Wscript.echo "SupportsCallback:"  & objItem.SupportsCallback
Wscript.echo "SupportsSynchronousConnect:"  & objItem.SupportsSynchronousConnect
Wscript.echo "SystemCreationClassName:"  & objItem.SystemCreationClassName
Wscript.echo "SystemName:"  & objItem.SystemName
Wscript.echo "Terminator:"  & objItem.Terminator
Wscript.echo "TimeOfLastReset:"  & objItem.TimeOfLastReset
Wscript.echo "Tone:"  & objItem.Tone
Wscript.echo "VoiceSwitchFeature:"  & objItem.VoiceSwitchFeature
Next