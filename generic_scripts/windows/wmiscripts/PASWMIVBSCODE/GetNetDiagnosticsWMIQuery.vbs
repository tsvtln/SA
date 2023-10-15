strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM NetDiagnostics",,48) 
For Each objItem in colItems 
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "NetDiagnostics instance"
    Wscript.Echo "-----------------------------------"
    Wscript.Echo "bIEProxy: " & objItem.bIEProxy
    Wscript.Echo "id: " & objItem.id
    Wscript.Echo "IEProxy: " & objItem.IEProxy
    Wscript.Echo "IEProxyPort: " & objItem.IEProxyPort
    Wscript.Echo "NewsNNTPPort: " & objItem.NewsNNTPPort
    Wscript.Echo "NewsServer: " & objItem.NewsServer
Next