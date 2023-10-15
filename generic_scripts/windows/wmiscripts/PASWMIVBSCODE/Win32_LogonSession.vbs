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
wmiQuery = "Select * from Win32_LogonSession"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AuthenticationPackage: " & objItem.AuthenticationPackage
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "LogonId: " & objItem.LogonId
 wscript.echo "LogonType: " & objItem.LogonType
 wscript.echo "Name: " & objItem.Name
 wscript.echo "StartTime: " & funTime(objItem.StartTime)
 wscript.echo "Status: " & objItem.Status
wscript.echo " "
Next

Function FunTime(wmiTime)
 Dim objSWbemDateTime 'holds an swbemDateTime object. Used to translate Time
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function