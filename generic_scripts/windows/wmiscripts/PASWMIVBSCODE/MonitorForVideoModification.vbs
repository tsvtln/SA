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
objTGT = "'Win32_VideoController'"
wmiNS = "\root\cimv2"

wmiQuery = "SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
Do
   Set objItem = colItems.NextEvent(-1)
   Wscript.Echo "Video Settings were Modified at: " & Now & vbcrlf & _
   space(4) & "Description: " & objItem.TargetInstance.Name & vbcrlf & _
   space(4) & "VideoModeDescription: " & objItem.TargetInstance.VideoModeDescription & vbcrlf & _
   Space(4) & "Previous Settings: " & objItem.PreviousInstance.VideoModeDescription
Loop

WScript.echo "all done"



