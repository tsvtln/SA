'==========================================================================
'
' COMMENT: <Use as a WMI Template for ConnectServer method.>
'
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
Dim objLocator
dim colItems
dim objItem
Dim strUsr, strPWD, strLocl, strAuth, iFLag 'connect server parameters
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_NetworkLoginProfile where name LIKE '%londonadmin%'"
strUsr =""'Blank for current security. Domain\Username
strPWD = ""'Blank for current security.
strLocl = "MS_409" 'US English. Can leave blank for current language
strAuth = ""'if specify domain in strUsr this must be blank
iFlag = "0" 'only two values allowed here: 0 (wait for connection) 128 (wait max two min)

Set objLocator = CreateObject("WbemScripting.SWbemLocator")
Set objWMIService = objLocator.ConnectServer(strComputer, wmiNS, _
	strUsr, strPWD, strLocl, strAuth, iFLag)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
  WScript.Echo "AccountExpires: " & (objItem.AccountExpires)
  WScript.Echo "AuthorizationFlags: " & objItem.AuthorizationFlags
  WScript.Echo "BadPasswordCount: " & objItem.BadPasswordCount
  WScript.Echo "Caption: " & objItem.Caption  
  WScript.Echo "Comment: " & objItem.Comment
  WScript.Echo "Description: " & objItem.Description
  WScript.Echo "Flags: " & objItem.Flags
  WScript.Echo "FullName: " & objItem.FullName
  WScript.Echo "HomeDirectory: " & objItem.HomeDirectory
  WScript.Echo "HomeDirectoryDrive: " & objItem.HomeDirectoryDrive
  WScript.Echo "LastLogoff: " & (objItem.LastLogoff)
  WScript.Echo "LastLogon: " & funDate(objItem.LastLogon)
  WScript.Echo "LogonHours: " & objItem.LogonHours
  WScript.Echo "LogonServer: " & objItem.LogonServer
  WScript.Echo "MaximumStorage: " & objItem.MaximumStorage
  WScript.Echo "Name: " & objItem.Name
  WScript.Echo "NumberOfLogons: " & objItem.NumberOfLogons
  WScript.Echo "PasswordAge: " & (objItem.PasswordAge)
  WScript.Echo "PasswordExpires: " &(objItem.PasswordExpires)
  WScript.Echo "PrimaryGroupId: " & objItem.PrimaryGroupId
  WScript.Echo "Privileges: " & objItem.Privileges
  WScript.Echo "Profile: " & objItem.Profile
  WScript.Echo "ScriptPath: " & objItem.ScriptPath
  WScript.Echo "UnitsPerWeek: " & objItem.UnitsPerWeek
  WScript.Echo "UserComment: " & objItem.UserComment
  WScript.Echo "UserId: " & objItem.UserId
  WScript.Echo "UserType: " & objItem.UserType
  WScript.Echo "Workstations: " & objItem.Workstations
Next

Function funDate(wmiDate)
Dim objSWbemDateTime
Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
objSWbemDateTime.value = wmiDate
funDate = objSWbemDateTime.GetVarDate
End function