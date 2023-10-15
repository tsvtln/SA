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
wmiQuery = "Select * from Win32_PhysicalMedia"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Capacity: " & objItem.Capacity
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CleanerMedia: " & objItem.CleanerMedia
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "HotSwappable: " & objItem.HotSwappable
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MediaDescription: " & objItem.MediaDescription
 wscript.echo "MediaType: " & objItem.MediaType
 wscript.echo "Model: " & objItem.Model
 wscript.echo "Name: " & objItem.Name
 wscript.echo "OtherIdentifyingInfo: " & objItem.OtherIdentifyingInfo
 wscript.echo "PartNumber: " & objItem.PartNumber
 wscript.echo "PoweredOn: " & objItem.PoweredOn
 wscript.echo "Removable: " & objItem.Removable
 wscript.echo "Replaceable: " & objItem.Replaceable
 wscript.echo "SerialNumber: " & objItem.SerialNumber
 wscript.echo "SKU: " & objItem.SKU
 wscript.echo "Status: " & objItem.Status
 wscript.echo "Tag: " & objItem.Tag
 wscript.echo "Version: " & objItem.Version
 wscript.echo "WriteProtectOn: " & objItem.WriteProtectOn
wscript.echo " "
next
