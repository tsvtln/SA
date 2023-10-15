'==========================================================================
'
' COMMENT: <Use this script to compare two classes>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colProperties, colMethods
dim objItem
Dim strClass
Dim strPrompt, strTitle, strDef
strPrompt = "Enter classes to compare. use , to separate"
strTitle = "Compare Methods and Properties"
strDef = "win32_PointingDevice,cim_PointingDevice"
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = InputBox(strPrompt, strTitle, strDef)

wmiQuery = Split(wmiQuery,",")
For Each strClass In wmiQuery
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS & funFIX(strClass))
Set colProperties = objWMIService.properties_
Set colMethods = objWMIService.methods_
WScript.Echo strClass & " has " & colProperties.count & " Properties and " _
 & colMethods.count & " Methods"
next

Function funFix(strIN)
funFix = ":" & strIN
End function