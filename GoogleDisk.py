# coding=utf-8

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

class GoogleDisk(object):
    NONE = -1                   # constant represent none in google disk
    queryResult = None          # query result list
    drive = None                # google drive object

    def __init__(self):
        """
            Create the google disk instance
        """
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        self.drive = GoogleDrive(gauth)
        
    def getContainList(self, folder_id):
        """
        Get the list of the folder by the specific folder id
        0 represent root
        
        Arg: folder id
        Ret: contain list
        """
        global queryResult
        if folder_id == 0:
            self.queryResult = self.drive.ListFile({'q': "'root' in parents"})._GetList()
        else:
            _q = {'q': "'{}' in parents and trashed=false".format(folder_id)}
            self.queryResult = self.drive.ListFile(_q).GetList()
        return self.queryResult
        
    def getFolder(self, folder_list=None, id=NONE):
        """
            Get the list of the whole folder
        
            Arg: the JSON list
            Ret: the list with folder only
            
            Usage: ....
                   print disk.getFolder(id=0, folder_list='LIST')
                   ....
        """
        _l = []
        if folder_list == None:
            if id == self.NONE:
                if self.queryResult == None:
                    print "Please Check if you have submit query?"
                else:
                    origin = self.queryResult
            else:
                origin = self.getContainList(id)
        else:
            origin = folder_list
        for file in origin:
            if file['mimeType'] == "application/vnd.google-apps.folder":
                _l.append(file)
        return _l
    
    def getName(self, procList):
        """
            Get the name list from the JSON query
        
            Arg: the waiting process JSON
            Ret: the name list
        """
        if len(procList) > 0 and procList[0]['title'] == None:
            print "Invalid JSON input"
        res = []
        for file in procList:
            res.append(file['title'])
        return res
        
    def getID(self, name, query=NONE):
        """
            Get the file id
        
            Arg: the name of the file, query result
            Ret: the folder id
            
            Usage: ....
                   print disk.getID(query=_q, name="NAME")
                   ....
        """
        if query == self.NONE:
            if self.queryResult == None:
                print "Empty Query, or you haven't send the JSON yet?"
            else:
                print "Find the file from root that might get the wrong path?"
                query = self.queryResult
        for i in range(len(query)):
            if query[i]['title'] == name:
                return query[i]['id']
        print "didn't find the folder ( ", name, " )"
        return None
        
    def createFolder(self, folderName, parent=0):
        """
            Create the folder on the google drive
            
            Arg: the name of the new folder
            Ret: None
            
            Usage: ....
                   disk.createFolder(folderName = "monday", parent="MESS_ID")
                   ....
        """
        if parent == 0:
            print "create the folder at root?"
            file = self.drive.CreateFile({'title': folderName, 
                "mimeType": "application/vnd.google-apps.folder"})
        else:
            file = self.drive.CreateFile({'title': folderName, 
                "parents" : [{"id":parent}],
                "mimeType": "application/vnd.google-apps.folder"})
        file.Upload()
        
    def upload(self, fileName, ID=-1):
        """
            Upload the file by the given file name
        
            Arg: the name of the file which want to upload
            Ret: None
            
            Usage: ....
                   disk.upload(fileName="dog1.jpg")
                   ....
        """
        try:
            fp = open(fileName, 'rb')
            fp.close()
        except IOError:
            print "Is the file exist?"
            return;
        if not ID  == -1:
            file = self.drive.CreateFile({"parents": [{"id": ID}]})
        else:
            file = self.drive.CreateFile()
        file.SetContentFile(fileName)
        file.Upload()
        
    def download(self, fileName, ID=-1):
        """
            Download the file from the drive by the given file name
            
            Arg: the file name which want to download
            Ret: None
            
            Usage: ....
                   disk.download(fileName="dog1.jpg", ID="MESS_ID")
                   ....
        """
        if ID == -1:
            fileID = self.getID(name=fileName)
        else:
            fileList = self.getContainList(ID)
            fileID = self.getID(name=fileName, query=fileList)
        file = self.drive.CreateFile({'id': fileID,
            "parents":ID})
        file.GetContentFile(fileName)
        
    def getModified(self, position, folder_id=0):
        """
            Get the different name of the list
            
            Arg: the folder id
            Ret: the name list which didn't exist in drive, the origin query
            
            Usage: ....
                   diff = disk.download(position=".", ID="MESS_ID")
                   ....
        """
        driveDirList = self.getContainList(folder_id)
        nowDirList = os.listdir(position)
        res = []
        for fileOut in range(len(nowDirList)):
            exist = False
            for fileIn in range(len(driveDirList)):
                if nowDirList[fileOut] == driveDirList[fileIn]['title']:
                    exist = True
            if exist == False:
                res.append(nowDirList[fileOut])
        res = self.removeHiddenObject(res)
        return res
        
    def removeHiddenObject(self, llist):
        """
            (Hidden function)
            Remove the hidden file
            
            Arg: the process list
            Ret: the finish list
        """
        res = []
        for i in range(len(llist)):
            if not llist[i][:1] == '.':
                res.append(llist[i])
        return res
        
    def splitlist(self, llist, position):
        """
            Split the file name list and the folder name list
            
            Arg: the name list
            Ret: the file name list and the folder name list
            
            Usage: ....
                   f, n = disk.splitlist(mot, '.')
                   ....
        """
        _folder = []
        folderList = next(os.walk(position))[1]
        for i in range(len(folderList)):
            if folderList[i] in llist:
                llist.remove(folderList[i])
        return self.removeHiddenObject(llist), self.removeHiddenObject(folderList)
        
    def update(self, position='./', ID=0):
        """
            Update the contain of the folder
            
            Arg: None
            Ret: None
        """
        llist = self.getModified(position, folder_id=ID)
        n, f = self.splitlist(llist, position)
        for i in range(len(n)):
            self.upload(n[i])
        
        # update the sub-folder
        for i in range(len(f)):
            idd = self.getID(f[i])
            self.upload(position + f[i] + '/', idd)
        print "update successful!"
        
        
disk = GoogleDisk()
_q = disk.getFolder(id=0)
disk.update()