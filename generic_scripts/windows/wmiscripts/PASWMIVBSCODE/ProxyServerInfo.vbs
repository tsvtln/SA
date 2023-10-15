'==========================================================================
'
'
' COMMENT: <Uses Get Method to retrieve win32_Proxy info>
'1. Uses get method to connect to wmi and retrieve specific Proxy server info
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim strServerName
Dim errRTN

strComputer = "."
strServerName = """Mred.microsoft.com"""
wmiNS = "\root\cimv2"
wmiQuery = "win32_proxy.ServerName=" & strServerName
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
	WScript.Echo "current proxy settings on: " & strServerName
    Wscript.Echo "ProxyPortNumber: " & objItem.ProxyPortNumber
    Wscript.Echo "ProxyServer: " & objItem.ProxyServer
' now call a method to change these settings

errRTN = objItem.SetProxySetting(Null,Null)
subCheckError

Sub subCheckError
If errRTN = 0 Then
	WScript.Echo "New settings were accepted"
Else
	WScript.Echo "an error occurred. it was: " & errRTN
End If
End sub