Function CurrentPath()
    strPath = Wscript.ScriptFullName
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.GetFile(strPath)
    CurrentPath = objFSO.GetParentFolderName(objFSO.GetParentFolderName(objFile))
End Function

parCurrentPath = CurrentPath()
quo = """"
strArgs = quo & parCurrentPath & "\python27\1.0\python.exe" & quo & " " & quo & parCurrentPath & "\launcher\start_brook.py" & quo

Set ws = CreateObject("wscript.shell")
ws.run strArgs,0