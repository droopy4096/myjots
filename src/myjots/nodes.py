'''
Created on Dec 7, 2011

@author: dimon
'''

from PyQt4 import QtCore


class Note:
    def __init__(self, fileinfo,parent=None):
        self.fileinfo=fileinfo
        self.parent=parent
        
    def __str__(self):
        return str(self.fileinfo.filePath())
    
    def delete(self):
        pass
    
    def create(path):
        """Static method for creating on-disk Nodes"""
        pass
        
    
class Node(Note):

    # dictionary of tuples: child[path]=(fileInfo,Note|Node)
    children=None
    
    def __init__(self, path,parent=None):
        # super(Node,self).__init__(QtCore.QFileInfo(path))
        Note.__init__(self,QtCore.QFileInfo(path),parent)
        self.dir=QtCore.QDir(path)
        self.repopulate()

    def repopulate(self):
        self.children={}
        self.populate()
        
    def populate(self):
        children_fi=self.dir.entryInfoList(filters=QtCore.QDir.Files|QtCore.QDir.Dirs|QtCore.QDir.NoDotAndDotDot|QtCore.QDir.Readable, sort=QtCore.QDir.Unsorted)
        for cf in children_fi:
            self.add(fileinfo=cf)
        
    def __str__(self):
        return str(self.dir.path())+"("+",".join([str(c[1]) for c in self.children.values()])+")"
        
    def createNote(self,filepath,filepath_list=None):
        ##TODO this needs more work - it probably doesn't even work
        fi=QFileInfo(filepath)
        if fi.path() == self.dir.path():
            self._createNode(self,filepath)
        else:
            node_path_list=self.dir.path().split(self.dir.separator())
            note_path_list=filepath.split(self.dir.separator())
            i=0
            try:
                while node_path_list[i]==note_path_list[i]:
                    i=i+1
            except IndexError:
                # full match initially
                node_pl=len(node_path_list)
                note_pl=len(note_path_list)
                if node_pl>note_pl:
                    # can't figure out why would that be
                    raise "WTF? node_path longer than note_path???"
                elif note_pl == note_pl:
                    # creating the note inside this node
                    self._createNote(fi.fileName())
                else:
                    # we need to look elsewhere: in children
                    for c in self.children.values():
                        if c[0].isDir():
                            c[1].createNote(filepath)

    def _createNote(self,nodename):
        """create new Node"""
        nodepath=self.dir.filePath(nodename)
        Node.create(nodepath)
        self.add(path=nodepath)

    def add(self,path=None,fileinfo=None):
        """Adds existing child either by path or by fileinfo"""
        if fileinfo:
            fi=fileinfo
        elif path:
            fi=QtCore.QFileInfo(path)
        else:
            raise "Either path or FileInfo needs to be specified in Node::add call"
        if fi.isFile():
            self.children[fi.fileName()]=(fi,Note(fi,parent=self))
        elif fi.isDir():
            self.children[fi.fileName()]=(fi,Node(fi.filePath(),parent=self))

    def delete(self,fileinfo):
        if fileinfo.path()==self.dir.path():
            print "will delete ", fileinfo.filePath()
        else:
            print "need to find better parent"

    def getChildren(self):
        return self.children
    
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
    