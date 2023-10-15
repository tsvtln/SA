'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Uses an instanceModificationEvent query to monitor for changes in the
'2.state of a service. This tells if a service is started or stopped.
'3. Uses win32_service class to get this information. 
'4. We are checking for changes every 10 seconds, in production do Not
'5. Check this often. 
'==========================================================================

strComputer = "."
wmiNS = "\root\cimv2"
objClass = "'Win32_Service'"
StrMessage = "A " & objClass & " was modified at : "
strMessage1 = "The Service is now: "
wmiQuery = "SELECT * FROM __InstanceModificationEvent " _
        & "WITHIN 10 WHERE TargetInstance ISA " & objClass
           
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)

Do
Set objItem = colItems.NextEvent
With objItem
    Wscript.Echo StrMessage & Now & vbcrlf & strMessage1 & _
    .TargetInstance.State & vbcrlf & .TargetInstance.Name & _
    vbtab & .TargetInstance.PathName & vbtab & "PID: " & _
    .TargetInstance.ProcessId
End with
loop
