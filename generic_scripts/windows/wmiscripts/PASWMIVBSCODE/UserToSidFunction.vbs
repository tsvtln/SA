'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Function translates user name to a SID
'==========================================================================

Option Explicit 
'On Error Resume Next


WScript.Echo funUserSid("'edwils'")'demo Purposes

Function funUserSid(strName)
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "select sid from win32_userAccount where name=" & strName 'name is key
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.execQuery(wmiQuery)

For Each objItem in colItems
    funUserSid= objItem.sid
Next
End function