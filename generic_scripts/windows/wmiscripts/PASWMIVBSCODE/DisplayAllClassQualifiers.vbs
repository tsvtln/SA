'==========================================================================
' COMMENT: <Uses qualifiers_ property of swbemObject.>
'1. gets a collection of classes
'2. uses the subClassesOf method to obtain
'3. Uses the class property of the path object to get the class name
'4. Retrieves qualifiers property
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS 'the target wmi namespace
dim objWMIService
Dim objLocator
Dim colClasses'holds collection of classes in wmiNS
Dim strClass ' individual wmi class
dim objItem
Dim a 'counters used to go through properties and qualifiers
Dim strMsg 'single output variable
Dim strTab 'conserve space. combine vbtab and vbcrlf
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
strTab = VBcrlf & vbtab
strComputer = "."
wmiNS = "\root\cimv2"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, _
	 wmiNS, strUsr, strPWD, strLocl, strAuth, iFLag)
Set colClasses = objWMIService.SubclassesOf()

For Each strClass In colClasses
Set objItem = objWMIService.get(strClass.path_.class)
strMsg= funLine(objItem.Path_.Class)

For Each a In objItem.Qualifiers_
strMsg= strMsg & strTab & a.name
Next
	WScript.echo strMsg
Next'for each strClass

'#### functions below ##### 
Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End Function
