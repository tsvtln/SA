'==========================================================================
' COMMENT: <Use an associators of query to associate groups with domain>
'1. the name property is domain: nwtraders -- space is required as are """"
'==========================================================================

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
wmiQuery = "associators of {win32_ntdomain.name=""domain: nwtraders""}" _
	& " where assocClass =win32_groupInDomain"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
  With objItem
    Wscript.Echo .name
    WScript.echo vbtab & "sid type: " & .sidType & vbtab & .sid
  	If .description = "" Then ' .description may be empty, but is not null
  	else
  	WScript.echo vbtab & .description
  	End If
  End with
Next