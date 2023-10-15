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
wmiQuery = "Select * from win32_volume where drivetype ='3'"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "Access:"  & objItem.Access
Wscript.echo "Automount:"  & objItem.Automount
Wscript.echo "Availability:"  & objItem.Availability
Wscript.echo "BlockSize:"  & objItem.BlockSize
Wscript.echo "Capacity:"  & objItem.Capacity
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "Compressed:"  & objItem.Compressed
Wscript.echo "ConfigManagerErrorCode:"  & objItem.ConfigManagerErrorCode
Wscript.echo "ConfigManagerUserConfig:"  & objItem.ConfigManagerUserConfig
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "DeviceID:"  & objItem.DeviceID
Wscript.echo "DirtyBitSet:"  & objItem.DirtyBitSet
Wscript.echo "DriveLetter:"  & objItem.DriveLetter
Wscript.echo "DriveType:"  & objItem.DriveType
Wscript.echo "ErrorCleared:"  & objItem.ErrorCleared
Wscript.echo "ErrorDescription:"  & objItem.ErrorDescription
Wscript.echo "ErrorMethodology:"  & objItem.ErrorMethodology
Wscript.echo "FileSystem:"  & objItem.FileSystem
Wscript.echo "FreeSpace:"  & objItem.FreeSpace
Wscript.echo "IndexingEnabled:"  & objItem.IndexingEnabled
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "Label:"  & objItem.Label
Wscript.echo "LastErrorCode:"  & objItem.LastErrorCode
Wscript.echo "MaximumFileNameLength:"  & objItem.MaximumFileNameLength
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "NumberOfBlocks:"  & objItem.NumberOfBlocks
Wscript.echo "PNPDeviceID:"  & objItem.PNPDeviceID
Wscript.echo "PowerManagementCapabilities:"  & objItem.PowerManagementCapabilities
Wscript.echo "PowerManagementSupported:"  & objItem.PowerManagementSupported
Wscript.echo "Purpose:"  & objItem.Purpose
Wscript.echo "QuotasEnabled:"  & objItem.QuotasEnabled
Wscript.echo "QuotasIncomplete:"  & objItem.QuotasIncomplete
Wscript.echo "QuotasRebuilding:"  & objItem.QuotasRebuilding
Wscript.echo "SerialNumber:"  & objItem.SerialNumber
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "StatusInfo:"  & objItem.StatusInfo
Wscript.echo "SupportsDiskQuotas:"  & objItem.SupportsDiskQuotas
Wscript.echo "SupportsFileBasedCompression:"  & objItem.SupportsFileBasedCompression
Wscript.echo "SystemCreationClassName:"  & objItem.SystemCreationClassName
Wscript.echo "SystemName:"  & objItem.SystemName & vbcrlf
Next