strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2\Applications\MicrosoftIE") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM MicrosoftIE_ConnectionSettings",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "MicrosoftIE_ConnectionSettings instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "AllowInternetPrograms: " & objItem.AllowInternetPrograms
    Wscript.Echo "AutoConfigURL: " & objItem.AutoConfigURL
    Wscript.Echo "AutoDisconnect: " & objItem.AutoDisconnect
    Wscript.Echo "AutoProxyDetectMode: " & objItem.AutoProxyDetectMode
    Wscript.Echo "Caption: " & objItem.Caption
    Wscript.Echo "DataEncryption: " & objItem.DataEncryption
    Wscript.Echo "Default: " & objItem.Default
    Wscript.Echo "DefaultGateway: " & objItem.DefaultGateway
    Wscript.Echo "Description: " & objItem.Description
    Wscript.Echo "DialUpServer: " & objItem.DialUpServer
    Wscript.Echo "DisconnectIdleTime: " & objItem.DisconnectIdleTime
    Wscript.Echo "EncryptedPassword: " & objItem.EncryptedPassword
    Wscript.Echo "IPAddress: " & objItem.IPAddress
    Wscript.Echo "IPHeaderCompression: " & objItem.IPHeaderCompression
    Wscript.Echo "Modem: " & objItem.Modem
    Wscript.Echo "Name: " & objItem.Name
    Wscript.Echo "NetworkLogon: " & objItem.NetworkLogon
    Wscript.Echo "NetworkProtocols: " & objItem.NetworkProtocols
    Wscript.Echo "PrimaryDNS: " & objItem.PrimaryDNS
    Wscript.Echo "PrimaryWINS: " & objItem.PrimaryWINS
    Wscript.Echo "Proxy: " & objItem.Proxy
    Wscript.Echo "ProxyOverride: " & objItem.ProxyOverride
    Wscript.Echo "ProxyServer: " & objItem.ProxyServer
    Wscript.Echo "RedialAttempts: " & objItem.RedialAttempts
    Wscript.Echo "RedialWait: " & objItem.RedialWait
    Wscript.Echo "ScriptFileName: " & objItem.ScriptFileName
    Wscript.Echo "SecondaryDNS: " & objItem.SecondaryDNS
    Wscript.Echo "SecondaryWINS: " & objItem.SecondaryWINS
    Wscript.Echo "ServerAssignedIPAddress: " & objItem.ServerAssignedIPAddress
    Wscript.Echo "ServerAssignedNameServer: " & objItem.ServerAssignedNameServer
    Wscript.Echo "SettingID: " & objItem.SettingID
    Wscript.Echo "SoftwareCompression: " & objItem.SoftwareCompression
Next