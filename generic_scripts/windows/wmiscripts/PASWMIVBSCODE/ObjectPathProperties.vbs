'==========================================================================
'
' COMMENT: <Does a Meta_Class query from the schema>
'1. returns information from the schema about classes in namespace
'2. path_ returns an SWbemObjectPath object. This in turn has its own properties
'3. and methods. 
'4. Properties_ returns an SWbemPropertySet object which ONLY has one property: count. It also
'5. has three methods: add, item and remove. Since SWbemPropertySet is a collection, then we 
'6. have to use for each, and then we have an SWbemProperty object which has the name property.
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim a, b, c
Dim strClass
Dim key
Dim strProperties ' holds properties output

strComputer = "."
wmiNS = "\root\cimv2"
strClass = "'Win32_logicalDisk'"
wmiQuery = "Select * from meta_Class where __this ISA " & strClass
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
WScript.Echo "CLASS: " & objItem.path_.Class & " has " & _
	objItem.properties_.count & " properties and " & _
	objItem.qualifiers_.count & " qualifiers."
WScript.Echo "PROPERTIES:"
		For Each b In objItem.properties_
		If IsArray(b) Then
		wscript.echo b.name & " is an Array." & _
		vbcrlf & "The properties are: " & Join (b, ",")
		End if
		WScript.Echo vbtab & b.name
		Next
WScript.Echo "QUALIFIERS:" 
	   For Each a In objItem.qualifiers_
	   If IsArray(a) Then
	   wscript.echo vbtab & a.name & " is an array" & _
	   vbcrlf & vbtab & "The Properties are: " & Join(a, ",")
	   Else
	   WScript.Echo vbtab & a.name & " = " & objItem.qualifiers_.item(a.name)
	   End If
	   Next
WScript.Echo "OBJECT PATH PROPERTIES: "
With objItem.Path_
	strProperties = "displayname " & .displayname & vbcrlf
	strProperties = strProperties & "is class: " & .isClass & vbcrlf
	strProperties = strProperties & "is singleton: " & .IsSingleton & vbcrlf
	strProperties = strProperties & "namespace: " & .namespace & vbcrlf
	strProperties = strProperties & "parentNamespace: " & .parentNamespace & vbcrlf
	strProperties = strProperties & "path: " & .path & vbcrlf
	strProperties = strProperties & "relPath: " & .relpath & vbcrlf
	strProperties = strProperties & "server: " & .server & vbcrlf
	WScript.Echo "keys: " & .keys.count
End With	
WScript.Echo strProperties
Next