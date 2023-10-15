'==========================================================================
' NAME: <AddPrinterPort.vbs>
' COMMENT: <Use ConnectServer method. Add security privilege>
'1. To use add method to add security privilege, must define own constant
'2. To add a printer port, must first spawn an instance of Class
'3. Modify properties desired, then use put method to write it to wmi.
'==========================================================================
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim objWMISecurity
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_TcpIpPrinterPort"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English.
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" '(wait for connection) 128 (wait max two min)
Const LoadDriver = 9 '9 is equal to SeLoadDriverPrivilege
Const TcpPORT = "111.111.111.111" 'IP address 

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer,_
	wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set objWMISecurity =objWMIService.Security_.privileges
WScript.echo objWMISecurity.count 'debug
objWMISecurity.add(LoadDriver)
WScript.echo objWMISecurity.count 'debug
Set objItem = objWMIService.Get(wmiQuery).SpawnInstance_
objItem.Name = "IP_"& TcpPORT
objItem.Protocol = 1 '1 is raw, 2 is lpr
objItem.HostAddress = TcpPORT
objItem.PortNumber = "9100" 'default 
objItem.SNMPEnabled = False
objItem.Put_
