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
wmiQuery = "Select * from Win32_DiskDrive"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "BytesPerSector: " & objItem.BytesPerSector
 wscript.echo "Capabilities: " & join(objItem.Capabilities)
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "Index: " & objItem.Index
 wscript.echo "InterfaceType: " & objItem.InterfaceType
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MediaType: " & objItem.MediaType
 wscript.echo "Model: " & objItem.Model
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Partitions: " & objItem.Partitions
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "SectorsPerTrack: " & objItem.SectorsPerTrack
 wscript.echo "Signature: " & objItem.Signature
 wscript.echo "Size: " & objItem.Size
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TotalCylinders: " & objItem.TotalCylinders
 wscript.echo "TotalHeads: " & objItem.TotalHeads
 wscript.echo "TotalSectors: " & objItem.TotalSectors
 wscript.echo "TotalTracks: " & objItem.TotalTracks
 wscript.echo "TracksPerCylinder: " & objItem.TracksPerCylinder
wscript.echo " "
next
