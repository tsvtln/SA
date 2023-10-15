Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
Dim objRefresher, objRefreshItem, i
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfFormattedData_PerfOS_Objects"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objRefresher = CreateObject("WbemScripting.SWbemRefresher")
Set objRefreshItem = objRefresher.AddEnum(objWMIService,wmiQuery)
objRefresher.Refresh

For i = 1 To 4
For Each objItem in objRefreshItem.ObjectSet
objRefresher.refresh
 wscript.echo "Events: " & objItem.Events
 wscript.echo "Mutexes: " & objItem.Mutexes
 wscript.echo "Processes: " & objItem.Processes
 wscript.echo "Sections: " & objItem.Sections
 wscript.echo "Semaphores: " & objItem.Semaphores
 wscript.echo "Threads: " & objItem.Threads & vbcrlf
WScript.sleep 2000
next
Next