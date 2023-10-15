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
wmiQuery = "Select * from Win32_Share"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AccessMask: " & objItem.AccessMask
 wscript.echo "AllowMaximum: " & objItem.AllowMaximum
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "MaximumAllowed: " & objItem.MaximumAllowed
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Path: " & objItem.Path
 wscript.echo "Status: " & objItem.Status
 wscript.echo "Type: " & objItem.Type
wscript.echo " "
next
