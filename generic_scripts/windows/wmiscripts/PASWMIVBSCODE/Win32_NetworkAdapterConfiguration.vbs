Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strWhere
strComputer = "."
wmiNS = "\root\cimv2"
strWhere = "caption like '%intel%'" 'the name of your enet or wireless card
wmiQuery = "Select * from Win32_NetworkAdapterConfiguration where " & strWhere
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems:With objItem
 wscript.echo funLine("Caption: " & .Caption)
 wscript.echo "ArpAlwaysSourceRoute: " & .ArpAlwaysSourceRoute
 wscript.echo "ArpUseEtherSNAP: " & .ArpUseEtherSNAP
 wscript.echo "DatabasePath: " & .DatabasePath
 wscript.echo "DeadGWDetectEnabled: " & .DeadGWDetectEnabled
 If not isNull(.DefaultIPGateway) then
 wscript.echo "DefaultIPGateway: " & join(.DefaultIPGateway, ",")
 End if
 wscript.echo "DefaultTOS: " & .DefaultTOS
 wscript.echo "DefaultTTL: " & .DefaultTTL
 wscript.echo "Description: " & .Description
 wscript.echo "DHCPEnabled: " & .DHCPEnabled
 wscript.echo "DHCPLeaseExpires: " & .DHCPLeaseExpires
 wscript.echo "DHCPLeaseObtained: " & .DHCPLeaseObtained
 wscript.echo "DHCPServer: " & .DHCPServer
 wscript.echo "DNSDomain: " & .DNSDomain
 wscript.echo "DNSDomainSuffixSearchOrder: " & .DNSDomainSuffixSearchOrder
 wscript.echo "DNSEnabledForWINSResolution: " & .DNSEnabledForWINSResolution
 wscript.echo "DNSHostName: " & .DNSHostName
 If Not IsNull(.DNSServerSearchOrder) then
 wscript.echo "DNSServerSearchOrder: " & join(.DNSServerSearchOrder, ",")
 End if
 wscript.echo "DomainDNSRegistrationEnabled: " & .DomainDNSRegistrationEnabled
 wscript.echo "ForwardBufferMemory: " & .ForwardBufferMemory
 wscript.echo "FullDNSRegistrationEnabled: " & .FullDNSRegistrationEnabled
 If Not IsNull(.GatewayCostMetric) then
 wscript.echo "GatewayCostMetric: " & join(.GatewayCostMetric, ",")
 End if
 wscript.echo "IGMPLevel: " & .IGMPLevel
 wscript.echo "Index: " & .Index
 If Not IsNull(.IPAddress) then
 wscript.echo "IPAddress: " & join(.IPAddress, ",")
 End if
 wscript.echo "IPConnectionMetric: " & .IPConnectionMetric
 wscript.echo "IPEnabled: " & .IPEnabled
 wscript.echo "IPFilterSecurityEnabled: " & .IPFilterSecurityEnabled
 wscript.echo "IPPortSecurityEnabled: " & .IPPortSecurityEnabled
 If Not IsNull(.IPSecPermitIPProtocols) then
 wscript.echo "IPSecPermitIPProtocols: " & join(.IPSecPermitIPProtocols, ",")
 End If
 If Not IsNull(.IPSecPermitTCPPorts) then
 wscript.echo "IPSecPermitTCPPorts: " & join(.IPSecPermitTCPPorts, ",")
 End If
 If Not IsNull(.IPSecPermitUDPPorts) then
 wscript.echo "IPSecPermitUDPPorts: " & join(.IPSecPermitUDPPorts, ",")
 End If
 If Not IsNull(.IPSubnet) then
 wscript.echo "IPSubnet: " & join(.IPSubnet, ",")
 End if
 wscript.echo "IPUseZeroBroadcast: " & .IPUseZeroBroadcast
 wscript.echo "IPXAddress: " & .IPXAddress
 wscript.echo "IPXEnabled: " & .IPXEnabled
 wscript.echo "IPXFrameType: " & .IPXFrameType
 wscript.echo "IPXMediaType: " & .IPXMediaType
 wscript.echo "IPXNetworkNumber: " & .IPXNetworkNumber
 wscript.echo "IPXVirtualNetNumber: " & .IPXVirtualNetNumber
 wscript.echo "KeepAliveInterval: " & .KeepAliveInterval
 wscript.echo "KeepAliveTime: " & .KeepAliveTime
 wscript.echo "MACAddress: " & .MACAddress
 wscript.echo "MTU: " & .MTU
 wscript.echo "NumForwardPackets: " & .NumForwardPackets
 wscript.echo "PMTUBHDetectEnabled: " & .PMTUBHDetectEnabled
 wscript.echo "PMTUDiscoveryEnabled: " & .PMTUDiscoveryEnabled
 wscript.echo "ServiceName: " & .ServiceName
 wscript.echo "SettingID: " & .SettingID
 wscript.echo "TcpipNetbiosOptions: " & .TcpipNetbiosOptions
 wscript.echo "TcpMaxConnectRetransmissions: " & .TcpMaxConnectRetransmissions
 wscript.echo "TcpMaxDataRetransmissions: " & .TcpMaxDataRetransmissions
 wscript.echo "TcpNumConnections: " & .TcpNumConnections
 wscript.echo "TcpUseRFC1122UrgentPointer: " & .TcpUseRFC1122UrgentPointer
 wscript.echo "TcpWindowSize: " & .TcpWindowSize
 wscript.echo "WINSEnableLMHostsLookup: " & .WINSEnableLMHostsLookup
 wscript.echo "WINSHostLookupFile: " & .WINSHostLookupFile
 wscript.echo "WINSPrimaryServer: " & .WINSPrimaryServer
 wscript.echo "WINSScopeID: " & .WINSScopeID
 wscript.echo "WINSSecondaryServer: " & .WINSSecondaryServer & vbcrlf
end with:Next

'### functions below####
Function funLine(lineOfText)
Dim numEQs, separator, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separator = separator & "="
Next
 FunLine = lineOfText & vbcrlf & separator
End function