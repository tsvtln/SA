'==========================================================================
'
' COMMENT: <uses wmi to query status of WPA activation>
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
wmiQuery = "Select * from Win32_WindowsProductActivation"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "ActivationRequired: " & objItem.ActivationRequired
    Wscript.Echo "IsNotificationOn: " & objItem.IsNotificationOn
    Wscript.Echo "ProductID: " & objItem.ProductID
    Wscript.Echo "RemainingEvaluationPeriod: " & objItem.RemainingEvaluationPeriod
    Wscript.Echo "RemainingGracePeriod: " & objItem.RemainingGracePeriod
    Wscript.Echo "ServerName: " & objItem.ServerName
Next