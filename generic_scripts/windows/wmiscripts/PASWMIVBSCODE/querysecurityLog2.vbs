
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim objWMISecurity
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_NTLogEvent where logfile = 'security'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objWMISecurity = objWMIService.security_.privileges
objWMISecurity.add(7) 'the security privilege
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
   wscript.echo "Category: " & objItem.Category
 wscript.echo "CategoryString: " & objItem.CategoryString
 wscript.echo "ComputerName: " & objItem.ComputerName
 wscript.echo "Data: " & objItem.Data
 wscript.echo "EventCode: " & objItem.EventCode
 wscript.echo "EventIdentifier: " & objItem.EventIdentifier
 wscript.echo "EventType: " & objItem.EventType
 wscript.echo "InsertionStrings: " & join(objItem.InsertionStrings, ",")
 wscript.echo "Logfile: " & objItem.Logfile
 wscript.echo "Message: " & objItem.Message
 wscript.echo "RecordNumber: " & objItem.RecordNumber
 wscript.echo "SourceName: " & objItem.SourceName
 wscript.echo "TimeGenerated: " & objItem.TimeGenerated
 wscript.echo "TimeWritten: " & objItem.TimeWritten
 wscript.echo "Type: " & objItem.Type
 wscript.echo "User: " & objItem.User
wscript.echo " "
Next