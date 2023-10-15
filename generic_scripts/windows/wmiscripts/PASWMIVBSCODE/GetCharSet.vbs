'=====================================================================
' ~~Comment~~. Displays the decimal number, ASCII character and character
' of desired Windows font in IE (allows for copy and paste).
'
'==========================================================================

Dim IE
Const Font = "Wingdings 2"
call CreateIE()
For I = 33 to 254

ie.Document.Write "<FONT FACE=" & chr(34) & "Verdana" & chr(34) &_
		  ">" & I & " - " & chr(I) & " - " & "</Font>"
ie.Document.Write "<FONT FACE=" & chr(34) & Font & chr(34) &_
		  ">" & chr(I) & "</Font><BR>"

Next

Sub CreateIE()
	On Error Resume Next
	Set IE = CreateObject("InternetExplorer.Application")
	ie.height=370
	ie.width=500
	ie.menubar=0
	ie.toolbar=0
	ie.navigate "About:Blank"
	ie.visible=1
	Do while ie.Busy
		' wait for page to load
	Loop
	ie.Document.Write "<html><Body><br>"
End Sub
