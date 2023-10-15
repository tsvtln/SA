'==========================================================================
'
' COMMENT: <Uses Win32_PerfFormattedData_PerfOS_System class to get systemUptime>
'uses a function to convert from seconds to hours
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim numSeconds

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_PerfFormattedData_PerfOS_System=@"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
    numSeconds= objItem.SystemUpTime ' it is in seconds since last start
    WScript.echo "the system has been up " & convertHours(numSeconds) & " hours"
	WScript.echo "that translates to " & convertDays(numSeconds) & " days"
'### functions below ###
Function convertHours(numSeconds)
convertHours= int(numseconds/3600)  ' number of seconds in a hour
End Function

function convertDays(numseconds)
convertDays = Int(numSeconds/86400) ' number of seconds in a day
End Function