'==========================================================================
' COMMENT: <Use to perform refresher queries>
'1. Creates an SWbemRefresher object
'2. uses addEnum to add the wmi query to the refresher object
'3. calls the Refresh method
'==========================================================================

Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim objItem
Dim objRefresher, objRefreshItem, i
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objRefresher = CreateObject("WbemScripting.SWbemRefresher")
Set objRefreshItem = objRefresher.AddEnum(objWMIService,wmiQuery)
objRefresher.Refresh

For i = 1 To 4
For Each objItem in objRefreshItem.ObjectSet
objRefresher.refresh
 wscript.echo ": " & objItem.
 wscript.echo ": " & objItem.
 wscript.echo ": " & objItem.
 wscript.echo ": " & objItem.
 wscript.echo ": " & objItem.
 wscript.echo ": " & objItem.
 WScript.echo " "
WScript.sleep 2000
next
Next