'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.will center  give numbers used to center one line upon another
'2.Trick was subtracking half length of the text TO center from the centeree.
'3. example of use in AssociatorsOfW32System.vbs script.
'==========================================================================
'global variable strSYS holds value to CENTER.
'value passed as intL holds what will be centered UPON>
Function funCenter(intL)'used to get space value used to center name
intL = (intL)/2 'gives 1/2 of longest line
intL = intL - (Len(strSYS)/2)'get 1/2 if sysName sub from intL
funCenter = intL
End function