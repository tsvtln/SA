'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Deciphers the logical share access mask
'==========================================================================

Function funShare(inMask)
Dim strPerm
If inMask AND 0 Then strPerm = strPerm & "FILE_LIST_DIRECTORY, "
If inMask AND 1 Then strPerm = strPerm & "FILE_ADD_FILE, "
If inMask AND 2 Then strPerm = strPerm & "FILE_ADD_SUBDIRECTORY, "
If inMask AND 3 Then strPerm = strPerm & "FILE_READ_EA, "
If inMask AND 4 Then strPerm = strPerm & "FILE_WRITE_EA, "
If inMask AND 5 Then strPerm = strPerm & "FILE_TRAVERSE, "
If inMask AND 6 Then strPerm = strPerm & "FILE_DELETE_CHILD, "  
If inMask AND 7 Then strPerm = strPerm & "FILE_WRITE_ATTRIBUTES, "  
If inMask AND 8 Then strPerm = strPerm & "FILE_DELETE_CHILD, "  
If inMask AND 16 Then strPerm = strPerm & "DELETE, "  
If inMask AND 17 Then strPerm = strPerm & "READ_CONTROL, "  
If inMask AND 18 Then strPerm = strPerm & "WRITE_DAC, "  
If inMask AND 19 Then strPerm = strPerm & "WRITE_OWNER, "  
If inMask AND 20 Then strPerm = strPerm & "SYNCHRONIZE, " 
funShare = strPerm
End function