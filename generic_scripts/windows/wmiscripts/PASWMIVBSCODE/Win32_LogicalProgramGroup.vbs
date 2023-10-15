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
wmiQuery = "Select * from Win32_LogicalProgramGroup " _
	& "where username = 'All Users'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "GroupName: " & objItem.GroupName
 wscript.echo "InstallDate: " & funTime(objItem.InstallDate)
 wscript.echo "Name: " & objItem.Name
 wscript.echo "Status: " & objItem.Status
 wscript.echo "UserName: " & objItem.UserName & vbcrlf
Next

Function FunTime(wmiTime)
 Dim objSWbemDateTime 'holds an swbemDateTime object. 
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function