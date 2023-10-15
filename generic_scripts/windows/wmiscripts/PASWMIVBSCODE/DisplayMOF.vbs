'==========================================================================
'
' COMMENT: <Returns the MOF of a wmi Class. Uses the GetObjectText_ method>
'
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem, objMOF

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_process"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.Get(wmiQuery)
objMOF = objItem.GetObjectText_
WScript.Echo(objMOF)



