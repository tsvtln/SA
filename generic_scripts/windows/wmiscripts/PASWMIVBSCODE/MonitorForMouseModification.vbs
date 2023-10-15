'==========================================================================
'
' COMMENT: <Uses WMI Eventing>
'1. uses win32_Share and eventing to check for creation of Share
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
Dim objTGT 'monitored class

strComputer = "."
objTGT = "'win32_PointingDevice'"
wmiNS = "\root\cimv2"

wmiQuery = "SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
Do
   Set objItem = colItems.NextEvent(-1)
   Wscript.Echo "Mouse was modified at: " & Now & vbcrlf & _
   space(4) & "name: " & objItem.TargetInstance.Name & vbcrlf & _
   space(4) & "HandedNess: " & objItem.TargetInstance.HandedNess
Loop

WScript.echo "all done"



