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
strPrompt="Enter Class name":strTitle="WMI Key finder":strDefault="Win32_WMIsetting"
strComputer = "."
wmiNS = "\root\cimv2"
wmiClass = InputBox(strPrompt,strTitle,strDefault)
wmiQuery = "Select * from " & wmiClass
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	For Each a In objItem.properties_ 'returns a property set object
   		WScript.echo "property is " & a.name
   		WScript.echo "item " & a.item
   		For Each b in a.qualifiers_
   		WScript.echo funtype(vartype(b))
   		next
	next
Next


Function funType(strType)
	Select Case strType
	case 0	
		funType ="vbEmpty"
	case 1	
		funType ="vbNull"
	case 2	
		funType ="vbInteger"
	case 3	
		funType ="vbLong"
	case 4	
		funType ="vbSingle"
	case 5
		funType ="vbDouble"
	case 6
		funType ="vbCurrency"
	case 7
		funType ="vbDate"
	case 8
		funType ="vbString"
	case 9
		funType ="vbObject"
	case 10	
		funType ="vbError"
	case 11
		funType ="vbBoolean"
	case 12
		funType ="vbVariant"
	case 13
		 funType ="vbDataObject"
	case 17
		funType ="vbByte"
	case 8192
		funType ="vbArray"
	Case Else
		funType ="dude no idea"
	End Select 
End function
	