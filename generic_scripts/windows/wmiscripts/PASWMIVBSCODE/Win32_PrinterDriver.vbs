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
wmiQuery = "Select * from Win32_PrinterDriver"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConfigFile: " & objItem.ConfigFile
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "DataFile: " & objItem.DataFile
 wscript.echo "DefaultDataType: " & objItem.DefaultDataType
 wscript.echo "DependentFiles: " & join(objItem.DependentFiles, ",")
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DriverPath: " & objItem.DriverPath
 wscript.echo "FilePath: " & objItem.FilePath
 wscript.echo "HelpFile: " & objItem.HelpFile
 wscript.echo "InfName: " & objItem.InfName
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "MonitorName: " & objItem.MonitorName
 wscript.echo "Name: " & objItem.Name
 wscript.echo "OEMUrl: " & objItem.OEMUrl
 wscript.echo "Started: " & objItem.Started
 wscript.echo "StartMode: " & objItem.StartMode
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SupportedPlatform: " & objItem.SupportedPlatform
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "Version: " & objItem.Version
wscript.echo " "
next
