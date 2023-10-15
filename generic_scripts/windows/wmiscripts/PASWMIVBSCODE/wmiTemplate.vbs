
Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo ": " & objItem.
    Wscript.Echo ": " & objItem.
    Wscript.Echo ": " & objItem.
    Wscript.Echo ": " & objItem.
    Wscript.Echo ": " & objItem.
    Wscript.Echo ": " & objItem.
Next