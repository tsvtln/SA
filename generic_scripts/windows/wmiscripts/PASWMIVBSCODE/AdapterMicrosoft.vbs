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
wmiQuery = "Select MACAddress, Manufacturer,  Name, Description from Win32_NetworkAdapter" _
	& " where manufacturer = 'Microsoft' and MACAddress is null"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "Name: " & objItem.Name
 wscript.echo " "
next
