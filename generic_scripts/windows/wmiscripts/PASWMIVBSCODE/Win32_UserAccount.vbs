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
wmiQuery = "Select * from Win32_UserAccount"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AccountType: " & objItem.AccountType
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Disabled: " & objItem.Disabled
 wscript.echo "Domain: " & objItem.Domain
 wscript.echo "FullName: " & objItem.FullName
 wscript.echo "InstallDate: " & objItem.InstallDate
 wscript.echo "LocalAccount: " & objItem.LocalAccount
 wscript.echo "Lockout: " & objItem.Lockout
 wscript.echo "Name: " & objItem.Name
 wscript.echo "PasswordChangeable: " & objItem.PasswordChangeable
 wscript.echo "PasswordExpires: " & objItem.PasswordExpires
 wscript.echo "PasswordRequired: " & objItem.PasswordRequired
 wscript.echo "SID: " & objItem.SID
 wscript.echo "SIDType: " & objItem.SIDType
 wscript.echo "Status: " & objItem.Status
wscript.echo " "
next
