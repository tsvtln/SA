'==========================================================================
'
'
' COMMENT: <Uses the new FireWallProduct class from the security center namespace>
'1. Must connect to the root\securityCenter namespace
'2. Must use the FireWallProduct Class
'3. It is up to the firewall product company to instrument this class.
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
wmiQuery = "Select * from FirewallProduct"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
wscript.echo objItem.companyName
wscript.echo objItem.displayName
wscript.echo  objItem.enabled
wscript.echo objItem.enableUIMd5Hash
wscript.echo  objItem.enableUIParameters
wscript.echo objItem.instanceGuid
wscript.echo objItem.pathToEnableUI
wscript.echo objItem.versionNumber
Next