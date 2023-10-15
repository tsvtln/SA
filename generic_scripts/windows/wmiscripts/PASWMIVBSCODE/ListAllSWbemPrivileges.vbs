'==========================================================================
'
' COMMENT: <Illustrates obtaining an SWbemPrivilegeSet object at SwbemServices>
'
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
Dim i
dim objWMIService
dim objItem
Dim objWMISecurity ' contains an SWbemPrivilegeSet

strComputer = "."
wmiNS = "\root\cimv2"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
set objWMISecurity = objWMIService.Security_.privileges 'creates swbemPrivilegeSet
For i = 1 To 27
objWMISecurity.add(i)
Next

WScript.echo "How Many Special Privileges? " & objWMISecurity.count

For Each objItem In objWMISecurity:With objItem
wscript.echo .identifier & vbtab & .name & vbtab & .displayname _
			 & vbtab & .isenabled
end with:next

