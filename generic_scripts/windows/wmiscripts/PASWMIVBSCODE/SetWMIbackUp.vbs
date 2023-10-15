
Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
dim errRTN'holds the return code from setting the property
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "win32_wmiSetting=@"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set objItem = objWMIService.get(wmiQuery)
errRTN =objItem.backupInterval = 15
objItem.put_
WScript.echo errRTN
If Err.Number <> 0 Then
WScript.echo hex(Err.Number) & vbcrlf & Err.Description &_
	vbcrlf & Err.Source
End if