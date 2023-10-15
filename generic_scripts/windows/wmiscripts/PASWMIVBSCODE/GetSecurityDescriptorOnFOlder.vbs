'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Gets security descriptor from a folder. Translates into ACE, and SID
'2.Use GetSecurityDescriptor method from Win32_LogicalFileSecuritySetting class.
'3.From the securityDescriptor we use Win332_ACE to get Access Control Entries
'4.From the ACE object, we use win32_Trustee class to get the trusee's in the ACE
'5. Once we have the ACE, we use the SID property of the win32_Trustee class to return
'6. the SID.
'==========================================================================
Option Explicit
'On Error Resume Next
Dim strComputer ' target machine
Dim strFolder 'target folder
Dim wmiQuery 'the wmi query
Dim wmiNS 'the wmi namespace
Dim objWMIService 'connection into wmi
Dim objItem 'object returned by the wmi query
Dim errRTN 'return value from query. will indicate an error
Dim colDacl 'the discretionary access control list
Dim intACE
Dim intSID, strSID, intTrustee
Dim wmiSecurityDescriptor, i

strComputer = "."
strFolder = "'D:\\CIMv2Scripts'"
wmiQuery = "win32_LogicalFileSecuritySetting=" & strFolder
Set objWMIService = GetObject ("winmgmts:\\" & strComputer)
subGetDacl

'### subs are below ###
Sub subGetDacl
set objItem = objWMIService.Get(wmiQuery) 'use get method to get the folder
errRTN = objItem.GetSecurityDescriptor(wmiSecurityDescriptor)'Have to Assign to errRTN
subErr 'check for errors in retrieving the SID.
colDacl = wmiSecurityDescriptor.DACL ' Retrieve the DACL array of Win32_ACE objects.
For each intAce in colDacl
    wscript.echo "Access Mask: "     & strAccessMask(intAce.AccessMask)
    wscript.echo "ACE Type: "        & intAce.AceType
Set intTrustee = intAce.Trustee ' Get Win32_Trustee object from ACE object
    wscript.echo "Trustee Domain: "  & intTrustee.Domain
    wscript.echo "Trustee Name: "    & intTrustee.Name
intSID = intTrustee.SID ' Get SID as array from Trustee object
    For i = 0 To UBound(intSID) - 1
        strsid = strsid & intSID(i) & ","
    Next
    strsid = strsid & intSID(i)
    wscript.echo "Trustee SID: {"     & strsid & "}" & vbcrlf     
Next
End sub

Sub subErr
If Err <> 0 Then
    WScript.Echo "GetSecurityDescriptor failed" & VBCRLF & Err.Number & VBCRLF & Err.Description
    WScript.Quit
Else
    WScript.Echo "GetSecurityDescriptor suceeded"
End If
End Sub

Function strAccessMask(inMask)
Dim strPerm
	If inMask AND 1 Then strPerm = strPerm & "File List Dir, "
	If inMask AND 2 Then strPerm = strPerm & "File Add File, " 
	If inMask AND 4 Then strPerm = strPerm & "File Add Sub, "
	If inMask AND 8 Then strPerm = strPerm & "File Read Ext Attr, " 
	If inMask AND 16 Then strPerm = strPerm & "File Write Ext Attr, "
	If inMask AND 32 Then strPerm = strPerm & "File Traverse, "
	If inMask AND 64 Then strPerm = strPerm & "File Delete Child, "
	If inMask AND 128 Then strPerm = strPerm & "FIle Read Attrrib, "
	If inMask AND 256 Then strPerm = strPerm & "File Write Attrib, "
	If inMask AND 65536 Then strPerm = strPerm & "Delete, "
	If inMask AND 131072 Then strPerm = strPerm & "Read Control, "
	If inMask AND 262144 Then strPerm = strPerm & "Write DAC, "
	If inMask AND 524288 Then strPerm = strPerm & "Write Owner, "
	If inMask AND 1048576 Then strPerm = strPerm & "Synchronize, "
strAccessMask = strPerm
End Function



	
	
	
	

	
	
	
	
	
	
	