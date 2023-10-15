'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Use to parse results of VarType
'2.
'3. 
'==========================================================================

strNull = "" 'this is considered to be a string!
strInt = 7
WScript.echo "StrNull " & funType(VarType(strNull))
WScript.echo "strInt " & funType(VarType(strInt))

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