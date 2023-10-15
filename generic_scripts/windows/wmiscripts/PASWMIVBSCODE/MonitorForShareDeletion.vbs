'==========================================================================
'
' COMMENT: <Uses WMI Eventing>
'1. uses win32_Share and eventing to check for Deletion of Share
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
objTGT = "'win32_Share'"
wmiNS = "\root\cimv2"

wmiQuery = "SELECT * FROM __InstanceDeletionEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
Do
   Set objItem = colItems.NextEvent(-1)
   Wscript.Echo "A Share was deleted at: " & Now & vbcrlf & _
   space(4) & "share name: " & objItem.TargetInstance.Name & vbcrlf & _
   space(4) & "share path: " & objItem.TargetInstance.Path
Loop

WScript.echo "all done"



