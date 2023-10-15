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
wmiQuery = "Select * from Win32_ScheduledJob"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Command: " & objItem.Command
 wscript.echo "DaysOfMonth: " & objItem.DaysOfMonth
 wscript.echo "DaysOfWeek: " & objItem.DaysOfWeek
 wscript.echo "Description: " & objItem.Description
 wscript.echo "ElapsedTime: " & objItem.ElapsedTime
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "InteractWithDesktop: " & objItem.InteractWithDesktop
 wscript.echo "JobId: " & objItem.JobId
 wscript.echo "JobStatus: " & objItem.JobStatus
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Notify: " & objItem.Notify
 wscript.echo "Owner: " & objItem.Owner
 wscript.echo "Priority: " & objItem.Priority
 wscript.echo "RunRepeatedly: " & objItem.RunRepeatedly
 wscript.echo "StartTime: " & objItem.StartTime
 wscript.echo "Status: " & objItem.Status
 wscript.echo "TimeSubmitted: " & objItem.TimeSubmitted
 wscript.echo "UntilTime: " & objItem.UntilTime
wscript.echo " "
next
