
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strService
Dim strFile
Dim objFSO
Dim objFile
Dim intRTN
Dim msgOUT

strComputer = "."
strFile = "Services.txt"
wmiNS = "\root\cimv2"

Set objFSO = CreateObject("scripting.fileSystemObject")
Set objFile = objFSO.OpenTextFile(strFile)
objFile.SkipLine

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)

Do Until objFile.AtEndOfStream
strService = objFile.ReadLine
strService = "'" & strService & "'" 'because pass in single quote
wmiQuery = "Select name from win32_service where name = " & strService

Set colItems = objWMIService.ExecQuery(wmiQuery)
objWMIservice.security_.privileges.addAsString "SedebugPrivilege"
For Each objItem in colItems
    intRTN = objItem.StopService
subCheckError
 'wcript.Echo objWMIservice.security_.privileges.count 'Debug
Next
Loop
WScript.Echo msgOUT

Sub subCheckError
If intRTN = 0 Then 
    msgOUT = msgOUT & objItem.name & " was terminated" & vbcrlf
    Else
    msgOUT = msgOUT & "an error occurred trying to kill " & _
     objItem.name & " it was " & intRTN & vbcrlf
    End If
End sub
