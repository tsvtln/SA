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
wmiQuery = "Select * from Win32_DisplayConfiguration"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "BitsPerPel: " & objItem.BitsPerPel
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceName: " & objItem.DeviceName
 wscript.echo "DisplayFlags: " & objItem.DisplayFlags
 wscript.echo "DisplayFrequency: " & objItem.DisplayFrequency
 wscript.echo "DitherType: " & objItem.DitherType
 wscript.echo "DriverVersion: " & objItem.DriverVersion
 wscript.echo "ICMIntent: " & objItem.ICMIntent
 wscript.echo "ICMMethod: " & objItem.ICMMethod
 wscript.echo "LogPixels: " & objItem.LogPixels
 wscript.echo "PelsHeight: " & objItem.PelsHeight
 wscript.echo "PelsWidth: " & objItem.PelsWidth
 wscript.echo "SettingID: " & objItem.SettingID
 wscript.echo "SpecificationVersion: " & objItem.SpecificationVersion
wscript.echo " "
next
