'==========================================================================
' COMMENT: <Use Win32_ComputerSystem to change startup delay.>
'1.As systemStartUpDelay is read/write property, do not need to spawnInstance
'2. Use Get method to connect to specific instance of the computerSystem
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
Dim objWMISecurity
strComputer = "mred" 'name of Target Computer
wmiNS = "\root\cimv2"
wmiQuery = "win32_ComputerSystem.name='" & strComputer & "'"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set objWMISecurity =objWMIService.Security_.privileges
Set objItem = objWMIService.get(wmiQuery)

WScript.echo objWMISecurity.count 'debug
objWMISecurity.addAsString("SeSystemEnvironmentPrivilege")
WScript.echo objWMISecurity.count 'debug
Set objItem = objWMIService.get(wmiQuery)
objItem.SystemStartupDelay=5
objItem.Put_

WScript.echo "SystemStartupDelay " & objItem.SystemStartupDelay