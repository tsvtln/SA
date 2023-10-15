
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
Dim strVar
strComputer = "."
wmiNS = "\root\cimv2"
strVar = funFix("word") 'the product looked for
wmiQuery = "Select * from win32_SoftwareFeature" & strVar
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
Wscript.echo funLine("Accesses:"  & objItem.Accesses)
Wscript.echo "Attributes:"  & objItem.Attributes
Wscript.echo "Caption:"  & objItem.Caption
Wscript.echo "Description:"  & objItem.Description
Wscript.echo "IdentifyingNumber:"  & objItem.IdentifyingNumber
Wscript.echo "InstallDate:"  & funTime(objItem.InstallDate)
Wscript.echo "InstallState:"  & objItem.InstallState
Wscript.echo "LastUse:"  & funTime(objItem.LastUse)
Wscript.echo "Name:"  & objItem.Name
Wscript.echo "ProductName:"  & objItem.ProductName
Wscript.echo "Status:"  & objItem.Status
Wscript.echo "Vendor:"  & objItem.Vendor
Wscript.echo "Version:"  & objItem.Version
Next

'### functions below ###

Function FunTime(wmiTime)
If wmiTime <> Null then
 Dim objSWbemDateTime 'holds an swbemDateTime object. Used to translate Time
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End if
End Function

Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End Function

Function funFix(strVar) 'adds in where clause
funFix = " where description like '%" & strVar & "%'"
End Function
