'==========================================================================
'
'
' COMMENT: <Use create method of win32_Process to create a couple of processes>
'1. Launches two processes: notepad and calc
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strProc, arrProc, proc
Dim errRTN
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_Process"
strProc = "notepad,calc"
arrProc = Split(strProc,",")
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

For Each proc in arrProc
    errRTN = objItem.create(Proc)
subError
Next


Sub subError
If errRTN <> 0 Then
WScript.Echo "An error occurred. It was: " & Err.Number & vbcrlf & Err.Description
End If
End sub