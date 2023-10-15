Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim strMSG
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_NTEventlogFile"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)
For Each objItem in colItems

 wscript.echo "AccessMask: " & objItem.AccessMask
 wscript.echo "Archive: " & objItem.Archive
 wscript.echo "Caption: " & objItem.Caption
 wscript.echo "Compressed: " & objItem.Compressed
 wscript.echo "CompressionMethod: " & objItem.CompressionMethod
 wscript.echo "CreationClassName: " & objItem.CreationClassName
 wscript.echo "CreationDate: " & objItem.CreationDate
 wscript.echo "CSCreationClassName: " & objItem.CSCreationClassName
 wscript.echo "CSName: " & objItem.CSName
 wscript.echo "Description: " & objItem.Description
 wscript.echo "Drive: " & objItem.Drive
 wscript.echo "EightDotThreeFileName: " & objItem.EightDotThreeFileName
 wscript.echo "Encrypted: " & objItem.Encrypted
 wscript.echo "EncryptionMethod: " & objItem.EncryptionMethod
 wscript.echo "Extension: " & objItem.Extension
 wscript.echo "FileName: " & objItem.FileName
 wscript.echo "FileSize: " & objItem.FileSize
 wscript.echo "FileType: " & objItem.FileType
 wscript.echo "FSCreationClassName: " & objItem.FSCreationClassName
 wscript.echo "FSName: " & objItem.FSName
 wscript.echo "Hidden: " & objItem.Hidden
 wscript.echo "InstallDate: " & FunTime(objItem.InstallDate)
 wscript.echo "InUseCount: " & objItem.InUseCount
 wscript.echo "LastAccessed: " & FunTime(objItem.LastAccessed)
 wscript.echo "LastModified: " & FunTime(objItem.LastModified)
 wscript.echo "LogfileName: " & objItem.LogfileName
 wscript.echo "Manufacturer: " & objItem.Manufacturer
 wscript.echo "MaxFileSize: " & objItem.MaxFileSize
 wscript.echo "Name: " & objItem.Name
 wscript.echo "NumberOfRecords: " & objItem.NumberOfRecords
 wscript.echo "OverwriteOutDated: " & objItem.OverwriteOutDated
 wscript.echo "OverWritePolicy: " & objItem.OverWritePolicy
 wscript.echo "Path: " & objItem.Path
 wscript.echo "Readable: " & objItem.Readable
 wscript.echo "Sources: " & join(objItem.Sources, ",")
 wscript.echo "Status: " & objItem.Status
 wscript.echo "System: " & objItem.System
 wscript.echo "Version: " & objItem.Version
 wscript.echo "Writeable: " & objItem.Writeable & vbcrlf
Next

Function FunTime(wmiTime)
 Dim objSWbemDateTime 'holds an swbemDateTime object.
 Set objSWbemDateTime = CreateObject("WbemScripting.SWbemDateTime")
  objSWbemDateTime.Value= wmiTime
  FunTime = objSWbemDateTime.GetVarDate
End Function