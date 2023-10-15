'==========================================================================
'
' COMMENT: <Delete a service called notepad>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim errRTn
dim objItem
Dim strServiceName

strComputer = "."
wmiNS = "\root\cimv2"
strServiceName = "'notepad'"
wmiQuery = "win32_service.name=" & strServiceName
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

errRTN=objItem.delete("notepad")
WScript.Echo(errRTN)