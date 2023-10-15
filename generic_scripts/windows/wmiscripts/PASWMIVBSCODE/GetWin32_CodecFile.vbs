Option Explicit
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Win32_CodecFile=""C:\\WINDOWS\\system32\\MSAUD32.ACM"""
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set objItem = objWMIService.get(wmiQuery)
With objItem
 wscript.echo "AccessMask: " & .AccessMask
 wscript.echo "Caption: " & .Caption
 wscript.echo "Compressed: " & .Compressed
 wscript.echo "CompressionMethod: " & .CompressionMethod
 wscript.echo "CreationClassName: " & .CreationClassName
 wscript.echo "CreationDate: " & .CreationDate
 wscript.echo "CSCreationClassName: " & .CSCreationClassName
 wscript.echo "CSName: " & .CSName
 wscript.echo "Description: " & .Description
 wscript.echo "Encrypted: " & .Encrypted
 wscript.echo "EncryptionMethod: " & .EncryptionMethod
 wscript.echo "Extension: " & .Extension
 wscript.echo "FileName: " & .FileName
 wscript.echo "FileSize: " & .FileSize
 wscript.echo "FileType: " & .FileType
 wscript.echo "FSCreationClassName: " & .FSCreationClassName
 wscript.echo "FSName: " & .FSName
 wscript.echo "Group: " & .Group
 wscript.echo "Hidden: " & .Hidden
 wscript.echo "InstallDate: " & .InstallDate
 wscript.echo "LastAccessed: " & .LastAccessed
 wscript.echo "LastModified: " & .LastModified
 wscript.echo "Manufacturer: " & .Manufacturer
 wscript.echo "Name: " & .Name
 wscript.echo "Path: " & .Path
 wscript.echo "System: " & .System
 wscript.echo "Version: " & .Version
 wscript.echo "Writeable: " & .Writeable
End With
