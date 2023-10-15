
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim errRTN
Dim strName
Dim strDisplay
Dim strPath
Dim strType
Dim intErr
Dim strStartMode
Dim bolDesk

strComputer = "Acapulco"
wmiNS = "\root\cimv2"
wmiQuery = "win32_service"
strName = "notepad"
strDisplay = "notepad"
strPath="c:\windows\System32\notepad.exe"
intErr = 0 'do not notify user if error
strStartMode = "Manual"
bolDesk = False


Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
errRTN=objItem.create(strName,strDisplay,strPath,,intErr,strStartMode,bolDesk)
WScript.Echo(errRTN)