'==========================================================================
'
'
' COMMENT: <Uses ConnectServer method to explore Win32_NetworkProtocol.>
'1. Uses LIKE to filter out ONLY protocols that have a name like TCP/IP
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
Dim wmiClass, wmiWhere
Dim msg


strComputer = "acapulco" 'name of a remote computer
wmiNS = "\root\cimv2"
wmiClass = "win32_NetworkProtocol"
wmiWhere = " where name like '%TCP/IP%'"
wmiQuery = "Select * from " & wmiClass & wmiWhere
strUsr ="nwtraders\LondonAdmin"'Domain\Username
strPWD = "P@ssw0rd"'UserNames password

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
		strUsr, strPWD)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	With objItem
  		msg = msg & "Caption: " & .Caption & vbcrlf
      msg = msg & "ConnectionlessService: " & .ConnectionlessService& vbcrlf
      msg = msg & "Description: " & .Description& vbcrlf
      msg = msg & "GuaranteesDelivery: " & .GuaranteesDelivery& vbcrlf
      msg = msg &  "GuaranteesSequencing: " & .GuaranteesSequencing& vbcrlf
      msg = msg &  "InstallDate: " & FunTime(.InstallDate)& vbcrlf
      msg = msg &  "MaximumAddressSize: " & .MaximumAddressSize& vbcrlf
      msg = msg &  "MaximumMessageSize: " & .MaximumMessageSize& vbcrlf
      msg = msg &  "MessageOriented: " & .MessageOriented& vbcrlf
      msg = msg &  "MinimumAddressSize: " & .MinimumAddressSize& vbcrlf
      msg = msg &  "Name: " & .Name& vbcrlf
      msg = msg &  "PseudoStreamOriented: " & .PseudoStreamOriented& vbcrlf
      msg = msg &  "Status: " & .Status& vbcrlf
      msg = msg &  "SupportsBroadcasting: " & .SupportsBroadcasting& vbcrlf
      msg = msg &  "SupportsConnectData: " & .SupportsConnectData& vbcrlf
      msg = msg &  "SupportsDisconnectData: " & .SupportsDisconnectData& vbcrlf
      msg = msg &  "SupportsEncryption: " & .SupportsEncryption& vbcrlf
      msg = msg &  "SupportsExpeditedData: " & .SupportsExpeditedData& vbcrlf
      msg = msg &  "SupportsFragmentation: " & .SupportsFragmentation& vbcrlf
      msg = msg &  "SupportsGracefulClosing: " & .SupportsGracefulClosing& vbcrlf
      msg = msg &  "SupportsGuaranteedBandwidth: " & .SupportsGuaranteedBandwidth& vbcrlf
      msg = msg &  "SupportsMulticasting: " & .SupportsMulticasting& vbcrlf
      msg = msg &  "SupportsQualityofService: " & .SupportsQualityofService& vbcrlf
	End With 
Next
WScript.echo msg

Function FunTime(wmiTime)
 Dim objSWbemDateTime 'holds an swbemDateTime object. Used to translate Time
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function