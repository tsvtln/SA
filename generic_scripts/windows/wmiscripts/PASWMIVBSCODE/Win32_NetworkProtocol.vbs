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
wmiQuery = "Select * from Win32_NetworkProtocol"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ConnectionlessService: " & objItem.ConnectionlessService
 wscript.echo "Description: " & objItem.Description
 wscript.echo "GuaranteesDelivery: " & objItem.GuaranteesDelivery
 wscript.echo "GuaranteesSequencing: " & objItem.GuaranteesSequencing
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "MaximumAddressSize: " & objItem.MaximumAddressSize
 wscript.echo "MaximumMessageSize: " & objItem.MaximumMessageSize
 wscript.echo "MessageOriented: " & objItem.MessageOriented
 wscript.echo "MinimumAddressSize: " & objItem.MinimumAddressSize
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PseudoStreamOriented: " & objItem.PseudoStreamOriented
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SupportsBroadcasting: " & objItem.SupportsBroadcasting
 wscript.echo "SupportsConnectData: " & objItem.SupportsConnectData
 wscript.echo "SupportsDisconnectData: " & objItem.SupportsDisconnectData
 wscript.echo "SupportsEncryption: " & objItem.SupportsEncryption
 wscript.echo "SupportsExpeditedData: " & objItem.SupportsExpeditedData
 wscript.echo "SupportsFragmentation: " & objItem.SupportsFragmentation
 wscript.echo "SupportsGracefulClosing: " & objItem.SupportsGracefulClosing
 wscript.echo "SupportsGuaranteedBandwidth: " & objItem.SupportsGuaranteedBandwidth
 wscript.echo "SupportsMulticasting: " & objItem.SupportsMulticasting
 wscript.echo "SupportsQualityofService: " & objItem.SupportsQualityofService
wscript.echo " "
next
