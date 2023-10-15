'==========================================================================
'
'
' COMMENT: <Queries and starts a service>
'1. uses the win32_serice class
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim objName
Dim errRTN

objName = "'alerter'"
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select state,startmode from win32_service where Name = " & objName
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo ": " & objItem.state
    Wscript.Echo ": " & objItem.startmode
 If objItem.state <> "running" Then
 errRTN =objItem.startservice
 End If
 WScript.echo errRTN
Next