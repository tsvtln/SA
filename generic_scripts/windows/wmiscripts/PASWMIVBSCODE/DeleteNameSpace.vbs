
Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim strNS 'holds the path to the namespace

strComputer = "."
wmiNS = "\root"
wmiQuery = "__namespace.name='myNS1'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

strNS = objItem.path_
WScript.Echo strNS
    
objWMIService.delete(strNS)

If Err.Number <> 0 Then 
WScript.Echo "Error " & Err.Number  & " occurred" & vbcrlf &_
	Err.Description & vbcrlf &_
	Err.Source
	
Else
WScript.Echo strNS & " was deleted"
End if