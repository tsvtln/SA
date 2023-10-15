'==========================================================================
'
'
' COMMENT: <Parses a directory of txt files. counts methods and properties>
'
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strFile, objFSO, objTxt, strLine, strFolder, objFolder, file, colFIles
Dim logFile, strMSG, objLogFIle

'strFile = "F:\BookDocs\WMIbook\Scripts\AppC\com.txt" 'text file with WMI classes in it
strFolder = "F:\BookDocs\WMIbook\Scripts\AppC"
logFile = "OSclassPropAndMethod.txt"
subReadTxt

Sub subReadTxt
Set objFSO = CreateObject("Scripting.filesystemObject")
Set objFolder = objFSO.GetFolder(strFolder)
Set colFiles = objFolder.Files
WScript.Echo "There are " & colFIles.Count & " resource files in this folder"
For Each file In colFiles
strFile = file.path
Set objTxt = objFSO.openTextFile(strFile)

strMSG = "**** " & strFile & " ******"
strMSG = funLine(strMSG) & vbcrlf
'WScript.Echo "**** " & strFile & " ******"
subLogFile
Do Until objTxt.atEndOfStream
strLine = objTxt.readline

subWMI
subLogFIle
Loop
next
End Sub

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

End Sub


Function funLine(lineOfText)
Dim numEQs, separater, i
numEQs = Len(lineOfText)
For i = 1 To numEQs
	separater = separater & "="
Next
 FunLine = lineOfText & vbcrlf & separater
End Function

Sub subError
If Err.Number <> 0 Then
WScript.Echo strLine & "not found " & Err.Number & vbcrlf & Err.Description & vbcrlf & Err.Source
Err.Clear
End If
End Sub

Sub subLogFile
Set objlogFile = objFSO.OpenTextFile(logFIle,8,True)
objlogFile.WriteLine(strMSG)
strMSG = ""
objlogFile.close
End sub
