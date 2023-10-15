'==========================================================================
'
'
' NAME: <AssociatorsOfW32SystemDriver.vbs>
'
' COMMENT: <Uses ConnectServer method to do an associators of query.>
'1. Examines the win32_SystemDriver and the win32_SystemDriverPNPEnitity assoc Class
'2. Looks at the dependent role. 
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strDriver, strMSG, strSYS
Dim intL:intL=0 'used to get length of description
strComputer = "acapulco" ' modify to your computer.
strDriver = "'sysaudio'"
wmiQuery = "associators of {Win32_SystemDriver.Name="&strDriver&"}"_
	&" where assocClass=win32_SystemDriverPNPEntity role=Dependent"

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
With objItem
	strSys = .systemName :funLen(.systemName)
	strMSG = strMSG & .service & vbcrlf :funLen(.service)
    strMSG = strMSG &  vbtab &.deviceID & vbcrlf:funLen(.deviceID)
    strMSG = strMSG & vbtab & .manufacturer & vbcrlf:funLen(.manufacturer)
    strMSG = strMSG & vbtab & .name & vbcrlf:funLen(.name)
End with
Next

WScript.echo Space(funCenter(intL)) & strSYS & vbcrlf & strMSG

'+++ Functions below +++
Function funLen(msg)
If Len(msg) > intL Then intL = Len(msg)
funLen = intL
End Function

Function funCenter(intL)'used to get space value used to center name
intL = (intL)/2 'gives 1/2 of longest line
intL = intL - (Len(strSYS)/2)'get 1/2 if sysName sub from intL
funCenter = intL
End function


