'==========================================================================
'
' COMMENT: <Uses WMI Eventing>
'1. uses win32_Process and eventing to check on deletion of processes
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
Dim objName ' monitored item
Dim objTGT 'monitored class

strComputer = "."
objName = "'notepad.exe'" 
objTGT = "'win32_Process'"
wmiNS = "\root\cimv2"

wmiQuery = "SELECT * FROM __InstanceDeletionEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT & " AND " _
            & "TargetInstance.Name=" & objName
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)

Do
    Set objItem = colItems.NextEvent(-1)
    Wscript.Echo "Name: " & objItem.TargetInstance.Name & " " & now
    Wscript.Echo "ProcessID: " & objItem.TargetInstance.ProcessId 
Loop

WScript.echo "all done"



