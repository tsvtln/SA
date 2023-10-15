'==========================================================================
' NAME: <AntiVirusProperties.vbs>
'
' COMMENT: <Uses the new AntiVirusProduct class from the security center namespace>
'1. Must connect to the root\securityCenter namespace
'2. Must use the AntiVirusProduct Class
'3. It is up to the AntiVirus Product company to instrument this class.
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\securityCenter"
wmiQuery = "Select * from AntiVirusProduct"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo objItem.companyName
Wscript.echo objItem.displayName
Wscript.echo objItem.enableOnAccessUIMd5Hash
Wscript.echo objItem.enableOnAccessUIParameters
Wscript.echo objItem.instanceGuid
Wscript.echo objItem.onAccessScanningEnabled
Wscript.echo objItem.pathToEnableOnAccessUI
Wscript.echo objItem.pathToUpdateUI
Wscript.echo objItem.productUptoDate
Wscript.echo objItem.updateUIMd5Hash
Wscript.echo objItem.updateUIParameters
Wscript.echo objItem.versionNumber
Next