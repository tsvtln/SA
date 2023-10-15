'==========================================================================
'
' COMMENT: <Lists out all properties associated with a WMI Class
' to do this, we make our connection to the class itself instead of
' just to the wmi namespace. The properties in a class are the properties_ 
' attribute. The trailing _ is required. THe class name must have a : in front 
' of it. >
'
'==========================================================================

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
i=0 ' used to resize the dynamic array
b=0 ' used for Walking through the array

strComputer = "."
wmiNS = "\root\CIMV2" 'Change namespace if needed
strClass = "Win32_pointingDevice" 'Here is the Class Name

Set objClass = GetObject("winmgmts:\\" & strComputer & wmiNS & ":" & strClass)
For Each objItem in objClass.Properties_
	ReDim Preserve array1(i)	
    array1(i) = objItem.name 
           i = i + 1   
 Next
 
 For  b = 0 To UBound(Array1)
prop= prop & Array1(b) & vbcrlf
 Next

WScript.Echo(prop)' prints out all properties at once