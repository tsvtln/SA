Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim objSecurity

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_computerSystem"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)

Set colItems = objWMIService.ExecQuery(wmiQuery)
'objWMIservice.security_.privileges.addAsString "SeSystemEnvironmentPrivilege"
objWMIservice.security_.privileges.deleteall
Set objSecurity = objWMIservice.Security_.Privileges
WScript.echo "Number of Privileges held: " & objSecurity.count
For Each objItem in colItems
    Wscript.Echo "SystemStartupOptions: " & join(objItem.SystemStartupOptions, "," & vbcrlf) 
Next