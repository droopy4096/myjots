#!/usr/bin/env python

import sys, os

from myjots import nodes

from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from PyKDE4.kparts import *
from PyKDE4.khtml import KHTMLView, KHTMLPart


from PyQt4 import QtGui, QtCore, QtWebKit
from PyQt4.QtCore import SIGNAL, QUrl

class NotesTreeModel(QtGui.QStandardItemModel):
    def __init__(self, path, parent=None):
        super(NotesTreeModel, self).__init__(parent)
        self.rootItem=QtGui.QStandardItem("Note")

class Modes:
    EDIT=True
    VIEW=False

class MyJotsWindow (KMainWindow):
    
    # Settings
    notes_base=None
    root_node=None
    nav_mode=None
    
    # View elements
    editor=None
    tree=None
    viewedit=None
    editor_pos=None
    viewer_pos=None
    
    # Actions
    quitAct=None
    
    def __init__ (self):
        KMainWindow.__init__(self)

        # self.resize(640, 480)
        self.nav_mode=Modes.EDIT

        self.notes_base='/home/dimon/Notes'
        self.root_node=nodes.Node(self.notes_base)
        
        self.createActions()
        self.createLayout()
        self.connectSignals()
        self.loadNotes()

    def loadNotes(self):

        tree=self.tree
        tree.clear()
 
        notes_walker=QtCore.QDirIterator(self.notes_base,
                             QtCore.QDirIterator.FollowSymlinks|QtCore.QDirIterator.Subdirectories)
        dir_dict={}
        while(notes_walker.hasNext()):
            nwi=notes_walker.next()
            ffn=notes_walker.fileName()
            fi=notes_walker.fileInfo()
            fpath=fi.path()
            if ffn in ['.','..']:
                continue

            print fpath, ffn
            if fpath in dir_dict.keys():
                parent=dir_dict[fpath]
                print fpath, "", parent.text(0)
            else:
                parent=tree

            item=QtGui.QTreeWidgetItem(parent)
            item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
            item.setText(0,ffn)
            item.file_info=fi

            if fi.isDir():
                dir_dict[fi.filePath()]=item

    def treeItemChanged(self,item,n):
        ## rename file here...
        print "changed!",item.text(n), item.file_info.path(), item.file_info.fileName()

    def treeItemEdit (self, item, n):
        self.tree.editItem(item,n)

    def treeItemClicked (self, item, n):
        self._updateEditor(item,n)
        self._updateViewer(item,n)

    def _updateEditor(self,item,n):
        fpath=item.file_info.canonicalFilePath()
        # print fpath
        f=QtCore.QFile(fpath)
        f.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text)
        fstream=QtCore.QTextStream(f)
        aa=fstream.readAll()
        self.editor.clear()
        self.editor.document().setPlainText(aa)
        # self.editor.loadResource(1,QUrl(fpath))
        self.setWindowTitle(item.text(n))

    def _updateViewer(self,item,n):
        # fetch appropriate Node
        # and call render
        self.htmlview.setHtml("<html><body>Hello</body></html>")
        self.setWindowTitle(item.text(n))


    def createActions(self):
        self.quitAct=KAction("Quit",self,triggered=self.close)
        self.toggleModeAct=KAction("Toggle",self,triggered=self.toggle)

    def toggle(self):
        self.nav_mode=not self.nav_mode
        if self.nav_mode == Modes.EDIT:
            self.viewedit.setCurrentIndex(self.editor_pos)
        else:
            self.viewedit.setCurrentIndex(self.viewer_pos)
        
    def createLayout(self):
        widget=QtGui.QWidget()
        ## self.setCentralWidget(widget)

        vbox = KVBox(widget)
        vbox.setContentsMargins(5, 5, 5, 5)
        self.setCentralWidget(vbox)

        topFiller = QtGui.QWidget(vbox)

        hbox=KHBox(vbox)
        treebox=KVBox(hbox)
        searchline=KTreeWidgetSearchLine(treebox)
        
        self.tree=QtGui.QTreeWidget(treebox)
                
        # self.fs_model=QtGui.QFileSystemModel()
        # self.fs_model.setRootPath(self.notes_base)
        # self.tree.setModel(self.fs_model)
        
        header=QtGui.QTreeWidgetItem()
        header.setText(0,"Notes")
        self.tree.setHeaderItem(header)

        searchline.addTreeWidget(self.tree)


        self.viewedit=QtGui.QStackedWidget(hbox)
        self.editor=KTextEdit()
        self.editor_pos=self.viewedit.addWidget(self.editor)
        # self.viewedit.setCurrentIndex(0)
        
        self.htmlview=QtWebKit.QWebView()
        self.viewer_pos=self.viewedit.addWidget(self.htmlview)
        # self.viewedit.setCurrentIndex(1)
        self.viewedit.setCurrentIndex(self.editor_pos)


        bottomFiller = QtGui.QWidget(vbox)

        filem = self.menuBar().addMenu("&File")
        filem.addAction(self.quitAct)
        editm = self.menuBar().addMenu("&Edit")
        editm.addAction(self.toggleModeAct)

    def connectSignals(self):
        self.connect (self.tree, SIGNAL ('itemClicked (QTreeWidgetItem *, int)'),
                        self.treeItemClicked)
        self.connect (self.tree, SIGNAL ('itemDoubleClicked (QTreeWidgetItem *, int)'),
                        self.treeItemEdit)

        self.connect (self.tree, SIGNAL ('itemChanged (QTreeWidgetItem *, int)'),
                        self.treeItemChanged)

        
#--------------- main ------------------

if __name__ == '__main__':

    appName     = "MyJots"
    catalog     = ""
    programName = ki18n("My Jots")
    version     = "0.1"
    description = ki18n("Re-implementation of KJots")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2012 Dimon")
    text        = ki18n("none")
    homePage    = "makovey.net"
    bugEmail    = "dimon@makovey.net"
    
    aboutData   = KAboutData(appName, catalog, programName, version, description,
                                license, copyright, text, homePage, bugEmail)
            
    KCmdLineArgs.init(sys.argv, aboutData)
        
    app = KApplication()
    mainWindow = MyJotsWindow()
    mainWindow.show()
    app.exec_()
