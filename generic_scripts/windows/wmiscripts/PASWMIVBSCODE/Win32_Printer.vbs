Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strName
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_Printer"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems:With objItem
 wscript.echo "Attributes: " & .Attributes
 wscript.echo "Availability: " & .Availability
 wscript.echo "AvailableJobSheets: " & .AvailableJobSheets
 wscript.echo "AveragePagesPerMinute: " & .AveragePagesPerMinute
 wscript.echo "Capabilities: " & join(.Capabilities, ",")
 wscript.echo "CapabilityDescriptions: " & join(.CapabilityDescriptions, ",")
 wscript.echo "Caption: " & .Caption
 wscript.echo "CharSetsSupported: " & .CharSetsSupported
 wscript.echo "Comment: " & .Comment
 wscript.echo "ConfigManagerErrorCode: " & .ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & .ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & .CreationClassName
 wscript.echo "CurrentCapabilities: " & .CurrentCapabilities
 wscript.echo "CurrentCharSet: " & .CurrentCharSet
 wscript.echo "CurrentLanguage: " & .CurrentLanguage
 wscript.echo "CurrentMimeType: " & .CurrentMimeType
 wscript.echo "CurrentNaturalLanguage: " & .CurrentNaturalLanguage
 wscript.echo "CurrentPaperType: " & .CurrentPaperType
 wscript.echo "Default: " & .Default
 wscript.echo "DefaultCapabilities: " & .DefaultCapabilities
 wscript.echo "DefaultCopies: " & .DefaultCopies
 wscript.echo "DefaultLanguage: " & .DefaultLanguage
 wscript.echo "DefaultMimeType: " & .DefaultMimeType
 wscript.echo "DefaultNumberUp: " & .DefaultNumberUp
 wscript.echo "DefaultPaperType: " & .DefaultPaperType
 wscript.echo "DefaultPriority: " & .DefaultPriority
 wscript.echo "Description: " & .Description
 wscript.echo "DetectedErrorState: " & .DetectedErrorState
 wscript.echo "DeviceID: " & .DeviceID
 wscript.echo "Direct: " & .Direct
 wscript.echo "DoCompleteFirst: " & .DoCompleteFirst
 wscript.echo "DriverName: " & .DriverName
 wscript.echo "EnableBIDI: " & .EnableBIDI
 wscript.echo "EnableDevQueryPrint: " & .EnableDevQueryPrint
 wscript.echo "ErrorCleared: " & .ErrorCleared
 wscript.echo "ErrorDescription: " & .ErrorDescription
 wscript.echo "ErrorInformation: " & .ErrorInformation
 wscript.echo "ExtendedDetectedErrorState: " & .ExtendedDetectedErrorState
 wscript.echo "ExtendedPrinterStatus: " & .ExtendedPrinterStatus
 wscript.echo "Hidden: " & .Hidden
 wscript.echo "HorizontalResolution: " & .HorizontalResolution
 wscript.echo "InstallDate: " & .InstallDate
 wscript.echo "JobCountSinceLastReset: " & .JobCountSinceLastReset
 wscript.echo "KeepPrintedJobs: " & .KeepPrintedJobs
 wscript.echo "LanguagesSupported: " & .LanguagesSupported
 wscript.echo "LastErrorCode: " & .LastErrorCode
 wscript.echo "Local: " & .Local
 wscript.echo "Location: " & .Location
 wscript.echo "MarkingTechnology: " & .MarkingTechnology
 wscript.echo "MaxCopies: " & .MaxCopies
 wscript.echo "MaxNumberUp: " & .MaxNumberUp
 wscript.echo "MaxSizeSupported: " & .MaxSizeSupported
 wscript.echo "MimeTypesSupported: " & .MimeTypesSupported
 wscript.echo "Name: " & .Name
 wscript.echo "NaturalLanguagesSupported: " & .NaturalLanguagesSupported
 wscript.echo "Network: " & .Network
 wscript.echo "PaperSizesSupported: " & join(.PaperSizesSupported, ",")
 wscript.echo "PaperTypesAvailable: " & .PaperTypesAvailable
 wscript.echo "Parameters: " & .Parameters
 wscript.echo "PNPDeviceID: " & .PNPDeviceID
 wscript.echo "PortName: " & .PortName
 wscript.echo "PowerManagementCapabilities: " & .PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & .PowerManagementSupported
wscript.echo "PrinterPaperNames: " & Join(.PrinterPaperNames)
 wscript.echo "PrinterState: " & .PrinterState
 wscript.echo "PrinterStatus: " & .PrinterStatus
 wscript.echo "PrintJobDataType: " & .PrintJobDataType
 wscript.echo "PrintProcessor: " & .PrintProcessor
 wscript.echo "Priority: " & .Priority
 wscript.echo "Published: " & .Published
 wscript.echo "Queued: " & .Queued
 wscript.echo "RawOnly: " & .RawOnly
 wscript.echo "SeparatorFile: " & .SeparatorFile
 wscript.echo "ServerName: " & .ServerName
 wscript.echo "Shared: " & .Shared
 wscript.echo "ShareName: " & .ShareName
 wscript.echo "SpoolEnabled: " & .SpoolEnabled
 wscript.echo "StartTime: " & .StartTime
 wscript.echo "Status: " & .Status
 wscript.echo "StatusInfo: " & .StatusInfo
 wscript.echo "SystemCreationClassName: " & .SystemCreationClassName
 wscript.echo "SystemName: " & .SystemName
 wscript.echo "TimeOfLastReset: " & .TimeOfLastReset
 wscript.echo "UntilTime: " & .UntilTime
 wscript.echo "VerticalResolution: " & .VerticalResolution
 wscript.echo "WorkOffline: " & .WorkOffline & vbcrlf
end with:next
