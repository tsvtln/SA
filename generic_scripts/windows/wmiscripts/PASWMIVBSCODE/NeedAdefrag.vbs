
Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery, wmiquery1
dim objWMIService
dim colItems, colitems1
dim objItem, objitem1
dim defrag, defragNeeded

strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from win32_Volume where DriveType ='3'"

Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
    Wscript.Echo "Beginning analysis of: " & objItem.DriveLetter 
objItem.DefragAnalysis defrag,objitem1 'two output parameters must be specified
   																		 'what is returned in 2nd parameter is a
   																		 'Win32_DefragAnalysis class
     subEvalDefrag   
Next

Sub subEvalDefrag
If defrag = 0 then
 WScript.echo "this disk does not need defragmentation"
  Else
    WScript.echo defrag
End if
 
    Wscript.Echo "AverageFileSize: " & objitem1.AverageFileSize
    Wscript.Echo "FilePercentFragmentation: " & objitem1.FilePercentFragmentation 
    Wscript.Echo "FragmentedFolders: " & objitem1.FragmentedFolders 
    Wscript.Echo "TotalExcessFragments: " & objitem1.TotalExcessFragments 
    Wscript.Echo "MFTPercentInUse: " & objitem1.MFTPercentInUse 
    Wscript.Echo "TotalPageFileFragments: " & objitem1.TotalPageFileFragments 
End Sub 