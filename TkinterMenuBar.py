from tkinter import *



class MyTkinterMenuBar:

    def __init__(self, rootWidget):

        
        menubar = Menu(rootWidget)

        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="command1", command=self.command1)
        filemenu.add_command(label="command2", command=self.command2)
        menubar.add_cascade(label="File", menu=filemenu)

        # create a pulldown menu, and add it to the menu bar
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="command3", command=self.command1)
        editmenu.add_command(label="command4", command=self.command2)
        menubar.add_cascade(label="edit", menu=editmenu)





                
        # display the menu
        rootWidget.config(menu=menubar)


    def command1(self):
        print ("command 1")
        
    def command2(self):
        print ("command 2")