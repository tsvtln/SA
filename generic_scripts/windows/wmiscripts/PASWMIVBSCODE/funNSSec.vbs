'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.the fun namespace security function decodes the wmi NS security descriptor
'2.It is used in the GetAccessRightsInALLNameSpaces.vbs script.
'==========================================================================


Function funNSSEC (inMASK)
Dim strPerm
If inMask AND 1 Then strPerm = strPerm & "WBEM_ENABLE, "
If inMask AND 2 Then strPerm = strPerm & "WBEM_METHOD_EXECUTE, "
If inMask AND 4 Then strPerm = strPerm & "WBEM_FULL_WRITE_REP, "
If inMask AND 8 Then strPerm = strPerm & "WBEM_PARTIAL_WRITE_REP, "
If inMask AND 16 Then strPerm = strPerm & "WBEM_WRITE_PROVIDER, "
If inMask AND 32 Then strPerm = strPerm & "WBEM_REMOTE_ACCESS, "
If inMask AND 131072 Then strPerm = strPerm & "READ_CONTROL, "
If inMask AND 262144 Then strPerm = strPerm & "WRITE_DAC, "
funNSSEC = strPerm
End function