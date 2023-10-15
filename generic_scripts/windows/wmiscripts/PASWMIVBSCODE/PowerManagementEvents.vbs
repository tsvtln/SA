'==========================================================================
'
' COMMENT: <Uses the powermanagement provider to monitor for power events>
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
Dim objTGT
strComputer = "."
objTGT = "'win32_PowerManagementEvent'"
wmiNS = "\root\cimv2"
wmiQuery = "SELECT * FROM win32_PowerManagementEvent"
            
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)

Do
    Set objItem = colItems.NextEvent
    Wscript.Echo "EventType: " & funLookup(objItem.EventType)
loop


Function funLookup(intStatus)
Select Case intStatus
Case 4
funLookup ="Entering Suspend"
Case 7
funLookup ="Resume from Suspend"
Case 10
funLookup ="Power Status Change"
Case 11
funLookup ="OEM Event"
Case 17
funLookup ="Resume Automatic"
Case Else
funLookup ="unknown"
End Select
End function