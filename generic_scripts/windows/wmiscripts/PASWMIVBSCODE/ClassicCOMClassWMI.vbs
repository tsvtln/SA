Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strWhere
strComputer = "."
wmiNS = "\root\cimv2"
strWhere = funQuery("wmi")
wmiQuery = "Select * from Win32_ClassicCOMClass" & strWhere

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ComponentId: " & objItem.ComponentId
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Name: " & objItem.Name & vbcrlf
Next

Function funQuery(strwmi)
funQuery = " where caption like " & "'%" & strwmi & "%'"
End function