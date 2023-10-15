'==========================================================================
'
' COMMENT: <Reads the SecurityEvent Log>
'1. Uses SWbemSecurity to add security priviledge to read EventSecurity Log
'2. I did not GET an access Denied message WITHOUT the security Priviledge, 
'3. Just no Records. The interesting THING Here is the construction of the 
'4. Security Line -- INSTEAD of using the MONIKER
'5. Uses the Win32_NTLogEvent Class
'6. Refer to the SWbemPrivilegeSet.AddAsString article in SDK 
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer 'can be any computer
dim wmiNS 'the wmi name space - root\cimv2 is where win32_NTLogEvent resides
dim wmiQuery 'the actual wmi query itself
dim objWMIService 'connection into wmi
dim colItems 'collection of events
dim objItem 'used to walk through the collection
Dim strEventCode 'event code to look for

strComputer = "."
strEventCode = "'529'"
wmiNS = "\root\cimv2"
wmiQuery = "SELECT * FROM Win32_NTLogEvent WHERE Logfile = 'security'"_
	& "AND EventCode = " & strEventCode
Const Enable = "true" 'true will turn on the privilege, FALSE turns OFF
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
objWMIService.security_.Privileges.addASstring _
	"seSecurityPrivilege", Enable
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo ": " & objItem.TimeGenerated 
    Wscript.Echo ": " & objItem.message
Next