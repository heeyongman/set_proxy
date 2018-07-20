Function CurrentPath()
    strPath = Wscript.ScriptFullName
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    Set objFile = objFSO.GetFile(strPath)
    CurrentPath = objFSO.GetParentFolderName(objFile)
End Function

strCurrentPath = CurrentPath()

Set ws = CreateObject("wscript.shell")
ws.run strCurrentPath & "\start_brook.cmd",0