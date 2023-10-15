
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_NamedJobObjectActgInfo"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "128" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
 WScript.Echo "ActiveProcesses: " & objItem.ActiveProcesses
 WScript.Echo "Caption: " & objItem.Caption
 WScript.Echo "Description: " & objItem.Description
 WScript.Echo "Name: " & objItem.Name
 WScript.Echo "OtherOperationCount: " & formatNumber(objItem.OtherOperationCount,0,,-1)
 WScript.Echo "OtherTransferCount: " & funNum(objItem.OtherTransferCount)
 WScript.Echo "PeakJobMemoryUsed: " & funNum(objItem.PeakJobMemoryUsed)
 WScript.Echo "PeakProcessMemoryUsed: " & funNum(objItem.PeakProcessMemoryUsed)
 WScript.Echo "ReadOperationCount: " & funNum(objItem.ReadOperationCount)
 WScript.Echo "ReadTransferCount: " & funNum(objItem.ReadTransferCount)
 WScript.Echo "ThisPeriodTotalKernelTime: " & funNum(objItem.ThisPeriodTotalKernelTime)
 WScript.Echo "ThisPeriodTotalUserTime: " & funNum(objItem.ThisPeriodTotalUserTime)
 WScript.Echo "TotalKernelTime: " & funNum(objItem.TotalKernelTime)
 WScript.Echo "TotalPageFaultCount: " & funNum(objItem.TotalPageFaultCount)
 WScript.Echo "TotalProcesses: " & funNum(objItem.TotalProcesses)
 WScript.Echo "TotalTerminatedProcesses: " & funNum(objItem.TotalTerminatedProcesses)
 WScript.Echo "TotalUserTime: " & funNum(objItem.TotalUserTime)
 WScript.Echo "WriteOperationCount: " & funNum(objItem.WriteOperationCount)
 WScript.Echo "WriteTransferCount: " & funNum(objItem.WriteTransferCount)
 WScript.Echo
Next

Function funNum(num)
funNum = FormatNumber(num,0,,-1)
End function