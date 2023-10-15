'==========================================================================
'
'
' COMMENT: <Use ConnectServer method and NTLM to get remote route table.>
'1. Gets routing table from remote machine by using NTLM authentication
'2. and using specific credentials using connect server method.
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
Const intMin = 3600'converts seconds to minutes
strComputer = "acapulco" 'A remote computer
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_IP4RouteTable"
strUsr ="LondonAdmin"'Blank for current security. Domain\Username
strPWD = "P@ssw0rd"'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = "NTLMDomain:nwtraders"'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
      WScript.Echo "Age in Minutes: " & int(objItem.Age/intMin) 
      WScript.Echo "Caption: " & objItem.Caption
      WScript.Echo "Description: " & objItem.Description
      WScript.Echo "Destination: " & objItem.Destination
      WScript.Echo "InterfaceIndex: " & objItem.InterfaceIndex
      WScript.Echo "Mask: " & objItem.Mask
      WScript.Echo "Metric1: " & objItem.Metric1
      WScript.Echo "Metric2: " & objItem.Metric2
      WScript.Echo "Metric3: " & objItem.Metric3
      WScript.Echo "Metric4: " & objItem.Metric4
      WScript.Echo "Metric5: " & objItem.Metric5
      WScript.Echo "Name: " & objItem.Name
      WScript.Echo "NextHop: " & objItem.NextHop
      WScript.Echo "Protocol: " & objItem.Protocol
      WScript.Echo "Type: " & objItem.Type
      WScript.Echo

Next