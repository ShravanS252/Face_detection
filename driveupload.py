from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  
upfile='saved/Unknown.jpg'
gfile = drive.CreateFile({'parents': [{'id': '1pzschX3uMbxU0lB5WZ6IlEEeAUE8MZ-t'}]})
# Read file and set it as the content of this instance.
gfile.SetContentFile(upfile)
gfile.Upload() # Upload the file.