'==========================================================================
'
'
' NAME: <BackUpEventLogCreateFileName.vbs>
' COMMENT: <Backs up event log, creates file name on fly>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer ' global variable
dim wmiNS	' global variable 
dim wmiQuery ' used in bu event log. same variable name used in sub
dim objWMIService
dim colItems ' recycled in sub .. but gets re defined after sub
dim objItem ' recycled in sub .. but gets re defined after sub
Dim errBackupLog
Dim strLogFolder
Dim strFile ' file name for backup 
Dim strLOG
Dim strMSG ' failure message for backup


strComputer = "."
wmiNS = "\root\cimv2"
strLOG = "'application'"
strMSG = " The Application event log could not be backed up."
wmiQuery = "Select * from win32_NTEventLogFile where LogFileName=" & strLOG
strLogFolder = "C:\fso\"

subCreateFileName

Set objWMIService = GetObject("winmgmts:" _
    & "{impersonationLevel=impersonate,(Backup)}!\\" & _
        strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
    errBackupLog = objItem.BackupEventLog(strLogFOlder & strFIle)
    If errBackupLog <> 0 Then        
        Wscript.Echo errBackupLog & strMSG
    Else
        objItem.ClearEventLog()
        WScript.echo "event log was backed up."
    End If
Next

Sub subCreateFileName
dim wmiQuery ' recycled variable. same name outside. 
Dim strDate ' only used in sub
Dim strName ' only used in sub

wmiQuery = "select domain from win32_computerSystem"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.execQuery(wmiQuery)

For Each objItem in colItems
 strName =  objItem.name
 strName = strName & "." & objItem.domain
Next

strDate = Replace (cstr(Date), "/", "_")
strLog = Replace (strLOG, "'", "_")
strFIle = strName & strLog & strDate & ".evt"
End sub



