'==========================================================================
'
' COMMENT: <Use as a WMI Template>
'1. this script will not work because Cim_MonitorResolution is not implemented.
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strFile

strComputer = "."
wmiNS = "\root\cimv2"
strFile = "'%boot.ini%'"
wmiQuery = "Select * from CIM_MonitorResolution"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "HorizontalResolution:"  & objItem.HorizontalResolution
Wscript.echo "MaxRefreshRate:"  & objItem.MaxRefreshRate
Wscript.echo "MinRefreshRate:"  & objItem.MinRefreshRate
Wscript.echo "RefreshRate:"  & objItem.RefreshRate
Wscript.echo "ScanMode:"  & objItem.ScanMode
Wscript.echo "SettingID:"  & objItem.SettingID
Wscript.echo "VerticalResolution:"  & objItem.VerticalResolution
Next