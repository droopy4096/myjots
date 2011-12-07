'''
Created on Dec 7, 2011

@author: dimon
'''

from PyQt4 import QtCore


class Note:
    def __init__(self, fileinfo):
        self.fileinfo=fileinfo
        
    def __str__(self):
        return str(self.fileinfo.filePath())
    
    def delete(self):
        pass
        
    
class Node:
    def __init__(self, path):
        self.dir=QtCore.QDir(path)
        self.children={}
        children_fi=self.dir.entryInfoList(filters=QtCore.QDir.Files|QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot|QtCore.QDir.Readable, sort=QtCore.QDir.Unsorted)
        for cf in children_fi:
            self.add(fileinfo=cf)
        
    def __str__(self):
        return str(self.dir.path())+"("+",".join([str(c) for c in self.children.values()])+")"
        
    def add(self,path=None,fileinfo=None):
        """Add child either by path or by fileinfo"""
        if fileinfo:
            fi=fileinfo
        elif path:
            fi=QtCore.QFileInfo(path)
        else:
            raise "Either path or FileInfo needs to be specified in Node::add call"
        if fi.isFile():
            self.children[fi.fileName()]=Note(fi)
        elif fi.isDir():
            self.children[fi.fileName()]=Node(fi.filePath())

    def delete(self,fileinfo):
        if fileinfo.path()==self.dir.path():
            print "will delete ", fileinfo.filePath()
        else:
            print "need to find better parent"

    def load(self):
        pass
    
    def get(self,fullpath):
        # need to extract first path level,
        # pass it onto the next Node
        pass
    

if __name__=="__main__":
    root=Node('/home/dimon/Notes')
    print root
    # fi=QtCore.QFileInfo('/home/dimon/Notes/node1/SubNote1')
    fi=QtCore.QFileInfo('/home/dimon/Notes/node1')
    root.delete(fi)
    