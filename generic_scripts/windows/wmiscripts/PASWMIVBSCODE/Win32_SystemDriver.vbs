Option Explicit
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strWhere
strComputer = "."
wmiNS = "\root\cimv2"
strWhere =funfix(InputBox("what driver are you looking for"))
wmiQuery = "Select * from Win32_SystemDriver" & strWhere
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AcceptPause: " & objItem.AcceptPause
 wscript.echo "AcceptStop: " & objItem.AcceptStop
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DesktopInteract: " & objItem.DesktopInteract
 wscript.echo "DisplayName: " & objItem.DisplayName
 wscript.echo "ErrorControl: " & objItem.ErrorControl
 wscript.echo "ExitCode: " & objItem.ExitCode
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PathName: " & objItem.PathName
 wscript.echo "ServiceSpecificExitCode: " & objItem.ServiceSpecificExitCode
 wscript.echo "ServiceType: " & objItem.ServiceType
 wscript.echo "Started: " & objItem.Started
 wscript.echo "StartMode: " & objItem.StartMode
 wscript.echo "StartName: " & objItem.StartName
 wscript.echo "State: " & objItem.State
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TagId: " & objItem.TagId & vbcrlf
Next

Function funFix (strWhere)
funFix = " where name like '%" & strWhere & "%'"
End function