Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim objRefresher, i
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfFormattedData_PerfProc_Process.name='wmplayer'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objRefresher = CreateObject("wbemScripting.SWbemRefresher")
Set objItem= objRefresher.Add(objWMIService,wmiQuery).object
objRefresher.Refresh
For I = 1 To 4
With objItem
objRefresher.refresh
 wscript.echo "Caption: " & .Caption
 wscript.echo "CreatingProcessID: " & .CreatingProcessID
 wscript.echo "Description: " & .Description
 wscript.echo "ElapsedTime: " & .ElapsedTime
 wscript.echo "Frequency_Object: " & .Frequency_Object
 wscript.echo "Frequency_PerfTime: " & .Frequency_PerfTime
 wscript.echo "Frequency_Sys100NS: " & .Frequency_Sys100NS
 wscript.echo "HandleCount: " & .HandleCount
 wscript.echo "IDProcess: " & .IDProcess
 wscript.echo "IODataBytesPersec: " & .IODataBytesPersec
 wscript.echo "IODataOperationsPersec: " & .IODataOperationsPersec
 wscript.echo "IOOtherBytesPersec: " & .IOOtherBytesPersec
 wscript.echo "IOOtherOperationsPersec: " & .IOOtherOperationsPersec
 wscript.echo "IOReadBytesPersec: " & .IOReadBytesPersec
 wscript.echo "IOReadOperationsPersec: " & .IOReadOperationsPersec
 wscript.echo "IOWriteBytesPersec: " & .IOWriteBytesPersec
 wscript.echo "IOWriteOperationsPersec: " & .IOWriteOperationsPersec
 wscript.echo "Name: " & .Name
 wscript.echo "PageFaultsPersec: " & .PageFaultsPersec
 wscript.echo "PageFileBytes: " & .PageFileBytes
 wscript.echo "PageFileBytesPeak: " & .PageFileBytesPeak
 wscript.echo "PercentPrivilegedTime: " & .PercentPrivilegedTime
 wscript.echo "PercentProcessorTime: " & .PercentProcessorTime
 wscript.echo "PercentUserTime: " & .PercentUserTime
 wscript.echo "PoolNonpagedBytes: " & .PoolNonpagedBytes
 wscript.echo "PoolPagedBytes: " & .PoolPagedBytes
 wscript.echo "PriorityBase: " & .PriorityBase
 wscript.echo "PrivateBytes: " & .PrivateBytes
 wscript.echo "ThreadCount: " & .ThreadCount
 wscript.echo "Timestamp_Object: " & .Timestamp_Object
 wscript.echo "Timestamp_PerfTime: " & .Timestamp_PerfTime
 wscript.echo "Timestamp_Sys100NS: " & .Timestamp_Sys100NS
 wscript.echo "VirtualBytes: " & .VirtualBytes
 wscript.echo "VirtualBytesPeak: " & .VirtualBytesPeak
 wscript.echo "WorkingSet: " & .WorkingSet
 wscript.echo "WorkingSetPeak: " & .WorkingSetPeak & vbcrlf
 WScript.Sleep 3000
End with
next
