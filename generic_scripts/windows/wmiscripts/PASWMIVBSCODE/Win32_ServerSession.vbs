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
wmiQuery = "Select * from Win32_ServerSession"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "ActiveTime: " & objItem.ActiveTime
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ClientType: " & objItem.ClientType
 wscript.echo "ComputerName: " & objItem.ComputerName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "IdleTime: " & objItem.IdleTime
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "Name: " & objItem.Name
 wscript.echo "ResourcesOpened: " & objItem.ResourcesOpened
 wscript.echo "SessionType: " & objItem.SessionType
 wscript.echo "Status: " & objItem.Status
 wscript.echo "TransportName: " & objItem.TransportName
 wscript.echo "UserName: " & objItem.UserName
wscript.echo " "
next
