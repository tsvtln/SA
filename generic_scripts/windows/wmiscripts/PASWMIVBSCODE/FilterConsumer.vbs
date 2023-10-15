'==========================================================================
'
' COMMENT: <Displays Permenant event to consumer bindings>
'
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from __FilterToConsumerBinding"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "Consumer Name: " & objItem.consumer
    Wscript.Echo "CreatorSID: " & join(objItem.CreatorSID)
    Wscript.Echo "Name of the event filter: " & objItem.Filter 
    Wscript.Echo "MaintainSecurityContext: " & objItem.MaintainSecurityContext 
    Wscript.Echo "SlowDownProviders: " & objItem.SlowDownProviders 
Next