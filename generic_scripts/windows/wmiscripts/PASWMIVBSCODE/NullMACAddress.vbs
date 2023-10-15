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
wmiQuery = "Select * from Win32_NetworkAdapter where MACAddress IS null"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "Index: " & objItem.Index
 wscript.echo "Installed: " & objItem.Installed
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NetConnectionID: " & objItem.NetConnectionID
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "ProductName: " & objItem.ProductName
 wscript.echo "ServiceName: " & objItem.ServiceName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TimeOfLastReset: " & objItem.TimeOfLastReset
wscript.echo " "
next
