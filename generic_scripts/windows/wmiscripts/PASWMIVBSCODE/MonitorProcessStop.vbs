
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "SELECT * FROM Win32_ProcessStopTrace"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
        WScript.Echo "Waiting for process to stop ..."
    Do
        Set objItem = colItems.NextEvent
        With objItem
            Wscript.Echo "StoppedProcess Name: " & .ProcessName
            Wscript.Echo "Process ID: " & .ProcessId
            WScript.Echo "Exit Status: " & .ExitStatus
        End With
  Loop