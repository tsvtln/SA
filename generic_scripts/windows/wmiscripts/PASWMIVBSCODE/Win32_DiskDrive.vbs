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
wmiQuery = "Select * from Win32_DiskDrive"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "BytesPerSector: " & objItem.BytesPerSector
 wscript.echo "Capabilities: " & join(objItem.Capabilities, ",")
 wscript.echo "CapabilityDescriptions: " & objItem.CapabilityDescriptions
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CompressionMethod: " & objItem.CompressionMethod
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "DefaultBlockSize: " & objItem.DefaultBlockSize
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "ErrorMethodology: " & objItem.ErrorMethodology
 wscript.echo "Index: " & objItem.Index
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "InterfaceType: " & objItem.InterfaceType
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MaxBlockSize: " & objItem.MaxBlockSize
 wscript.echo "MaxMediaSize: " & objItem.MaxMediaSize
 wscript.echo "MediaLoaded: " & objItem.MediaLoaded
 wscript.echo "MediaType: " & objItem.MediaType
 wscript.echo "MinBlockSize: " & objItem.MinBlockSize
 wscript.echo "Model: " & objItem.Model
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NeedsCleaning: " & objItem.NeedsCleaning
 wscript.echo "NumberOfMediaSupported: " & objItem.NumberOfMediaSupported
 wscript.echo "Partitions: " & objItem.Partitions
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "SCSIBus: " & objItem.SCSIBus
 wscript.echo "SCSILogicalUnit: " & objItem.SCSILogicalUnit
 wscript.echo "SCSIPort: " & objItem.SCSIPort
 wscript.echo "SCSITargetId: " & objItem.SCSITargetId
 wscript.echo "SectorsPerTrack: " & objItem.SectorsPerTrack
 wscript.echo "Signature: " & objItem.Signature
 wscript.echo "Size: " & objItem.Size
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TotalCylinders: " & objItem.TotalCylinders
 wscript.echo "TotalHeads: " & objItem.TotalHeads
 wscript.echo "TotalSectors: " & objItem.TotalSectors
 wscript.echo "TotalTracks: " & objItem.TotalTracks
 wscript.echo "TracksPerCylinder: " & objItem.TracksPerCylinder
wscript.echo " "
next
