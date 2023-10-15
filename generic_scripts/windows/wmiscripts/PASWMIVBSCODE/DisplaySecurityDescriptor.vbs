'==========================================================================
'
'
' COMMENT: <Uses the __SystemSecurity class to display the security descriptor>
'1. Uses @ to point to running copy of wmi. 
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim intRTN
Dim arrSD, intSD
Dim i
strComputer = "."
wmiNS = "\root\wmi"
wmiQuery = "__SystemSecurity=@"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.Get(wmiQuery)
intRTN = objItem.getSD(arrSD)
For I = 0 To UBound(arrSD)
intSD = intSD & arrSD(i)
	If I <> Ubound(arrSD) Then
      intSD = intSD & ","
   	End If
Next
WScript.echo intSD
