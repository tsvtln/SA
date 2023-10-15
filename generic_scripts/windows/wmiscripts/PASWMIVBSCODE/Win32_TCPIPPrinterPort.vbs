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
wmiQuery = "Select * from Win32_TCPIPPrinterPort"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "ByteCount: " & objItem.ByteCount
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "HostAddress: " & objItem.HostAddress
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PortNumber: " & objItem.PortNumber
 wscript.echo "Protocol: " & objItem.Protocol
 wscript.echo "Queue: " & objItem.Queue
 wscript.echo "SNMPCommunity: " & objItem.SNMPCommunity
 wscript.echo "SNMPDevIndex: " & objItem.SNMPDevIndex
 wscript.echo "SNMPEnabled: " & objItem.SNMPEnabled
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SystemCreationClassName: " & objItem.SystemCreationClassName
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "Type: " & objItem.Type
wscript.echo " "
next
