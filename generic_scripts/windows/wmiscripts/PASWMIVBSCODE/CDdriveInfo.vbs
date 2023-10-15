Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_CDROMDrive"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "Caption: " & objItem.Caption

if instr(1,objItem.caption,"DVD",1) <> 0 then
	WScript.echo "this drive is a DVD player"
End If

wscript.echo "Drive: " & objItem.Drive
wscript.echo "SystemName: " & objItem.SystemName
Next

