'==========================================================================
'
'
' COMMENT: <Does listing of WMI NameSpaces>
'1. Uses the ExecQuery method to retrieve the names of all wmi namespaces
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
wmiNS = "\root"
wmiQuery = "Select * from __NameSpace"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo ": " & objItem.name
Next