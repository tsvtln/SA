
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
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_PortConnector"
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
Wscript.echo "Caption:"  & objItem.Caption
'Wscript.echo "ConnectorPinout:"  & objItem.ConnectorPinout
Wscript.echo "ConnectorType:"  & join(objItem.ConnectorType, ",")
'Wscript.echo "CreationClassName:"  & objItem.CreationClassName
'Wscript.echo "Description:"  & objItem.Description
Wscript.echo "ExternalReferenceDesignator:"  & objItem.ExternalReferenceDesignator
'Wscript.echo "InstallDate:"  & objItem.InstallDate
'Wscript.echo "InternalReferenceDesignator:"  & objItem.InternalReferenceDesignator
'Wscript.echo "Manufacturer:"  & objItem.Manufacturer
'Wscript.echo "Model:"  & objItem.Model
'Wscript.echo "Name:"  & objItem.Name
'Wscript.echo "OtherIdentifyingInfo:"  & objItem.OtherIdentifyingInfo
'Wscript.echo "PartNumber:"  & objItem.PartNumber
Wscript.echo "PortType:"  & objItem.PortType
'Wscript.echo "PoweredOn:"  & objItem.PoweredOn
'Wscript.echo "SerialNumber:"  & objItem.SerialNumber
'Wscript.echo "SKU:"  & objItem.SKU
'Wscript.echo "Status:"  & objItem.Status
Wscript.echo "Tag:"  & objItem.Tag
'Wscript.echo "Version:"  & objItem.Version
WScript.echo ""
Next