
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strSession

strComputer = "."
wmiNS = "\root\cimv2"
strSession = "999"
wmiQuery = "Win32_LogonSession.LogonId=" & strSession
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiquery)


Wscript.echo "AuthenticationPackage:"  & objItem.AuthenticationPackage
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "LogonId:"  & objItem.LogonId
Wscript.echo "LogonType:"  & objItem.LogonType
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "StartTime:"  & objItem.StartTime
Wscript.echo "Status:"  & objItem.Status
