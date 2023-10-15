'==========================================================================
'
' COMMENT: <ClearEventlog.VBS>
'1. uses win32_NTEventlogFile. 

'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim LogFile, rtnCode

strComputer = "."
wmiNS = "\root\cimv2"
LogFile = "'application'"
wmiQuery = "Select * from win32_NTEventlogFile where LogfileName = "& LogFile

Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate,(backup)}\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
rtnCode = objItem.ClearEventLog'() are optional. Logname generates error
WScript.echo rtnCode
Next


