'==========================================================================
'
'
' COMMENT: <Use win32_LogicalShareSecuritySetting class>
'1. retrieves sid and account name with permission on share.
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strShare

strComputer = "."
wmiNS = "\root\cimv2"
strShare = "'a'" 'name of a Share on the system
wmiQuery = "associators of{win32_LogicalShareSecuritySetting="_
	& strSHare & "}where resultClass = win32_sid"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "SID: " & objItem.sid
   	WScript.Echo objItem.accountName   
Next