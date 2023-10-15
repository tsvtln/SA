

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
wmiNS = "\root\cimv2"
intLogon = """999""}"
wmiQuery = "References of {win32_LogonSession.LogonId=" & intLogon
'wmiQuery = "References of {win32_LogonSession.LogonId=" & intLogon & " where classdefsonly"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	Wscript.Echo objItem.path_
Next