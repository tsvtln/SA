'==========================================================================
'
'
' COMMENT: <Use raw disk performance counter>
'1. takes 8 samples and figures out average disk time
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem1, objItem2
Dim i, n1, n2, d1, d2
Dim PercentUtilization
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfRawData_PerfDisk_LogicalDisk.name='_total'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
WScript.echo "Disk Utilization"
For i = 1 to 8
Set objItem1 = objWMIService.get(wmiQuery)
   N1 = objItem1.PercentDiskTime
   D1 = objItem1.TimeStamp_Sys100NS
WScript.Sleep 2000
Set objItem2 = objWMIService.get(wmiQuery)
   N2 = objItem2.PercentDiskTime
   D2 = objItem2.TimeStamp_Sys100NS
PercentUtilization = (1 - ((N2 - N1)/(D2-D1)))*100
   WScript.Echo Round(PercentUtilization,2)
Next
