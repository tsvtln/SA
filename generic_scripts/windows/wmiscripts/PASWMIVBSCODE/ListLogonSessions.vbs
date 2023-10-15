'==========================================================================
'
' COMMENT: <Use as a WMI Template>
'
'==========================================================================

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
wmiQuery = "Select * from win32_logonsession"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "AuthenticationPackage:"  & objItem.AuthenticationPackage
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "LogonId:"  & objItem.LogonId
Wscript.echo "LogonType:"  & objItem.LogonType
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "StartTime:"  & objItem.StartTime
Wscript.echo "Status:"  & objItem.Status
WScript.Echo ""
Next