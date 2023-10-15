'==========================================================================
'
'
' COMMENT: <Uses ConnectServer method defaults.>
'1. uses a function to format the output from the description property as it
'2. is very long text in some places. 
'3. Breaks the wmi query into parts for ease of understanding and use
'==========================================================================

Option Explicit 
'On Error Resume Next
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim tab : tab=Space(3)
Dim strProperty, strClass, strState
strProperty = "startMode, description" 
strClass = "Win32_Service"
strState = "state = 'running' and startmode <> 'Auto'"

wmiQuery = "Select " & strProperty & " from " & strClass &_
			" where "& strState

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	With objItem
    Wscript.Echo "Name: " & .name & tab & "startMode: " & .startMode
    wscript.echo tab & .description
   	End With 
Next
