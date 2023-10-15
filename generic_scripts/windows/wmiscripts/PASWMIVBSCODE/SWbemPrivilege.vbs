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

dim objWMIService

dim objItem
Dim objWMISecurity ' contains an SWbemPrivilegeSet

strComputer = "."
wmiNS = "\root\cimv2"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
set objWMISecurity = objWMIService.Security_.privileges 'creates swbemPrivilegeSet

objWMISecurity.add(1):objWMISecurity.add(2):objWMISecurity.add(3)
WScript.echo "How Many Special Privileges? " & objWMISecurity.count

WScript.echo "Status of priv. 3: " & objWMISecurity.item(3) 'to retrieve status of specific privilege

For Each objItem In objWMISecurity:With objItem
wscript.echo .identifier & vbtab & .name & vbtab & .displayname _
			 & vbtab & .isenabled
end with:next

 
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