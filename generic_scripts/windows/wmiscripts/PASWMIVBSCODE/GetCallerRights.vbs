Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim errRTN
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
dim intRights
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "__SystemSecurity"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set objItem = objWMIService.get(wmiQuery)
errRTN = objItem.GetCallerAccessRights(intRights)

If errRTN = 0 then
WScript.Echo "Calling users rights: " & intRights
Else
WScript.echo "error occurred. It was: " & errRTN 
End if