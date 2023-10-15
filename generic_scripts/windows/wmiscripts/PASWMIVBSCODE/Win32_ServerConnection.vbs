Option Explicit
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_ServerConnection"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "ActiveTime: " & objItem.ActiveTime
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "ComputerName: " & objItem.ComputerName
 wscript.echo "ConnectionID: " & objItem.ConnectionID
 wscript.echo "Description: " & objItem.Description
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NumberOfFiles: " & objItem.NumberOfFiles
 wscript.echo "NumberOfUsers: " & objItem.NumberOfUsers
 wscript.echo "ShareName: " & objItem.ShareName
 wscript.echo "Status: " & objItem.Status
 wscript.echo "UserName: " & objItem.UserName
wscript.echo " "
next
