Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
dim msg
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_Directory='c:\\a'"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
With objItem
 msg = "AccessMask: " & .AccessMask
 msg = msg  & vbcrlf &  "Archive: " & .Archive
 msg = msg  & vbcrlf &  "Caption: " & .Caption
 msg = msg  & vbcrlf &  "Compressed: " & .Compressed
 msg = msg  & vbcrlf &  "CompressionMethod: " & .CompressionMethod
 msg = msg  & vbcrlf &  "CreationClassName: " & .CreationClassName
 msg = msg  & vbcrlf &  "CreationDate: " & .CreationDate
 msg = msg  & vbcrlf &  "CSCreationClassName: " & .CSCreationClassName
 msg = msg  & vbcrlf &  "CSName: " & .CSName
 msg = msg  & vbcrlf &  "Description: " & .Description
 msg = msg  & vbcrlf &  "Drive: " & .Drive
 msg = msg  & vbcrlf &  "EightDotThreeFileName: " & .EightDotThreeFileName
 msg = msg  & vbcrlf &  "Encrypted: " & .Encrypted
 msg = msg  & vbcrlf &  "EncryptionMethod: " & .EncryptionMethod
 msg = msg  & vbcrlf &  "Extension: " & .Extension
 msg = msg  & vbcrlf &  "FileName: " & .FileName
 msg = msg  & vbcrlf &  "FileSize: " & .FileSize
 msg = msg  & vbcrlf &  "FileType: " & .FileType
 msg = msg  & vbcrlf &  "FSCreationClassName: " & .FSCreationClassName
 msg = msg  & vbcrlf &  "FSName: " & .FSName
 msg = msg  & vbcrlf &  "Hidden: " & .Hidden
 msg = msg  & vbcrlf &  "InstallDate: " & .InstallDate
 msg = msg  & vbcrlf &  "InUseCount: " & .InUseCount
 msg = msg  & vbcrlf &  "LastAccessed: " & .LastAccessed
 msg = msg  & vbcrlf &  "LastModified: " & .LastModified
 msg = msg  & vbcrlf &  "Name: " & .Name
 msg = msg  & vbcrlf &  "Path: " & .Path
 msg = msg  & vbcrlf &  "Readable: " & .Readable
 msg = msg  & vbcrlf &  "Status: " & .Status
 msg = msg  & vbcrlf &  "System: " & .System
 msg = msg  & vbcrlf &  "Writeable: " & .Writeable
End With

WScript.echo msg