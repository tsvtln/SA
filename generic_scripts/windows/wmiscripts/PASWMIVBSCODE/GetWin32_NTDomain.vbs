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
wmiQuery = "Win32_NTDomain='Domain: nwtraders'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
With objItem
 wscript.echo "Caption: " & .Caption
 wscript.echo "ClientSiteName: " & .ClientSiteName
 wscript.echo "CreationClassName: " & .CreationClassName
 wscript.echo "DcSiteName: " & .DcSiteName
 wscript.echo "Description: " & .Description
 wscript.echo "DnsForestName: " & .DnsForestName
 wscript.echo "DomainControllerAddress: " & .DomainControllerAddress
 wscript.echo "DomainControllerAddressType: " & .DomainControllerAddressType
 wscript.echo "DomainControllerName: " & .DomainControllerName
 wscript.echo "DomainGuid: " & .DomainGuid
 wscript.echo "DomainName: " & .DomainName
 wscript.echo "DSDirectoryServiceFlag: " & .DSDirectoryServiceFlag
 wscript.echo "DSDnsControllerFlag: " & .DSDnsControllerFlag
 wscript.echo "DSDnsDomainFlag: " & .DSDnsDomainFlag
 wscript.echo "DSDnsForestFlag: " & .DSDnsForestFlag
 wscript.echo "DSGlobalCatalogFlag: " & .DSGlobalCatalogFlag
 wscript.echo "DSKerberosDistributionCenterFlag: " & .DSKerberosDistributionCenterFlag
 wscript.echo "DSPrimaryDomainControllerFlag: " & .DSPrimaryDomainControllerFlag
 wscript.echo "DSTimeServiceFlag: " & .DSTimeServiceFlag
 wscript.echo "DSWritableFlag: " & .DSWritableFlag
 wscript.echo "InstallDate: " & .InstallDate
 wscript.echo "Name: " & .Name
 wscript.echo "NameFormat: " & .NameFormat
 wscript.echo "PrimaryOwnerContact: " & .PrimaryOwnerContact
 wscript.echo "PrimaryOwnerName: " & .PrimaryOwnerName
 wscript.echo "Roles: " & .Roles
 wscript.echo "Status: " & .Status
End with

