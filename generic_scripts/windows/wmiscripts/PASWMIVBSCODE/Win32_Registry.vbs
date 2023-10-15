Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strPath
strComputer = "."
wmiNS = "\root\cimv2"
strPath = "'Microsoft Windows XP Professional|C:\WINDOWS|\Device\Harddisk0\Partition1'"
wmiQuery = "Win32_Registry.name=" & strPath
WScript.echo wmiquery
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)

 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "CurrentSize: " & objItem.CurrentSize
 wscript.echo "Description: " & objItem.Description
 wscript.echo "InstallDate: " & FunTime(objItem.InstallDate)
 wscript.echo "MaximumSize: " & objItem.MaximumSize
 wscript.echo "Name: " & objItem.Name
 wscript.echo "ProposedSize: " & objItem.ProposedSize
 wscript.echo "Status: " & objItem.Status
wscript.echo " "

Function FunTime(wmiTime)
Dim objSWbemDateTime 'holds an swbemDateTime object. Used to translate Time
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function