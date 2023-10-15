'==========================================================================
'
'
' COMMENT: <Use ConnectServer method, specify remote machine and Kerberos.>
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
wmiQuery = "Select * from win32_DiskDrive"
strUsr ="londonAdmin"'Blank for current security. Domain\Username
strPWD = "P@ssw0rd"'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = "Kerberos:acapulco"'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
 wscript.echo "BytesPerSector: " & objItem.BytesPerSector
 wscript.echo "Capabilities: " & join(objItem.Capabilities)
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "DeviceID: " & objItem.DeviceID
 wscript.echo "Index: " & objItem.Index
 wscript.echo "InterfaceType: " & objItem.InterfaceType
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MediaType: " & objItem.MediaType
 wscript.echo "Model: " & objItem.Model
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Partitions: " & objItem.Partitions
 wscript.echo "PNPDeviceID: " & objItem.PNPDeviceID
 wscript.echo "SectorsPerTrack: " & objItem.SectorsPerTrack
 wscript.echo "Signature: " & objItem.Signature
 wscript.echo "Size: " & objItem.Size
 wscript.echo "Status: " & objItem.Status
 wscript.echo "SystemName: " & objItem.SystemName
 wscript.echo "TotalCylinders: " & objItem.TotalCylinders
 wscript.echo "TotalHeads: " & objItem.TotalHeads
 wscript.echo "TotalSectors: " & objItem.TotalSectors
 wscript.echo "TotalTracks: " & objItem.TotalTracks
 wscript.echo "TracksPerCylinder: " & objItem.TracksPerCylinder
 wscript.echo " "
Next