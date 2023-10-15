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
wmiQuery = "Select * from Win32_VideoController"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AcceleratorCapabilities: " & objItem.AcceleratorCapabilities
 wscript.echo "AdapterCompatibility: " & objItem.AdapterCompatibility
 wscript.echo "AdapterDACType: " & objItem.AdapterDACType
 wscript.echo "AdapterRAM: " & objItem.AdapterRAM
 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "CapabilityDescriptions: " & objItem.CapabilityDescriptions
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ColorTableEntries: " & objItem.ColorTableEntries
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "CurrentBitsPerPixel: " & objItem.CurrentBitsPerPixel
 wscript.echo "CurrentHorizontalResolution: " & objItem.CurrentHorizontalResolution
 wscript.echo "CurrentNumberOfColors: " & objItem.CurrentNumberOfColors
 wscript.echo "CurrentNumberOfColumns: " & objItem.CurrentNumberOfColumns
 wscript.echo "CurrentNumberOfRows: " & objItem.CurrentNumberOfRows
 wscript.echo "CurrentRefreshRate: " & objItem.CurrentRefreshRate
 wscript.echo "CurrentScanMode: " & objItem.CurrentScanMode
 wscript.echo "CurrentVerticalResolution: " & objItem.CurrentVerticalResolution
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "DeviceSpecificPens: " & objItem.DeviceSpecificPens
 wscript.echo "DitherType: " & objItem.DitherType
 wscript.echo "DriverDate: " & objItem.DriverDate
 wscript.echo "DriverVersion: " & objItem.DriverVersion
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "ICMIntent: " & objItem.ICMIntent
 wscript.echo "ICMMethod: " & objItem.ICMMethod
 wscript.echo "InfFilename: " & objItem.InfFilename
 wscript.echo "InfSection: " & objItem.InfSection
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "InstalledDisplayDrivers: " & objItem.InstalledDisplayDrivers
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "MaxMemorySupported: " & objItem.MaxMemorySupported
 wscript.echo "MaxNumberControlled: " & objItem.MaxNumberControlled
 wscript.echo "MaxRefreshRate: " & objItem.MaxRefreshRate
 wscript.echo "MinRefreshRate: " & objItem.MinRefreshRate
 wscript.echo "Monochrome: " & objItem.Monochrome
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NumberOfColorPlanes: " & objItem.NumberOfColorPlanes
 wscript.echo "NumberOfVideoPages: " & objItem.NumberOfVideoPages
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "ProtocolSupported: " & objItem.ProtocolSupported
 wscript.echo "ReservedSystemPaletteEntries: " & objItem.ReservedSystemPaletteEntries
 wscript.echo "SpecificationVersion: " & objItem.SpecificationVersion
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "SystemPaletteEntries: " & objItem.SystemPaletteEntries
 wscript.echo "TimeOfLastReset: " & objItem.TimeOfLastReset
 wscript.echo "VideoArchitecture: " & objItem.VideoArchitecture
 wscript.echo "VideoMemoryType: " & objItem.VideoMemoryType
 wscript.echo "VideoMode: " & objItem.VideoMode
 wscript.echo "VideoModeDescription: " & objItem.VideoModeDescription
 wscript.echo "VideoProcessor: " & objItem.VideoProcessor
wscript.echo " "
next
