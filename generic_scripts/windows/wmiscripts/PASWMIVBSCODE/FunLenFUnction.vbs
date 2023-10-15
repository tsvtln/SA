'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Used to determine the longest property description. 
'2. Used in the associatorsOfw32System.vbs script
'3. Call this function by feeding it the property value
'==========================================================================
Function funLen(msg)
If Len(msg) > intL Then intL = Len(msg)
funLen = intL
End Function
