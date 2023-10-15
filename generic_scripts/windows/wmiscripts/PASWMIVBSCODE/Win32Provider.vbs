
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
wmiQuery = "Select * from __win32Provider"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "name: " & objItem.name
    Wscript.Echo "CLSID: " & objItem.CLSID 
     Wscript.Echo "HostingModel: " & objItem.HostingModel 
     Wscript.Echo "InitializationReentrancy: " & objItem.InitializationReentrancy &vbcrlf
Next