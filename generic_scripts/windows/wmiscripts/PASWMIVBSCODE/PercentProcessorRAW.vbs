'==========================================================================
'
'
' COMMENT: <Uses raw performance data, calculates processor utilization>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem1
Dim i, objItem2
Dim percentProcessorTime
Dim n1, n2, d1,d2
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfRawData_PerfOS_Processor.Name='_Total'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
WScript.echo "Percent processor utilization"
For i = 1 to 8
Set objItem1 = objWMIService.get(wmiQuery)
   N1 = objItem1.PercentProcessorTime
   D1 = objItem1.TimeStamp_Sys100NS
WScript.Sleep 2000
Set objItem2 = objWMIService.get(wmiQuery)
   N2 = objItem2.PercentProcessorTime
   D2 = objItem2.TimeStamp_Sys100NS
PercentProcessorTime = (1 - ((N2 - N1)/(D2-D1)))*100
   WScript.Echo Round(PercentProcessorTime,2)
Next
