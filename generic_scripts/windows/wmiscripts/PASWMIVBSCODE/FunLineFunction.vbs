'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.FunLine function. Used to count length of a line
'2.and then underline it. Produces cleaner output. 
'3. use: funLine(objItem.Path_.Class)
'==========================================================================

Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText) + 42
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = separater
End Function