Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "select * from win32_autoChkSetting"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.execQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "SettingID: " & objItem.SettingID
 wscript.echo "UserInputDelay: " & objItem.UserInputDelay

next
