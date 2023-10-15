'==========================================================================
' COMMENT: Key concepts are listed below:
'1.FunFormat function. Breaks output into chunks. 
'2. Use it like  wscript.echo funformat(objItem.description)
'==========================================================================

Function funformat (txt)
Dim width, sp, size, numlines, a, strTxt
width = 55 'How wide to display the text
sp=1 ' the starting position 
size = Len(txt)' the length of the line of text
If size > width Then
	numlines=Int(size/width)' how many lines we will need to display
	'WScript.echo "numline" & numlines
	If numlines * width < size Then numlines = numlines + 1 ' due to rounding of INT
	For a = 1 To numlines
	If a < numLines Then 'this will trim the _ from the last line.
	strtxt= strtxt & mid(txt, sp, width) & "_" & vbcrlf & tab 'line continuation
	Else
	strTxt= strTxt & mid(txt, sp, width) 'no line continuation
	End if
	sp=sp+width ' the starting position is now moved over the width of our text
	next
End If
funformat = strtxt
End function