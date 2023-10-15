
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strValue
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_USBHub"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "Availability:"  & objItem.Availability
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "ClassCode:"  & objItem.ClassCode
Wscript.echo "ConfigManagerErrorCode:"  & objItem.ConfigManagerErrorCode
Wscript.echo "ConfigManagerUserConfig:"  & objItem.ConfigManagerUserConfig
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "CurrentAlternateSettings:"  & objItem.CurrentAlternateSettings
Wscript.echo "CurrentConfigValue:"  & objItem.CurrentConfigValue
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "DeviceID:"  & objItem.DeviceID
Wscript.echo "ErrorCleared:"  & objItem.ErrorCleared
Wscript.echo "ErrorDescription:"  & objItem.ErrorDescription
Wscript.echo "GangSwitched:"  & objItem.GangSwitched
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "LastErrorCode:"  & objItem.LastErrorCode
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "NumberOfConfigs:"  & objItem.NumberOfConfigs
Wscript.echo "NumberOfPorts:"  & objItem.NumberOfPorts
Wscript.echo "PNPDeviceID:"  & objItem.PNPDeviceID
Wscript.echo "PowerManagementCapabilities:"  & objItem.PowerManagementCapabilities
Wscript.echo "PowerManagementSupported:"  & objItem.PowerManagementSupported
Wscript.echo "ProtocolCode:"  & objItem.ProtocolCode
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "StatusInfo:"  & objItem.StatusInfo
Wscript.echo "SubclassCode:"  & objItem.SubclassCode
Wscript.echo "SystemCreationClassName:"  & objItem.SystemCreationClassName
Wscript.echo "SystemName:"  & objItem.SystemName
Wscript.echo "USBVersion:"  & objItem.USBVersion
WScript.echo ""


Next