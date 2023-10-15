

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_ntdomain"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "ClientSiteName:"  & objItem.ClientSiteName
Wscript.echo "CreationClassName:"  & objItem.CreationClassName
Wscript.echo "DcSiteName:"  & objItem.DcSiteName
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "DnsForestName:"  & objItem.DnsForestName
Wscript.echo "DomainControllerAddress:"  & objItem.DomainControllerAddress
Wscript.echo "DomainControllerAddressType:"  & objItem.DomainControllerAddressType
Wscript.echo "DomainControllerName:"  & objItem.DomainControllerName
Wscript.echo "DomainGuid:"  & objItem.DomainGuid
Wscript.echo "DomainName:"  & objItem.DomainName
Wscript.echo "DSDirectoryServiceFlag:"  & objItem.DSDirectoryServiceFlag
Wscript.echo "DSDnsControllerFlag:"  & objItem.DSDnsControllerFlag
Wscript.echo "DSDnsDomainFlag:"  & objItem.DSDnsDomainFlag
Wscript.echo "DSDnsForestFlag:"  & objItem.DSDnsForestFlag
Wscript.echo "DSGlobalCatalogFlag:"  & objItem.DSGlobalCatalogFlag
Wscript.echo "DSKerberosDistributionCenterFlag:"  & objItem.DSKerberosDistributionCenterFlag
Wscript.echo "DSPrimaryDomainControllerFlag:"  & objItem.DSPrimaryDomainControllerFlag
Wscript.echo "DSTimeServiceFlag:"  & objItem.DSTimeServiceFlag
Wscript.echo "DSWritableFlag:"  & objItem.DSWritableFlag
Wscript.echo "InstallDate:"  & objItem.InstallDate
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "NameFormat:"  & objItem.NameFormat
Wscript.echo "PrimaryOwnerContact:"  & objItem.PrimaryOwnerContact
Wscript.echo "PrimaryOwnerName:"  & objItem.PrimaryOwnerName
Wscript.echo "Roles:"  & objItem.Roles.isarray
Wscript.echo "Status:"  & objItem.Status
WScript.Echo " " 

Next