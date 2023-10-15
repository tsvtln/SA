'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.creates a scheduled job to run Notepad.
'==========================================================================

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_ScheduledJob"
objJob = "notepad.exe"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objitem = objWMIService.Get(wmiQuery)
errRTN = objitem.Create _
    (objJob, "********075200.000000-300", True , 32, , , JobID) 
    
If errRTN <> 0 Then 
Wscript.Echo " error: " & errRTN
Else 
WScript.echo "New Job created. " & objJob & vbcrlf & " job id: " & jobID 
End if