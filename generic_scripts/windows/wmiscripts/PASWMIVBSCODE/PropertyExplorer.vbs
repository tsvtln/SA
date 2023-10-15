'==========================================================================
'
' COMMENT: <Lists out all properties associated with a WMI Class
' to do this, we make our connection to the class itself instead of
' just to the wmi namespace. The properties in a class are the properties_ 
' attribute. The trailing _ is required. THe class name must have a : in front 
' of it. >
'
'==========================================================================
'Header section
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim objClass
dim colItems
dim objItem
Dim strClass
Dim Array1()' holds all the class Properties
Dim i,b
Dim wmiquery
Dim objWMIService, item, prop ' prop holds ALL the properties
Dim StrPrompt, StrTitle, StrDefault ' used for InputBox Function

'Reference Section
i=0 ' used to resize the dynamic array
b=0 ' used for Walking through the array
strComputer = "."
wmiNS = "\root\CIMV2" 'Change namespace if needed
StrPrompt = "Type in the class to explore"
StrTitle = "ClassExplorer"
StrDefault = "Win32_LogonSession"
strClass = inputbox(Strprompt, Strtitle, StrDefault) 'Supply class to input box.

'Worker Section
Set objClass = GetObject("winmgmts:\\" & strComputer & wmiNS & ":" & strClass)
For Each objItem in objClass.Properties_
	ReDim Preserve array1(i)	
    array1(i) = objItem.name 
           i = i + 1   
 Next
 
 
 For  b = 0 To UBound(Array1)
'prop= prop  & "Wscript.echo objItem." & Array1(b) & vbcrlf
prop= prop  & "Wscript.echo " & """" & Array1(b) & ":""" & "  & objItem." & Array1(b) & vbcrlf
 Next

'OutPut Section of Script
WScript.Echo(prop)' prints out all properties at once
