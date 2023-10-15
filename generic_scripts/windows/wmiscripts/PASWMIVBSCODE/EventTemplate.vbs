
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim objTGT 'monitored class

strComputer = "."
objTGT = "'Win32_'"
wmiNS = "\root\cimv2"

wmiQuery = "SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
Do
   Set objItem = colItems.NextEvent(-1)
   Wscript.Echo  "Settings were Modified at: " & Now & vbcrlf & _
   space(4) & "Description: " & objItem.TargetInstance.Name
Loop

WScript.echo "all done"