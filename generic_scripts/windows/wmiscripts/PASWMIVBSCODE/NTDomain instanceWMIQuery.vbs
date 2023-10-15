strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Win32_NTDomain",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Win32_NTDomain instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "ClientSiteName: " & objItem.ClientSiteName
    Wscript.Echo "CreationClassName: " & objItem.CreationClassName
    Wscript.Echo "DcSiteName: " & objItem.DcSiteName
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "DnsForestName: " & objItem.DnsForestName
    Wscript.Echo "DomainControllerAddress: " & objItem.DomainControllerAddress
    Wscript.Echo "DomainControllerAddressType: " & objItem.DomainControllerAddressType
    Wscript.Echo "DomainControllerName: " & objItem.DomainControllerName
    Wscript.Echo "DomainGuid: " & objItem.DomainGuid
    Wscript.Echo "DomainName: " & objItem.DomainName
    Wscript.Echo "DSDirectoryServiceFlag: " & objItem.DSDirectoryServiceFlag
    Wscript.Echo "DSDnsControllerFlag: " & objItem.DSDnsControllerFlag
    Wscript.Echo "DSDnsDomainFlag: " & objItem.DSDnsDomainFlag
    Wscript.Echo "DSDnsForestFlag: " & objItem.DSDnsForestFlag
    Wscript.Echo "DSGlobalCatalogFlag: " & objItem.DSGlobalCatalogFlag
    Wscript.Echo "DSKerberosDistributionCenterFlag: " & objItem.DSKerberosDistributionCenterFlag
    Wscript.Echo "DSPrimaryDomainControllerFlag: " & objItem.DSPrimaryDomainControllerFlag
    Wscript.Echo "DSTimeServiceFlag: " & objItem.DSTimeServiceFlag
    Wscript.Echo "DSWritableFlag: " & objItem.DSWritableFlag
    Wscript.Echo "InstallDate: " & objItem.InstallDate
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "NameFormat: " & objItem.NameFormat
    Wscript.Echo "PrimaryOwnerContact: " & objItem.PrimaryOwnerContact
    Wscript.Echo "PrimaryOwnerName: " & objItem.PrimaryOwnerName
    If isNull(objItem.Roles) Then
        Wscript.Echo "Roles: "
    Else
        Wscript.Echo "Roles: " & Join(objItem.Roles, ",")
    End If
    Wscript.Echo "Status: " & objItem.Status
Next