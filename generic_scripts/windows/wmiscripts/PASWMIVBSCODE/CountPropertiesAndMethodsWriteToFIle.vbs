'==========================================================================
'
' COMMENT: <Parses a directory of txt files. counts methods and properties>
'
'==========================================================================

Option Explicit 
On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strFile, objFSO, objTxt, strLine, strFolder, objFolder, file, colFIles
Dim logFile, strMSG, objLogFIle

strFolder = "F:\BookDocs\WMIbook\Scripts\AppD"
logFile = "PerformanceClassesPropAndMethods.txt"

subReadTxt

Sub subReadTxt
Set objFSO = CreateObject("Scripting.filesystemObject")
Set objFolder = objFSO.GetFolder(strFolder)
Set colFiles = objFolder.Files
WScript.Echo "There are " & colFIles.Count & " resource files in this folder"
For Each file In colFiles
strFile = file.path
Set objTxt = objFSO.openTextFile(strFile)
strMSG = funLine("**** "&strFile&" ******") & vbcrlf

subLogFile

Do Until objTxt.atEndOfStream
strLine = objTxt.readline

subWMI
subLogFile

Loop
next
End Sub 'subReadTxt

Sub subWMI
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = ":" & strLine
On Error Resume Next
subError
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS & wmiQuery)
subError
strMSG =  funLine(strLine) & vbcrlf
strMSG = strMSG & vbtab & "Properties: " & objWMIService.properties_.count & vbcrlf
strMSG = strMSG & vbtab & "Methods: " & objWMIService.Methods_.count & vbcrlf
End Sub 'subWMI


Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End Function 'funLine

Sub subError
If Err.Number <> 0 Then
logFile = "PerferrorLog.txt"
strMSG= strLine & "not found " & Err.Number & vbcrlf & Err.Description & _
	 vbcrlf & Err.Source & vbcrlf
Err.Clear

subLogFile

strMSG = ""
logFile = "PerformanceClassesPropAndMethods.txt"
End If
End Sub 'subError

Sub subLogFile
Const Append=8:Const Create=True
Set objlogFile = objFSO.OpenTextFile(logFIle,Append,Create)
objlogFile.WriteLine(strMSG)
strMSG = ""
objlogFile.close
End Sub 'subLogFIle
