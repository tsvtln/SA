Option Explicit
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select Manufacturer, Model, UserName" _
	& " from Win32_ComputerSystem"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
wscript.echo "Manufacturer: " & objItem.Manufacturer
wscript.echo "Model: " & objItem.Model
wscript.echo "UserName: " & objItem.UserName
next
