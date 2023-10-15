Option Explicit
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_NamedJobObjectActgInfo"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
With objItem
 wscript.echo "ActiveProcesses: " & .ActiveProcesses
 wscript.echo "Caption: " & .Caption
 wscript.echo "Description: " & .Description
 wscript.echo "Name: " & .Name
 wscript.echo "OtherOperationCount: " & .OtherOperationCount
 wscript.echo "OtherTransferCount: " & .OtherTransferCount
 wscript.echo "PeakJobMemoryUsed: " & .PeakJobMemoryUsed
 wscript.echo "PeakProcessMemoryUsed: " & .PeakProcessMemoryUsed
 wscript.echo "ReadOperationCount: " & .ReadOperationCount
 wscript.echo "ReadTransferCount: " & .ReadTransferCount
 wscript.echo "ThisPeriodTotalKernelTime: " & .ThisPeriodTotalKernelTime
 wscript.echo "ThisPeriodTotalUserTime: " & .ThisPeriodTotalUserTime
 wscript.echo "TotalKernelTime: " & .TotalKernelTime
 wscript.echo "TotalPageFaultCount: " & .TotalPageFaultCount
 wscript.echo "TotalProcesses: " & .TotalProcesses
 wscript.echo "TotalTerminatedProcesses: " & .TotalTerminatedProcesses
 wscript.echo "TotalUserTime: " & .TotalUserTime
 wscript.echo "WriteOperationCount: " & .WriteOperationCount
 wscript.echo "WriteTransferCount: " & .WriteTransferCount & vbcrlf
End with
next
