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
wmiQuery = "Win32_PerfFormattedData_PerfDisk_LogicalDisk"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objRefresher = CreateObject("WbemScripting.SWbemRefresher")
Set objRefreshItem = objRefresher.AddEnum(objWMIService,wmiQuery)
objRefresher.Refresh
For i = 1 To 3
objRefresher.Refresh 
For Each objItem in objRefreshItem.ObjectSet
With objItem
 wscript.echo funLine("Name: " & .Name)
 wscript.echo "AvgDiskBytesPerRead: " & cdbl(.AvgDiskBytesPerRead)
 wscript.echo "AvgDiskBytesPerTransfer: " & cdbl(.AvgDiskBytesPerTransfer)
 wscript.echo "AvgDiskBytesPerWrite: " & .AvgDiskBytesPerWrite
 wscript.echo "AvgDiskQueueLength: " & .AvgDiskQueueLength
 wscript.echo "AvgDiskReadQueueLength: " & .AvgDiskReadQueueLength
 wscript.echo "AvgDisksecPerRead: " & .AvgDisksecPerRead
 wscript.echo "AvgDisksecPerTransfer: " & .AvgDisksecPerTransfer
 wscript.echo "AvgDisksecPerWrite: " & .AvgDisksecPerWrite
 wscript.echo "AvgDiskWriteQueueLength: " & .AvgDiskWriteQueueLength
 wscript.echo "Caption: " & .Caption
 wscript.echo "CurrentDiskQueueLength: " & .CurrentDiskQueueLength
 wscript.echo "Description: " & .Description
 wscript.echo "DiskBytesPersec: " & .DiskBytesPersec
 wscript.echo "DiskReadBytesPersec: " & .DiskReadBytesPersec
 wscript.echo "DiskReadsPersec: " & .DiskReadsPersec
 wscript.echo "DiskTransfersPersec: " & .DiskTransfersPersec
 wscript.echo "DiskWriteBytesPersec: " & .DiskWriteBytesPersec
 wscript.echo "DiskWritesPersec: " & .DiskWritesPersec
 wscript.echo "FreeMegabytes: " & .FreeMegabytes
 wscript.echo "Frequency_Object: " & .Frequency_Object
 wscript.echo "Frequency_PerfTime: " & .Frequency_PerfTime
 wscript.echo "Frequency_Sys100NS: " & .Frequency_Sys100NS
 wscript.echo "PercentDiskReadTime: " & .PercentDiskReadTime
 wscript.echo "PercentDiskTime: " & .PercentDiskTime
 wscript.echo "PercentDiskWriteTime: " & .PercentDiskWriteTime
 wscript.echo "PercentFreeSpace: " & .PercentFreeSpace
 wscript.echo "PercentIdleTime: " & .PercentIdleTime
 wscript.echo "SplitIOPerSec: " & .SplitIOPerSec
 wscript.echo "Timestamp_Object: " & .Timestamp_Object
 wscript.echo "Timestamp_PerfTime: " & .Timestamp_PerfTime
 wscript.echo "Timestamp_Sys100NS: " & .Timestamp_Sys100NS & vbcrlf
End With
WScript.sleep 2000
next
Next

'### functions below
Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End function