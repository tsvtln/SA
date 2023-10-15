'==========================================================================
'
'
' COMMENT: <Illustrates obtaining an SWbemPrivilegeSet object at SwbemServices>
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
Dim objWMISecurity ' contains an SWbemPrivilegeSet

strComputer = "."
wmiNS = "\root\cimv2"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
set objWMISecurity = objWMIService.Security_.privileges 'creates swbemPrivilegeSet
objWMISecurity.add(1)
WScript.echo "How Many Special Privileges? " & objWMISecurity.count
 
' Set colItems = objWMIService.ExecQuery(wmiQuery)
' 
' For Each objItem in colItems
'     Wscript.Echo ": " & objItem.
'     Wscript.Echo ": " & objItem.
'     Wscript.Echo ": " & objItem.
'     Wscript.Echo ": " & objItem.
'     Wscript.Echo ": " & objItem.
'     Wscript.Echo ": " & objItem.
' Next