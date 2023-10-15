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
wmiQuery = "Select Description, SupportsGuaranteedBandwidth, SupportsQualityofService" _
	& " from Win32_NetworkProtocol where SupportsQualityofService = 'true'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Name: " & objItem.Name ' name is key value
 wscript.echo "SupportsGuaranteedBandwidth: " & objItem.SupportsGuaranteedBandwidth
 wscript.echo "SupportsQualityofService: " & objItem.SupportsQualityofService
 wscript.echo " "
next
