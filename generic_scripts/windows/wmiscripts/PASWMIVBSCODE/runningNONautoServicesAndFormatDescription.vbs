'==========================================================================
'
'
' COMMENT: <Uses ConnectServer method defaults.>
'1. uses a function to format the output from the description property as it
'2. is very long text in some places. 
'3. Breaks the wmi query into parts for ease of understanding and use
'==========================================================================

Option Explicit 
'On Error Resume Next
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim tab : tab=Space(3)
Dim strProperty, strClass, strState
strProperty = "startMode, description" 
strClass = "Win32_Service"
strState = "state = 'running' and startmode <> 'Auto'"

wmiQuery = "Select " & strProperty & " from " & strClass &_
			" where "& strState

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	With objItem
    Wscript.Echo "Name: " & .name & tab & "startMode: " & .startMode
    wscript.echo tab & funformat(.description)
   	End With 
Next

Function funformat (txt)
Dim width, sp, size, numlines, a, strTxt
width = 55 'How wide to display the text
sp=1 ' the starting position 
size = Len(txt)' the length of the line of text
If size > width Then
	numlines=Int(size/width)' how many lines we will need to display
	If numlines * width < size Then numlines = numlines + 1 ' due to rounding of INT
	For a = 1 To numlines
		If a < numLines Then 'this will trim the _ from the last line.
		strtxt= strtxt & mid(txt, sp, width) & "_" & vbcrlf & tab 'line continuation
		Else
		strTxt= strTxt & mid(txt, sp, width) 'no line continuation for last line.
		End if
	sp=sp+width ' the starting position is now moved over the width of our text
	next
End If
funformat = strTxt 'assign results to name of function. 
End function