'=====================================================================
' This script demonstrates how to download a file from
' the web, using Microsoft.XMLHTTP to retrieve the file
' and FileSystemObject for **binary** file output.
'
'----------------------------------------------------------

'--Begin user variables--
sSource = "http://msdn.microsoft.com/scripting/art/t_scripting.jpg"
sDest = "test.jpg"
'---End user variables---

set oHTTP = WScript.CreateObject("Microsoft.XMLHTTP")
set oFSO = WScript.CreateObject("Scripting.FileSystemObject")

oHTTP.open "GET", sSource, False
oHTTP.send
body8209 = oHTTP.responseBody
set oHTTP = nothing

sOut = ""
For i = 0 to UBound(body8209)
	sOut = sOut & chrw(ascw(chr(ascb(midb(body8209,i+1,1)))))
Next

set oTS = oFSO.CreateTextFile(sDest, True)
oTS.Write sOut
oTS.Close
set oTS = Nothing
set oFSO = Nothing
WScript.Echo "Done!"
