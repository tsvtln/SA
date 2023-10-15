'==========================================================================
'
' COMMENT: <Use as a WMI Template>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer 'target computer
dim wmiNS 
dim wmiQuery, wmiQuery1
dim objWMIService
Dim objProcess
dim objProcessSU 'holds the Process Startup Object
Dim objConfig 'new Instance of ProcessSU object
Dim errRTN 'rtn code from create process
Dim procID 'process ID returned from createProcess
Dim strCommand 'Command to launch

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_ProcessStartUP"
wmiQuery1="win32_process"

strCommand = "c:\Program Files\Windows NT\Accessories\wordpad.exe" 'application we want to launch. 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objProcessSU = objWMIService.Get(wmiQuery)'create Process Startup object
Set objProcess = objWMIService.Get(WmiQuery1) 'Get win32_process class
Set objConfig = objProcessSU.SpawnInstance_ 'Create an instance of the processSU
objConfig.ShowWindow = 1 'normal window
objConfig.x = 5
objConfig.y = 5
errRTN = objProcess.Create(strCommand, Null, objConfig, procID)
WScript.echo errRTN & " " & procID
SubERR

Sub subERR
If errRTN <> 0 Then 
WScript.echo "An error occurred while launching " & strcommand &_
	vbcrlf & "the error was: " & errRTN
End If
End sub
