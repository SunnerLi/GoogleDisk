#http://stackoverflow.com/questions/28184419/pydrive-invalid-client-secrets-file

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def GetListInFolder(folder_id):
    """
        Get the list of the folder by the specific folder id
        0 represent root
        
        Arg: folder id
        Ret: the list of the contain
    """
    if folder_id == 0:
        return drive.ListFile({'q': "'root' in parents"})._GetList()
    else:
        _q = {'q': "'{}' in parents and trashed=false".format(folder_id)}
        return drive.ListFile(_q).GetList()
        
def GetFolderList(folder_list):
    """
        Get the list of the whole folder within the given list
        
        Arg: the contain list in folder
        Ret: the list with folder only
    """
    _l = []
    for file in folder_list:
        if file['mimeType'] == "application/vnd.google-apps.folder":
            _l.append(file)
    return _l
        
def CreateFolder(folderName):
    """
        Create the folder on the google drive
        
        Arg: the name of the new folder
        Ret: None
    """
    file = drive.CreateFile({'title': folderName, "mimeType": "application/vnd.google-apps.folder"})
    file.Upload()

def UploadFile(fileName):
    """
        Upload the file by the given file name
        
        Arg: the name of the file which want to upload
        Ret: None
    """
    file = drive.CreateFile()
    file.SetContentFile(fileName)
    file.Upload()
    
def DownloadFile(fileName, folderID):
    """
        Download the file from the drive by the given file name
        
        Arg: the file name which want to download
        Ret: None
    """
    _l = GetListInFolder(folderID)
    for file in _l:
        if file['title'] == fileName:
            idd = file['id']
            break
    file = drive.CreateFile({'id': idd})
    #print('Downloading file %s from Google Drive' % file3['title']) # 'hello.png'
    file.GetContentFile(fileName)
    
def UploadFolder(folderName):
    """
    """
    pass
    
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
driveList = drive.ListFile({'q': "'root' in parents"})._GetList()
#for file in driveList:
#    print "file name: ", file['title'], ", id: ", file['id']
#print driveList
#driveList2 = GetListInFolder("0B4D95KgQvoiRfjNuZEk0NUM5M2pITHFpeXFPZkhENW9GVEtjTjRMQk5pZzNCRjY2NmZmNEk")

#DownloadFile('dog1.jpg', 0)


#print driveList[0]
#print driveList[0]['mimeType']
#print driveList[0]['lastViewedByMeDate']


#file1 = drive.CreateFile({'title': 'Hello.txt'})
#file1.SetContentString('Hello')
#file1.Upload() # Files.insert()

