'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Prints out WMI settings by using the win32_wmisetting class
'==========================================================================
Option Explicit
'on error resume next
Dim strComputer
Dim wmiNS
Dim wmiQuery
Dim objWMIService
Dim colItems, ObjItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_WMISetting"

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "ASPScriptDefaultNamespace: " & objItem.ASPScriptDefaultNamespace
 wscript.echo "ASPScriptEnabled: " & objItem.ASPScriptEnabled
 wscript.echo "AutorecoverMofs: " & vbcrlf & vbtab &  _
 	join(objItem.AutorecoverMofs, "" & vbcrlf & vbtab)
 wscript.echo "AutoStartWin9X: " & objItem.AutoStartWin9X
 wscript.echo "BackupInterval: " & objItem.BackupInterval
 wscript.echo "BackupLastTime: " & objItem.BackupLastTime
 wscript.echo "BuildVersion: " & objItem.BuildVersion
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "DatabaseDirectory: " & objItem.DatabaseDirectory
 wscript.echo "DatabaseMaxSize: " & objItem.DatabaseMaxSize
 wscript.echo "Description: " & objItem.Description
 wscript.echo "EnableAnonWin9xConnections: " & objItem.EnableAnonWin9xConnections
 wscript.echo "EnableEvents: " & objItem.EnableEvents
 wscript.echo "EnableStartupHeapPreallocation: " & objItem.EnableStartupHeapPreallocation
 wscript.echo "HighThresholdOnClientObjects: " & objItem.HighThresholdOnClientObjects
 wscript.echo "HighThresholdOnEvents: " & objItem.HighThresholdOnEvents
 wscript.echo "InstallationDirectory: " & objItem.InstallationDirectory
 wscript.echo "LastStartupHeapPreallocation: " & objItem.LastStartupHeapPreallocation
 wscript.echo "LoggingDirectory: " & objItem.LoggingDirectory
 wscript.echo "LoggingLevel: " & objItem.LoggingLevel
 wscript.echo "LowThresholdOnClientObjects: " & objItem.LowThresholdOnClientObjects
 wscript.echo "LowThresholdOnEvents: " & objItem.LowThresholdOnEvents
 wscript.echo "MaxLogFileSize: " & objItem.MaxLogFileSize
 wscript.echo "MaxWaitOnClientObjects: " & objItem.MaxWaitOnClientObjects
 wscript.echo "MaxWaitOnEvents: " & objItem.MaxWaitOnEvents
 wscript.echo "MofSelfInstallDirectory: " & objItem.MofSelfInstallDirectory
 wscript.echo "SettingID: " & objItem.SettingID
wscript.echo " "
next
