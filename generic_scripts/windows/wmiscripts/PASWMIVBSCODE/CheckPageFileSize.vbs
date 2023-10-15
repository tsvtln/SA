'==========================================================================
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
wmiQuery = "Select InitialSize, name from win32_PageFileSetting"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "InitialSize: " & objItem.InitialSize
Next