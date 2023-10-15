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
wmiQuery = "Select * from Win32_NamedJobObject"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "BasicUIRestrictions: " & objItem.BasicUIRestrictions
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CollectionID: " & objItem.CollectionID
 wscript.echo "Description: " & objItem.Description
wscript.echo " "
next
