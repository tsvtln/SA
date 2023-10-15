'==========================================================================
'
'
' COMMENT: <Use Win32_LogicakShareAccess class>
'1.Reports on shares and the accee rights associated with those shares.
'2.Translates the accessMask via a function.
'3.Uses FunLine2 function to separate the user name portion for readability
'==========================================================================

Option Explicit 
'On Error Resume Next
dim strComputer
dim wmiNS
dim wmiQuery
dim objWMIService
dim colItems
dim objItem
Dim strUser
strComputer = "."
wmiNS = "\root\cimv2"
wmiQuery = "Select * from Win32_LogicalShareAccess"
Set objWMIService = GetObject("winmgmts:\\" & strComputer & wmiNS)
Set colItems = objWMIService.ExecQuery(wmiQuery)

For Each objItem in colItems
	Wscript.Echo myFun("SecuritySetting: " & objItem.SecuritySetting)
    Wscript.Echo "AccessMask: " & funShare(objItem.AccessMask)
    WScript.Echo "Trustee" &  objItem.Trustee
    Wscript.Echo "Type: " & objItem.Type
    Wscript.Echo "Inheritance : " & objItem.Inheritance 
    Wscript.Echo "GuidObjectType: " & objItem.GuidObjectType & vbcrlf
Next

'##### Functions are below ###

Function funShare(inMask)
Dim strPerm
If inMask AND 0 Then strPerm = strPerm & "FILE_LIST_DIRECTORY, "
If inMask AND 1 Then strPerm = strPerm & "FILE_ADD_FILE, "
If inMask AND 2 Then strPerm = strPerm & "FILE_ADD_SUBDIRECTORY, "
If inMask AND 3 Then strPerm = strPerm & "FILE_READ_EA, "
If inMask AND 4 Then strPerm = strPerm & "FILE_WRITE_EA, "
If inMask AND 5 Then strPerm = strPerm & "FILE_TRAVERSE, "
If inMask AND 6 Then strPerm = strPerm & "FILE_DELETE_CHILD, "  
If inMask AND 7 Then strPerm = strPerm & "FILE_WRITE_ATTRIBUTES, "  
If inMask AND 8 Then strPerm = strPerm & "FILE_DELETE_CHILD, "  
If inMask AND 16 Then strPerm = strPerm & "DELETE, "  
If inMask AND 17 Then strPerm = strPerm & "READ_CONTROL, "  
If inMask AND 18 Then strPerm = strPerm & "WRITE_DAC, "  
If inMask AND 19 Then strPerm = strPerm & "WRITE_OWNER, "  
If inMask AND 20 Then strPerm = strPerm & "SYNCHRONIZE, " 
funShare = strPerm
End function


Function myFun(input) 'FunLine2 function
Dim lstr
lstr = Len(input)
myFun = input & vbcrlf & string(lstr,"=")
End function
