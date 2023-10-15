'==========================================================================
'
'
' COMMENT: <Illustrates obtaining an SWbemPrivilegeSet Object with SWbemLocator.>
'
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
Dim objWMISecurity 'holds swbemPrivilege object
strComputer = "."
wmiNS = "\root\cimv2"
'wmiQuery = "Select * from win32_"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set objWMISecurity = objWMIService.Security_.privileges	
WScript.echo "How many privileges are here? " & objWMISecurity.count
