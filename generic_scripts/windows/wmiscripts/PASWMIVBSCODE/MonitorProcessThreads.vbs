'==========================================================================
'
' COMMENT: <Use to perform refresher queries>
'1. Creates an SWbemRefresher object
'2. uses addEnum to add the wmi query to the refresher object
'3. calls the Refresh method
'==========================================================================

Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim objRefresher, objRefreshItem, i
Dim strProcess
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfFormattedData_PerfProc_Thread"
strProcess = "winword"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objRefresher = CreateObject("WbemScripting.SWbemRefresher")
Set objRefreshItem = objRefresher.AddEnum(objWMIService,wmiQuery)
objRefresher.Refresh

For i = 1 To 4
For Each objItem in objRefreshItem.ObjectSet
objRefresher.refresh
If InStr (1,objItem.name,strProcess,1) then
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "ContextSwitchesPersec:"  & objItem.ContextSwitchesPersec
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "ElapsedTime:"  & objItem.ElapsedTime
Wscript.echo "IDProcess:"  & objItem.IDProcess
Wscript.echo "IDThread:"  & objItem.IDThread
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "PercentPrivilegedTime:"  & objItem.PercentPrivilegedTime
Wscript.echo "PercentProcessorTime:"  & objItem.PercentProcessorTime
Wscript.echo "PercentUserTime:"  & objItem.PercentUserTime
Wscript.echo "PriorityBase:"  & objItem.PriorityBase
Wscript.echo "PriorityCurrent:"  & objItem.PriorityCurrent
Wscript.echo "StartAddress:"  & objItem.StartAddress
Wscript.echo "ThreadState:"  & objItem.ThreadState
Wscript.echo "ThreadWaitReason:"  & objItem.ThreadWaitReason
WScript.sleep 2000
End if
next
Next