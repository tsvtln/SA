'==========================================================================
'
'
' COMMENT: <Uses raw performance data, calculates pageFile utilization>
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
Dim percentUtilization
Dim n1, n2, d1,d2
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfRawData_PerfOS_PagingFile.Name='_Total'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
WScript.echo "Percent utilization"
For i = 1 to 8
Set objItem1 = objWMIService.get(wmiQuery)
   N1 = objItem1.PercentUsage
   D1 = objItem1.TimeStamp_Sys100NS
WScript.Sleep 2000
Set objItem2 = objWMIService.get(wmiQuery)
   N2 = objItem2.PercentUsage
   D2 = objItem2.TimeStamp_Sys100NS
PercentUtilization = (1 - ((N2 - N1)/(D2-D1)))*100
   WScript.Echo Round(PercentUtilization,2)
Next
