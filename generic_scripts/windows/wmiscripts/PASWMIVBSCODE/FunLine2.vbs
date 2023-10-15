'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.new version of the funline function
'2.uses the string function to build the line
'==========================================================================

'below is demo
WScript.Echo myFun("this is a random line of stuff to underline")

' #### Function is below #####


Function myFun(input)
Dim lstr
lstr = Len(input)
myFun = input & vbcrlf & string(lstr,"=")
End function
