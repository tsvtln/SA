Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_PrintJob"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "DataType: " & objItem.DataType
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Document: " & objItem.Document
 wscript.echo "DriverName: " & objItem.DriverName
 wscript.echo "ElapsedTime: " & objItem.ElapsedTime
 wscript.echo "HostPrintQueue: " & objItem.HostPrintQueue
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "JobId: " & objItem.JobId
 wscript.echo "JobStatus: " & objItem.JobStatus
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Notify: " & objItem.Notify
 wscript.echo "Owner: " & objItem.Owner
 wscript.echo "PagesPrinted: " & objItem.PagesPrinted
 wscript.echo "Parameters: " & objItem.Parameters
 wscript.echo "PrintProcessor: " & objItem.PrintProcessor
 wscript.echo "Priority: " & objItem.Priority
 wscript.echo "Size: " & objItem.Size
 wscript.echo "StartTime: " & objItem.StartTime
 wscript.echo "Status: " & objItem.Status
 wscript.echo "StatusMask: " & objItem.StatusMask
 wscript.echo "TimeSubmitted: " & objItem.TimeSubmitted
 wscript.echo "TotalPages: " & objItem.TotalPages
 wscript.echo "UntilTime: " & objItem.UntilTime
wscript.echo " "
next
