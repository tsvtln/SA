'==========================================================================
'
'
' COMMENT: <Use as a WMI Template for ConnectServer method.>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_wmiSetting=@"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set objItem = objWMIService.get(wmiQuery)
With objItem
Wscript.echo "ASPScriptDefaultNamespace:"  & .ASPScriptDefaultNamespace
Wscript.echo "ASPScriptEnabled:"  & .ASPScriptEnabled
Wscript.echo "AutorecoverMofs:"  & join(.AutorecoverMofs, vbcrlf)
Wscript.echo "AutoStartWin9X:"  & .AutoStartWin9X
Wscript.echo "BackupInterval:"  & .BackupInterval
Wscript.echo "BackupLastTime:"  & FunTime(.BackupLastTime)
Wscript.echo "BuildVersion:"  & .BuildVersion
Wscript.echo "Caption:"  & .Caption
Wscript.echo "DatabaseDirectory:"  & .DatabaseDirectory
Wscript.echo "DatabaseMaxSize:"  & .DatabaseMaxSize
Wscript.echo "Description:"  & .Description
Wscript.echo "EnableAnonWin9xConnections:"  & .EnableAnonWin9xConnections
Wscript.echo "EnableEvents:"  & .EnableEvents
Wscript.echo "EnableStartupHeapPreallocation:"  & .EnableStartupHeapPreallocation
Wscript.echo "HighThresholdOnClientObjects:"  & .HighThresholdOnClientObjects
Wscript.echo "HighThresholdOnEvents:"  & .HighThresholdOnEvents
Wscript.echo "InstallationDirectory:"  & .InstallationDirectory
Wscript.echo "LastStartupHeapPreallocation:"  & .LastStartupHeapPreallocation
Wscript.echo "LoggingDirectory:"  & .LoggingDirectory
Wscript.echo "LoggingLevel:"  & .LoggingLevel
Wscript.echo "LowThresholdOnClientObjects:"  & .LowThresholdOnClientObjects
Wscript.echo "LowThresholdOnEvents:"  & .LowThresholdOnEvents
Wscript.echo "MaxLogFileSize:"  & .MaxLogFileSize
Wscript.echo "MaxWaitOnClientObjects:"  & .MaxWaitOnClientObjects
Wscript.echo "MaxWaitOnEvents:"  & .MaxWaitOnEvents
Wscript.echo "MofSelfInstallDirectory:"  & .MofSelfInstallDirectory
Wscript.echo "SettingID:"  & .SettingID
End with

'### functions below ####


Function FunTime(wmiTime)
If wmiTime <> Null Then 
 Dim objSWbemDateTime 'holds an swbemDateTime object. Used to translate Time
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End if
End Function