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
wmiQuery = "Select * from Win32_DiskPartition"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Access: " & objItem.Access
 wscript.echo "Availability: " & objItem.Availability
 wscript.echo "BlockSize: " & objItem.BlockSize
 wscript.echo "Bootable: " & objItem.Bootable
 wscript.echo "BootPartition: " & objItem.BootPartition
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigManagerErrorCode: " & objItem.ConfigManagerErrorCode
 wscript.echo "ConfigManagerUserConfig: " & objItem.ConfigManagerUserConfig
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "DiskIndex: " & objItem.DiskIndex
 wscript.echo "ErrorCleared: " & objItem.ErrorCleared
 wscript.echo "ErrorDescription: " & objItem.ErrorDescription
 wscript.echo "ErrorMethodology: " & objItem.ErrorMethodology
 wscript.echo "HiddenSectors: " & objItem.HiddenSectors
 wscript.echo "Index: " & objItem.Index
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "LastErrorCode: " & objItem.LastErrorCode
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NumberOfBlocks: " & objItem.NumberOfBlocks
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "PowerManagementCapabilities: " & objItem.PowerManagementCapabilities
 wscript.echo "PowerManagementSupported: " & objItem.PowerManagementSupported
 wscript.echo "PrimaryPartition: " & objItem.PrimaryPartition
 wscript.echo "Purpose: " & objItem.Purpose
 wscript.echo "RewritePartition: " & objItem.RewritePartition
 wscript.echo "Size: " & objItem.Size
 wscript.echo "StartingOffset: " & objItem.StartingOffset
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusInfo: " & objItem.StatusInfo
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "Type: " & objItem.Type
wscript.echo " "
next
