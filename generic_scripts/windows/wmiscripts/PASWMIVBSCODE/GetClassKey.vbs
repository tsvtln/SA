'==========================================================================
'
' COMMENT: <Gets the Key and the key value from a WMI Class>
'1. returns a collection of SWbemQualifier objects, enumerates the name
'2. Then uses INSTR to filter out if the name is equal to key. 
'3. Changed to use a INPUT box. 
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
Dim wmiClass
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim a, b, strMSG, strTab
Dim strPrompt, strTitle, strDefault 'use for input box
strTab = VBcrlf & vbtab
strPrompt="Enter Class name":strTitle="WMI Key finder":strDefault="Win32_computerSystem"
strComputer = "."
wmiNS = "\root\cimv2"
wmiClass = InputBox(strPrompt,strTitle,strDefault)
wmiQuery = "Select * from " & wmiClass
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	For Each a In objItem.properties_ 'returns a property set object
   		For Each b In a.qualifiers_ 'returns a collection of swbemQualifier objects
			If InStr (b.name, "key") Then
				strMSG = strMSG & VBcrlf & "Property Name: " & a.name
			    strMSG = strMSG & VBcrlf & "Property value: " & a.value
				strMSG = strMSG & strTab & "qualifier name: " & b.name 'name of PROPERTY QUALIFIER
				strMSG = strMSG & strTab & "qualifier value: " & b.value 'When Key set, ONLY TRUE
			End if
		Next
	next
Next
WScript.Echo(strMSG)
	