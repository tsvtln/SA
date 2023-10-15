'==========================================================================
'
' COMMENT: <Lists Processes by name, writes to txt file on desktop>
'1. interesting thing is the use of the desktop as place to hold txt file. 
'2. Also adds all output to single variable to ease writing to output. 
'3. Since special folder is used, do not need to see if the folder exists.
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strFolder
Dim message
Dim i

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select name, ExecutablePath from win32_process"
i = 0
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
   message = message & vbcrlf &  objItem.name & vbtab & objItem.ExecutablePath
   i = i+1 ' counts the number of processes that are running. 
 Next

SubSpecialFolder
SubLogFile

' subs are below
Sub SubSpecialFolder
Dim objShell
Set objShell = CreateObject ("wscript.shell")
strFolder = objshell.SpecialFolders("Desktop")
End Sub


Sub SubLogFile
Dim objFSO			' holds connection to file system object			
Dim objFile			' holds hook to the file to be used
Dim LogFile
Dim m1 ' holds message 1
m1 = "there are " & i & " processes running "
Const ForWriting = 2
Const ForAppending = 8
LogFile = strFolder & "\logFile.txt"

Set objFSO = CreateObject("Scripting.FileSystemObject")

	If objFSO.FileExists(LogFile) Then
		Set objFile = objFSO.OpenTextFile(LogFile, ForAppending)
		objFile.WriteBlankLines(1)
		objFile.Writeline " ** " & m1 & Now & message
	    objFile.Close
	Else
		Set objFile = objFSO.CreateTextFile(LogFile)
		objfile.writeline " ** " & m1 & Now & message
	    objFile.Close
	End If

End sub