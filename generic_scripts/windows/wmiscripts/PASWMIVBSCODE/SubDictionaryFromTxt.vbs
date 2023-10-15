'==========================================================================
' COMMENT: Key concepts are listed below:
'1. a subroutine used to create a dictionary from a txt file.
'2. great to use for parsing resource files. 
'3. See CreateDictionaryFromTxt.vbs for example use
'4. MUST DECLARE objDictionary. 
'==========================================================================

Sub subCreateDictionary ' creates dictionary from a text file
'*** objDictionary is declared global for use inside program. ***
Dim myFile ' holds pointer to text file
Dim ObjFSO, objTextFile
Dim strNextLine ' one line of text from myFile - fm readline method
Dim items ' array created by using split command on strNextLine

myFile = "cimTypes.csv" 'modify path as needed

Set objDictionary = CreateObject("scripting.dictionary")
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objTextFile = objFSO.OpenTextFile(myFile)
	Do until objTextFile.AtEndOfStream 
	    strNextLine = objTextFile.Readline
	    items = Split(strNextLine,",")
	   objDictionary.add items(0), items(1)
	Loop
End Sub