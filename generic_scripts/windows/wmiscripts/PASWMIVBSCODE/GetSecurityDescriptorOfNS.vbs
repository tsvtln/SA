'==========================================================================
'
' COMMENT: <Gets the security descriptor of a wmi namespace>
'1. need to check for error because will error out if try join a null. 

'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim strSD
dim objItem
Dim errRTN
strComputer = "."
wmiNS = "\root\wmi"
wmiQuery = "__SystemSecurity=@"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.Get(wmiQuery)

errRTN = objItem.GetSD(strSD)

SubCheckERR

  Wscript.Echo forMatSD(strSD)
  
Sub subCheckERR
If errRTN <> 0 Then
WScript.Echo "an error occurred. It was " & errRTN
WScript.Quit
End If
End sub  
  
Function forMatSD(strSD)
forMatSD = "{" & join(strSD,",") & "}"
End Function
