'''
Created on Dec 7, 2011

@author: dimon
'''

class Note:
    def __init__(self, filename):
        pass
    
class Node:
    def __init__(self, path):
        self.notes=[]
        
    def load(self):
        pass
    
    def get(self,fullpath):
        # need to extract first path level,
        # pass it onto the next Node
        pass
    
