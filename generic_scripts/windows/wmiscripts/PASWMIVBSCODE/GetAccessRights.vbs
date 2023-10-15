
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim strSD
dim objItem
Dim errRTN
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "__SystemSecurity=@"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

errRTN = objItem.GetCallerAccessRights(strSD)
  Wscript.Echo strSD
  WScript.Echo funNSSEC(strSD)


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