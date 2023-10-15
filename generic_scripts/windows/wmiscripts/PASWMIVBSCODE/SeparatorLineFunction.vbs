'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1. This script will format a separator line based upon the length of
'2. the input line. 
'3. We then use stdOut to output the information. 
'4. the Len command is used to get the length of a line
'5. For next is used to create our separator line. 
'==========================================================================
Option Explicit
Dim stdOut
Dim lineOfText

Set StdOut = WScript.stdOut 

lineOfText = "This is a long line of text used with thr to make it really longer function"

WScript.echo funLine(lineOfText)

'#### here is the actual function #####

Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End function
