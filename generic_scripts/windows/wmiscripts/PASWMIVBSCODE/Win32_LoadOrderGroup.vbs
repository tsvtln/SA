Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_LoadOrderGroup"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DriverEnabled: " & objItem.DriverEnabled
 wscript.echo "GroupOrder: " & objItem.GroupOrder
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Status: " & objItem.Status & vbcrlf
next
