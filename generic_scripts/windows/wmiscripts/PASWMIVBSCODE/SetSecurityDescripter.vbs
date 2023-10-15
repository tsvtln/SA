'==========================================================================
'
'
' COMMENT: <The following script shows you how to use SetSD 
'to obtain the current security descriptor for the Root\Cimv2 
'namespace and change it to the byte array shown in DisplaySD.>
' Refer to the __SystemSecurity class in the SDK
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems ' holds the return from the wmi query
dim errReturn ' return value from getting the security descripter
Dim arrSD ' array that holds the security descriptor
Dim DisplaySD
Dim i
Dim arSD ' array for new Security Descriptor

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "__SystemSecurity=@"
arSD= array(1,0,4,128,184,0,0,0,200,0,0,0,0,0,0,0,20,0,0,0,2,0,164,0,6,0,0,0,0,0,36,0,35,0,0,0,1,5,0,0,0,0,0,5,21,0,0,0,182,68,228,35,192,133,56,93,22,192,234,50,248,3,0,0,0,2,36,0,32,0,2,0,1,5,0,0,0,0,0,5,21,0,0,0,160,101,207,126,120,75,155,95,231,124,135,112,149,89,0,0,0,18,24,0,63,0,6,0,1,2,0,0,0,0,0,5,32,0,0,0,32,2,0,0,0,18,20,0,19,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,18,20,0,19,0,0,0,1,1,0,0,0,0,0,5,20,0,0,0,0,18,20,0,19,0,0,0,1,1,0,0,0,0,0,5,19,0,0,0,1,2,0,0,0,0,0,5,32,0,0,0,32,2,0,0,1,2,0,0,0,0,0,5,32,0,0,0,32,2,0,0)
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.Get(wmiQuery) ' note using Get not ExecQuery

WScript.Echo "Preparing to change the SD"

SubChangeSD

Sub SubChangeSD
errReturn = colItems.SetSD(arSD)
If Err <> 0 Then
   WScript.Echo "Method returned error " & errReturn
Else
WScript.Echo "SD was changed"
End If
End sub