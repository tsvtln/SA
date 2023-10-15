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
wmiQuery = "Select * from Win32_CDROMDrive"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Availability: " & objItem.Availability
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
 wscript.echo "Drive: " & objItem.Drive
 wscript.echo "DriveIntegrity: " & objItem.DriveIntegrity
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "ErrorMethodology: " & objItem.ErrorMethodology
 wscript.echo "FileSystemFlags: " & objItem.FileSystemFlags
 wscript.echo "FileSystemFlagsEx: " & objItem.FileSystemFlagsEx
 wscript.echo "Id: " & objItem.Id
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MaxBlockSize: " & objItem.MaxBlockSize
 wscript.echo "MaximumComponentLength: " & objItem.MaximumComponentLength
 wscript.echo "MaxMediaSize: " & objItem.MaxMediaSize
 wscript.echo "MediaLoaded: " & objItem.MediaLoaded
 wscript.echo "MediaType: " & objItem.MediaType
 wscript.echo "MfrAssignedRevisionLevel: " & objItem.MfrAssignedRevisionLevel
 wscript.echo "MinBlockSize: " & objItem.MinBlockSize
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NeedsCleaning: " & objItem.NeedsCleaning
 wscript.echo "NumberOfMediaSupported: " & objItem.NumberOfMediaSupported
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "RevisionLevel: " & objItem.RevisionLevel
 wscript.echo "SCSIBus: " & objItem.SCSIBus
 wscript.echo "SCSILogicalUnit: " & objItem.SCSILogicalUnit
 wscript.echo "SCSIPort: " & objItem.SCSIPort
 wscript.echo "SCSITargetId: " & objItem.SCSITargetId
 wscript.echo "Size: " & objItem.Size
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TransferRate: " & objItem.TransferRate
 wscript.echo "VolumeName: " & objItem.VolumeName
 wscript.echo "VolumeSerialNumber: " & objItem.VolumeSerialNumber
wscript.echo " "
next
