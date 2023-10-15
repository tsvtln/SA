'==========================================================================
' COMMENT: <Kills a list of processes by reading a txt file>
'1. read a text file and kill a list of processes. Uses the FileSystemObject
'2. Uses win32_process and the terminate method
'3. When first ran it killed ISATRAY.EXE as was running in user context. 
'4. But other processes running as localSystem would give rtnCode of 2 which
'5. is access denied. But I was able to kill from TaskManager. So it is a security
'6. Issue. To make it easier I used the addAsString method to add security.
'7. 'debug privilege allows to kill process. Shutdown, loadDriver, Security did not
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strProcess
Dim strFile
Dim objFSO
Dim objFile
Dim intRTN
Dim msgOUT

strComputer = "."
strFile = "Killprocesses.txt"
wmiNS = "\root\cimv2"

Set objFSO = CreateObject("scripting.fileSystemObject")
Set objFile = objFSO.OpenTextFile(strFile)
objFile.SkipLine

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)

Do Until objFile.AtEndOfStream
strProcess = objFile.ReadLine
strProcess = "'" & strProcess & "'" 'because pass in single quote
wmiQuery = "Select name from win32_process where name = " & strProcess

Set colItems = objWMIService.ExecQuery(wmiQuery)
objWMIservice.security_.privileges.addAsString "SedebugPrivilege"
For Each objItem in colItems
    intRTN = objItem.Terminate
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
End Sub 