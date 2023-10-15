'==========================================================================
'
'
' COMMENT: <Illustrates use of ITEM method to access specific privilege>
'1. uses HEX function to translate error code to hexidecimal for lookup in SDK
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim objWMISecurity

Const backup=16
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_Win32_NTEventlogFile"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
Set objWMISecurity = objWMIService.security_.privileges
objWMISecurity.add(backup)

subcount
WScript.sleep 1500:WScript.echo "deleting privilege"
objWMISecurity.remove(backup)
subCount

Sub subcount
wscript.echo "There is: " & objWMISecurity.count & " privileges"
End sub