Option Explicit
Dim strComputer
Dim objSWbemServices
Dim objNameSpace
Dim colNameSpaces
Dim secSTR
Dim myTab:mytab=Space(5)
strComputer = "."

Call EnumNameSpaces("root")

WScript.Echo("all done " & Now)

'#### functions and Subs below #####

Sub EnumNameSpaces(strNameSpace)
  secSTR= funAccess("\" & strNameSpace)
	WScript.Echo ("\" & strNameSpace)
    WScript.Echo myTab & secSTR & myTab & funNSSEC(secSTR)
  Set objSWbemServices = _
    GetObject("winmgmts:\\" & strComputer & "\" & strNameSpace)
  Set colNameSpaces = objSWbemServices.InstancesOf("__NAMESPACE")
    For Each objNameSpace In colNameSpaces
     Call EnumNameSpaces(strNameSpace & "\" & objNameSpace.Name)
    Next
End Sub

Function funAccess(wmiNS) 'retrieves security descriptor from NS
dim wmiQuery
dim objWMIService
dim strSD
dim objItem
Dim errRTN
wmiQuery = "__SystemSecurity=@"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
  errRTN=objItem.GetCallerAccessRights(strSD)
  funAccess= strSD
End Function

Function funNSSEC (inMASK) 'Deciphers the security descriptor
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