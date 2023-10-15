
strComputer = "."
objTGT = "'Win32_LocalTime'"
wmiNS = "\root\cimv2"
intHour = "11"
intMinute = "36"
intSecond = "0"
wmiQuery = "SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE " _
        & "TargetInstance ISA " & objTGT & "AND TargetInstance.Hour="&intHour _
        & "And TargetInstance.Minute = "&intMinute _
        & " And targetInstance.second="&intSecond
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecNotificationQuery(wmiQuery)
Do
   Set objItem = colItems.NextEvent
   Wscript.Echo  "Event triggered at " & now
Loop
