'==========================================================================
'
'
' NAME: <BackupAppLog.vbs>
' COMMENT: <Uses the add method to add the backup privilege>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim streventLog
dim objItem, colitems
Dim errRTN, objWMISecurity

strComputer = "."
wmiNS = "\root\cimv2"
Const backup = 16
wmiQuery = "select name from Win32_NTEventlogFile where Name like "
strEventLog = "'%AppEvent.Evt'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.execQuery(wmiQuery & strEventLog)
set objWMISecurity = objWMIService.Security_.privileges
objWMISecurity.add(backup)
subPrivileges

For Each objItem In colitems
errRTN = objItem.BackupEventLog("c:\fso\appLog.evt")
subError
next

Sub subPrivileges
WScript.echo objWMISecurity.count & " privilege exists"
For Each objItem In objWMISecurity:With objItem
wscript.echo .identifier & vbtab & .name & vbtab & .displayname _
			 & vbtab & "is it enabled? " & .isenabled
end with:Next
End Sub

Sub subError
Select Case errRTN
Case 0
	wscript.echo"success!"
Case 8
	wscript.echo"Privilege missing"
Case 21
	wscript.echo"Invalid parameter"
Case 183
	wscript.echo"Archive file name already exists"
Case Else
	wscript.echo"unknown error occurred"
End Select
End sub

