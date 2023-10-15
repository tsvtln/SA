'==========================================================================
'
' COMMENT: Key concepts are listed below:
'1.Selects provider counters from wmi
'2.
'3. 
'==========================================================================

On Error Resume Next 
strComputer = "." 
Set objWMIService = GetObject("winmgmts:\\" & strComputer & "\root\CIMV2") 
Set colItems = objWMIService.ExecQuery( _
    "SELECT * FROM Msft_WmiProvider_Counters",,48) 
For Each objItem in colItems 

    Wscript.Echo "Msft_WmiProvider_Counters instance"
    Wscript.Echo _
        "ProviderOperation_CreateClassEnumAsync: " _
             & objItem.ProviderOperation_CreateClassEnumAsync  _
         & VBNewLine & "ProviderOperation_CreateInstanceEnumAsync: " _
             & objItem.ProviderOperation_CreateInstanceEnumAsync _
         & VBNewLine & "ProviderOperation_DeleteClassAsync: " _
             & objItem.ProviderOperation_DeleteClassAsync _
         & VBNewLine & "ProviderOperation_DeleteInstanceAsync: " _
             & objItem.ProviderOperation_DeleteInstanceAsync _
         & VBNewLine & "ProviderOperation_ExecMethodAsync: " _
             & objItem.ProviderOperation_ExecMethodAsync _
         & VBNewLine & "ProviderOperation_ExecQueryAsync: " _
             & objItem.ProviderOperation_ExecQueryAsync _
         & VBNewLine & "ProviderOperation_GetObjectAsync: " _
             & objItem.ProviderOperation_GetObjectAsync _
         & VBNewLine & "ProviderOperation_PutClassAsync: " _
             & objItem.ProviderOperation_PutClassAsync  _
         & VBNewLine & "ProviderOperation_PutInstanceAsync: " _
             & objItem.ProviderOperation_PutInstanceAsync
Next
