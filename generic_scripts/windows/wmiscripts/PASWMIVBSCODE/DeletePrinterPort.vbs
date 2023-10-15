'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Uses connectServer method to connect to wmi
'2.Uses delete_ method to delete an instance
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
Const TcpPORT = "'IP_111.111.111.111'" 'IP address 
wmiQuery = "win32_TcpIpPrinterPort.name="& tcpPort
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English.
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" '(wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer,_
	wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set objItem = objWMIService.Get(wmiQuery)
objItem.Delete_
