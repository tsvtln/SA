
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem


'Const wbemFlagReturnImmediately = &h10
'Const wbemFlagForwardOnly = &h20
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_SystemBIOS"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
'Set colItems = objWMIService.ExecQuery(wmiQuery,"wql",wbemFlagReturnImmediately + wbemFlagForwardOnly)
Set colItems = objWMIService.ExecQuery(wmiQuery,"wql",&h10 + &h20)
For Each objItem in colItems
     WScript.Echo "GroupComponent: " & objItem.GroupComponent
     WScript.Echo "PartComponent: " & objItem.PartComponent
     WScript.Echo
Next

