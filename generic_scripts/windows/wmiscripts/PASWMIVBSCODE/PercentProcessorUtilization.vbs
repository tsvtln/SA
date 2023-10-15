'==========================================================================
'
' COMMENT: <Use to perform refresher queries>
'1. Creates an SWbemRefresher object
'2. uses add to add the wmi query to the refresher object
'3. calls the Refresh method for single Instance.
'==========================================================================

Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim objRefresher, objRefreshItem, i
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfFormattedData_PerfOS_Processor.name='_Total'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objRefresher = CreateObject("WbemScripting.SWbemRefresher")
Set objItem = objRefresher.Add(objWMIService,wmiQuery).object
objRefresher.Refresh

For i = 1 To 4
objRefresher.refresh
Wscript.echo "InterruptsPersec:"  & objItem.InterruptsPersec
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "PercentIdleTime:"  & objItem.PercentIdleTime
Wscript.echo "PercentInterruptTime:"  & objItem.PercentInterruptTime
Wscript.echo "PercentPrivilegedTime:"  & objItem.PercentPrivilegedTime
Wscript.echo "PercentProcessorTime:"  & objItem.PercentProcessorTime
Wscript.echo "PercentUserTime:"  & objItem.PercentUserTime & vbcrlf
WScript.sleep 3000
Next