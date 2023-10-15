'==========================================================================
'
' COMMENT: <returns useful information about Excel version information>
'1. uses the Office_ExcelVersion wmi class
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Office_ExcelVersion"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
wscript.echo "Build: " & objItem.Build
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Path: " & objItem.Path
 wscript.echo "Version: " & objItem.Version
wscript.echo " "

Next