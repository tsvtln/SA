
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
Dim strgroup, strUser, objDictionary, colItem, colkeys, i
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_ProgramGroup"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "128" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objdictionary = CreateObject("scripting.dictionary")
Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	If objdictionary.Exists(objItem.username) Then
	strGroup = strGroup & objItem.GroupName & vbcrlf & vbtab
	Else
	objDictionary.add objItem.UserName, strgroup
	strgroup = ""
	End if
Next

colItem = objDictionary.Items
colKeys = objDictionary.Keys
For i = 0 To objDictionary.Count -1
 Wscript.Echo "USER: " & colKeys(i) & vbcrlf &  vbtab & colItem(i)
next