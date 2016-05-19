#http://stackoverflow.com/questions/28184419/pydrive-invalid-client-secrets-file

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

"""
    day folder id: 0B4D95KgQvoiRQjUwMmlvc09YZVk
"""

queryResult = None          # query result list

def GoogleDisk_GetListInFolder(folder_id):
    """
        Get the list of the folder by the specific folder id
        0 represent root
        
        Arg: folder id
        Ret: None
    """
    global queryResult
    if folder_id == 0:
        queryResult = drive.ListFile({'q': "'root' in parents"})._GetList()
    else:
        _q = {'q': "'{}' in parents and trashed=false".format(folder_id)}
        queryResult = drive.ListFile(_q).GetList()
        
def GoogleDisk_GetFolderList(folder_list):
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
    
def GoogleDisk_GetNameList(folder_id):
    """
        Get the name list of the specific folder
        
        Arg: the folder id
        Ret: the name list
    """
    _l = GetListInFolder(folder_id)
    _ll = []
    for file in _l:
        _ll.append(file['title'])
    return _ll
    
def getFolderIDByNameAndQ(name, query):
    """
        Get the folder id by name and the exist query
        
        Arg: the name of the folder, query result
        Ret: the folder id
    """
    for i in range(len(query)):
        if query[i]['title'] == name:
            return query[i]['id']
    print "didn't find the folder ( ", name, " )"
    return None
        
def CreateFolder(folderName):
    """
        Create the folder on the google drive
        
        Arg: the name of the new folder
        Ret: None
    """
    file = drive.CreateFile({'title': folderName, "mimeType": "application/vnd.google-apps.folder"})
    file.Upload()

def UploadFile(fileName, id=-1):
    """
        Upload the file by the given file name
        
        Arg: the name of the file which want to upload
        Ret: None
    """
    if not id  == -1:
        file = drive.CreateFile({"parents": [{"id": id}]})
    else:
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
    
def GetDifferWholeName(folder_id, position):
    """
        Get the different name of the list
        
        Arg: the folder id
        Ret: the name list which didn't exist in drive, the origin query
    """
    nowDirList = os.listdir(position)
    driveDirList = GetNameList(folder_id)
    res = []
    for fileOut in range(len(nowDirList)):
        exist = False
        for fileIn in range(len(driveDirList)):
            if nowDirList[fileOut] == driveDirList[fileIn]:
                exist = True
                print "drive have: ", nowDirList[fileOut]
        if exist == False:
            res.append(nowDirList[fileOut])
    return res
    
def SplitFileName(nameList, position):
    """
        Split the file name list and the folder name list
        
        Arg: the name list
        Ret: the file name list and the folder name list
    """
    folderList = next(os.walk(position))[1]
    for i in range(len(folderList)):
        nameList.remove(folderList[i])
        
    # remove the hidden file
    for i in range(len(folderList)):
        if folderList[i][:1] == '.':
            folderList.remove(folderList[i])
    for i in range(len(nameList)):
        if nameList[i][:1] == '.':
            nameList.remove(nameList[i])
    return nameList, folderList
    
    
def Update(position='./', _id=-1):
    """
        Update the contain of the folder
        
        Arg: None
        Ret: None
    """
    if position == './':
        #llist = GetDifferWholeName(0, position)
        #n, f = SplitFileName(llist, position)
        #for i in range(len(n)):
        #    UploadFile(n[i])
        pass
    else:
        llist = GetDifferWholeName(_id, position)
        n, f = SplitFileName(llist, position)
        for i in range(len(n)):
            UploadFile(n[i])
    
    # update the sub-folder
    for i in range(len(f)):
        idd = getFolderIDByNameAndQ(f[i], llist)
        Update(position + f[i] + '/', idd)
    print "update successful!"

    
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)
driveList = drive.ListFile({'q': "'root' in parents"})._GetList()
#for file in driveList:
#    print "file name: ", file['title'], ", id: ", file['id']
#print driveList
#driveList2 = GetListInFolder("0B4D95KgQvoiRfjNuZEk0NUM5M2pITHFpeXFPZkhENW9GVEtjTjRMQk5pZzNCRjY2NmZmNEk")

GoogleDisk_GetListInFolder('0B4D95KgQvoiRQjUwMmlvc09YZVk')
print GoogleDisk_GetFolderList(queryResult)

#print driveList[0]
#print driveList[0]['mimeType']
#print driveList[0]['lastViewedByMeDate']


#file1 = drive.CreateFile({'title': 'Hello.txt'})
#file1.SetContentString('Hello')
#file1.Upload() # Files.insert()

