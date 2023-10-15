'==========================================================================
' NAME: <AssociatorsOfLogonSession.vbs>
'
' COMMENT: <Uses an associators type of query.>
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
Dim intLogon

strComputer = "."
intLogon = """999""}"
wmiNS = "\root\cimv2"
wmiQuery = "associators of {win32_LogonSession.LogonId=" & intLogon
'wmiQuery = "associators of {win32_LogonSession.LogonId=""999""}"

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo objItem.path_
Next