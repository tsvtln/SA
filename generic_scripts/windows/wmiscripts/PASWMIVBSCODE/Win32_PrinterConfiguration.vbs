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
wmiQuery = "Select * from Win32_PrinterConfiguration"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "BitsPerPel: " & objItem.BitsPerPel
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Collate: " & objItem.Collate
 wscript.echo "Color: " & objItem.Color
 wscript.echo "Copies: " & objItem.Copies
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceName: " & objItem.DeviceName
 wscript.echo "DisplayFlags: " & objItem.DisplayFlags
 wscript.echo "DisplayFrequency: " & objItem.DisplayFrequency
 wscript.echo "DitherType: " & objItem.DitherType
 wscript.echo "DriverVersion: " & objItem.DriverVersion
 wscript.echo "Duplex: " & objItem.Duplex
 wscript.echo "FormName: " & objItem.FormName
 wscript.echo "HorizontalResolution: " & objItem.HorizontalResolution
 wscript.echo "ICMIntent: " & objItem.ICMIntent
 wscript.echo "ICMMethod: " & objItem.ICMMethod
 wscript.echo "LogPixels: " & objItem.LogPixels
 wscript.echo "MediaType: " & objItem.MediaType
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Orientation: " & objItem.Orientation
 wscript.echo "PaperLength: " & objItem.PaperLength
 wscript.echo "PaperSize: " & objItem.PaperSize
 wscript.echo "PaperWidth: " & objItem.PaperWidth
 wscript.echo "PelsHeight: " & objItem.PelsHeight
 wscript.echo "PelsWidth: " & objItem.PelsWidth
 wscript.echo "PrintQuality: " & objItem.PrintQuality
 wscript.echo "Scale: " & objItem.Scale
 wscript.echo "SettingID: " & objItem.SettingID
 wscript.echo "SpecificationVersion: " & objItem.SpecificationVersion
 wscript.echo "TTOption: " & objItem.TTOption
 wscript.echo "VerticalResolution: " & objItem.VerticalResolution
 wscript.echo "XResolution: " & objItem.XResolution
 wscript.echo "YResolution: " & objItem.YResolution
wscript.echo " "
next
