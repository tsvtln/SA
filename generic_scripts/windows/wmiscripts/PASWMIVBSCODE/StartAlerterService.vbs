
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
wmiQuery = "win32_service.name='alerter'" 'make sure you do not have a space in here! 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

If objItem.state = "Running" then
 WScript.echo   objItem.stopService()
 Else
WScript.Echo objItem.startService()
End if
