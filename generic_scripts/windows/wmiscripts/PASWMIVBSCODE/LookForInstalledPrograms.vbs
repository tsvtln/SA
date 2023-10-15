'==========================================================================
'
' COMMENT: <uses win32_SoftwareElement>
'1. strProg is a variable you can use to type in exe name 
'2. If installed via MSI, will return all prog using that name
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strProg

strComputer = "."
wmiNS = "\root\cimv2"
strProg = funFix("Excel")
wmiQuery = "Select * from win32_SoftwareElement" & strProg
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo funLine("Attributes:"  & objItem.Attributes)
Wscript.echo "BuildNumber:"  & objItem.BuildNumber
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "CodeSet:"  & objItem.CodeSet
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "IdentificationCode:"  & objItem.IdentificationCode
Wscript.echo "InstallDate:"  & funTime(objItem.InstallDate)
Wscript.echo "InstallState:"  & objItem.InstallState
Wscript.echo "LanguageEdition:"  & objItem.LanguageEdition
Wscript.echo "Manufacturer:"  & objItem.Manufacturer
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "OtherTargetOS:"  & objItem.OtherTargetOS
Wscript.echo "Path:"  & objItem.Path
Wscript.echo "SerialNumber:"  & objItem.SerialNumber
Wscript.echo "SoftwareElementID:"  & objItem.SoftwareElementID
Wscript.echo "SoftwareElementState:"  & objItem.SoftwareElementState
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "TargetOperatingSystem:"  & objItem.TargetOperatingSystem
Wscript.echo "Version:"  & objItem.Version
Next

'##### functions are Below #####
Function funLine(lineOfText)
Dim numEQs, separator, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separator = separator & "="
Next
 FunLine = lineOfText & vbcrlf & separator
End Function

Function funFix(strVar) 'adds in where clause
funFix = " where path like '%" & strVar & "%'"
End Function

Function FunTime(wmiTime) 'Used to translate Time
 Dim objSWbemDateTime 'holds an swbemDateTime object. 
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value=wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function