'==========================================================================
'
'
' COMMENT: <Use OperatingSYstem Event>
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

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "SELECT * FROM Win32_ProcessStartTrace"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
        WScript.Echo "Waiting for process to start ..."
    Do
        Set objItem = colItems.NextEvent
        With objItem
            Wscript.Echo "StartedProcess Name: " & .ProcessName
            Wscript.Echo "Process ID: " & .ProcessId
            WScript.Echo "Time Generated: " & .Time_Created
            WScript.Echo "SID: " & Join(.SID) 
			WScript.Echo "Session ID: " & .sessionID
        End With
  Loop