'==========================================================================
'
'
' COMMENT: <Uses to test WMI Provider functionality>
'1. Uses GetObjectText_ method to return properties and values
'2. Uses a function to Fix up the computer name for the get command
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "mred1" 'name of the target computer system. 
wmiNS = "\root\cimv2"
wmiQuery = "win32_ComputerSystem.name=" & funFix(strComputer)
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

    Wscript.Echo myFun(wmiQuery) & objItem.getObjectText_

Function myFun(input)
Dim lstr
lstr = Len(input)
myFun = input & vbcrlf & string(lstr,"=")
End Function

Function funFix(strIN) 'computer name needs single ' 
funFix = "'" & strIN & "'"
End function