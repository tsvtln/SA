'==========================================================================
'
' COMMENT: <Use as a WMI Template for ConnectServer method.>
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
strComputer = "acapulco"
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_ComputerSystemProduct"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objitem In colitems
wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "IdentifyingNumber: " & objItem.IdentifyingNumber
 wscript.echo "Name: " & objItem.Name
 wscript.echo "SKUNumber: " & objItem.SKUNumber
 wscript.echo "UUID: " & objItem.UUID
 wscript.echo "Vendor: " & objItem.Vendor
 wscript.echo "Version: " & objItem.Version
wscript.echo " "
Next