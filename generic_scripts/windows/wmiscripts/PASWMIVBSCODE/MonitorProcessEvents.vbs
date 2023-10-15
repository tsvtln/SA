strComputer = "."
wmiNS = "\root\cimv2"
objClass = "'Win32_Process'"
StrMessage = "A new " & objClass & " was created at : "
wmiQuery = "SELECT * FROM __InstanceCreationEvent " _
        & "WITHIN 10 WHERE TargetInstance ISA " & objClass
           
Set objWMIService = getObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)

Do
Set objItem = colItems.NextEvent
With objItem
    Wscript.Echo StrMessage & Now & vbcrlf & .TargetInstance.Name & vbtab & _
    .TargetInstance.CommandLine & vbtab & "PID: " & .TargetInstance.ProcessId
End with
Loop
