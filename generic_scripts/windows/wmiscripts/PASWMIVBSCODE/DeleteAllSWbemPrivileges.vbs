'==========================================================================
'
' COMMENT: <Illustrates obtaining an SWbemPrivilegeSet object at SwbemServices>
'1. adds all privileges via the add method. Pauses for 1.5 seconds Then
'2. Uses the deleteAll method to delete all privileges. 
'==========================================================================

Option Explicit 
'On Error Resume Next
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

subCount
wscript.echo "wait while we delete Privileges":WScript.Sleep(1500)
objWMISecurity.deleteAll
subCount

Sub subCount 'uses count method to count privileges
WScript.echo "How Many Special Privileges? " & objWMISecurity.count 
End sub