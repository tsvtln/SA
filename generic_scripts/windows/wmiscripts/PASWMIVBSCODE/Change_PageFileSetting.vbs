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
wmiQuery = "Win32_PageFileSetting='c:\pagefile.sys'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "InitialSize: " & objItem.InitialSize
 wscript.echo "MaximumSize: " & objItem.MaximumSize
 wscript.echo "Name: " & objItem.Name
 wscript.echo "SettingID: " & objItem.SettingID

WScript.Echo "lets change the initial size"
objItem.initialSize = 19
objItem.put_
WScript.Echo "the new size is now: " & objItem.initialsize