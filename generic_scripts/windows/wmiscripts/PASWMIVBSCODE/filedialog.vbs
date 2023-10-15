
Dim obj
Dim numFiles
Dim counter

Set obj = WScript.CreateObject("Primalscript.FileDialog")
obj.HideReadOnly = vbTrue
obj.Title = "Try to open that file"
obj.InitialDir = "C:\Program Files"
obj.InitialFileName = "desktop.ini"
obj.Filter = "Chart Files (*.xlc)|*.xlc|Worksheet Files (*.xls)|*.xls|Data Files (*.xlc;*.xls)|*.xlc; *.xls|All Files (*.*)|*.*||"
obj.FilterIndex = 4
obj.ShowHelp = vbTrue
obj.AllowMultiSelect = vbTrue
obj.FileOpenDialog
numFiles = obj.NumFilesSelected

WScript.Echo "Selected Files"
WScript.Echo numFiles
For counter = 0 To numFiles - 1
	WScript.Echo obj.SelectedFiles(counter)
Next

obj.Title = "Try to save that file"
obj.FileSaveDialog