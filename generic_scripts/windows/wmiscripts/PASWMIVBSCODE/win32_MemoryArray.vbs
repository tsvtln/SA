'==========================================================================
'
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
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_MemoryArray"
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
Wscript.echo "Access:"  & objItem.Access
Wscript.echo "AdditionalErrorData:"  & objItem.AdditionalErrorData
Wscript.echo "Availability:"  & objItem.Availability
Wscript.echo "BlockSize:"  & objItem.BlockSize
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "ConfigManagerErrorCode:"  & objItem.ConfigManagerErrorCode
Wscript.echo "ConfigManagerUserConfig:"  & objItem.ConfigManagerUserConfig
Wscript.echo "CorrectableError:"  & objItem.CorrectableError
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "DeviceID:"  & objItem.DeviceID
Wscript.echo "EndingAddress:"  & objItem.EndingAddress
Wscript.echo "ErrorAccess:"  & objItem.ErrorAccess
Wscript.echo "ErrorAddress:"  & objItem.ErrorAddress
Wscript.echo "ErrorCleared:"  & objItem.ErrorCleared
Wscript.echo "ErrorData:"  & objItem.ErrorData
Wscript.echo "ErrorDataOrder:"  & objItem.ErrorDataOrder
Wscript.echo "ErrorDescription:"  & objItem.ErrorDescription
Wscript.echo "ErrorGranularity:"  & objItem.ErrorGranularity
Wscript.echo "ErrorInfo:"  & objItem.ErrorInfo
Wscript.echo "ErrorMethodology:"  & objItem.ErrorMethodology
Wscript.echo "ErrorResolution:"  & objItem.ErrorResolution
Wscript.echo "ErrorTime:"  & objItem.ErrorTime
Wscript.echo "ErrorTransferSize:"  & objItem.ErrorTransferSize
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "LastErrorCode:"  & objItem.LastErrorCode
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "NumberOfBlocks:"  & objItem.NumberOfBlocks
Wscript.echo "OtherErrorDescription:"  & objItem.OtherErrorDescription
Wscript.echo "PNPDeviceID:"  & objItem.PNPDeviceID
Wscript.echo "PowerManagementCapabilities:"  & objItem.PowerManagementCapabilities
Wscript.echo "PowerManagementSupported:"  & objItem.PowerManagementSupported
Wscript.echo "Purpose:"  & objItem.Purpose
Wscript.echo "StartingAddress:"  & objItem.StartingAddress
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "StatusInfo:"  & objItem.StatusInfo
Wscript.echo "SystemCreationClassName:"  & objItem.SystemCreationClassName
Wscript.echo "SystemLevelAddress:"  & objItem.SystemLevelAddress
Wscript.echo "SystemName:"  & objItem.SystemName & vbcrlf
Next