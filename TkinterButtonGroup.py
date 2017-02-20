from tkinter import *
from Controller import *




class MyButtonGroup:
    def __init__(self, rootWidget,parentView):


        self.parentView = parentView
        #add frame and attach buttons
        
        mainFrame = Frame(rootWidget)



        #Loading Frame
        loadFrame = Frame(mainFrame)

        btn_load = Button(loadFrame,text = "Load", width=10, command=self.cmd_load)
        btn_load.pack(side=RIGHT, padx=2, pady=2)

        btn_browse = Button(loadFrame, text = "Browse", width=10, command=self.cmd_browse)
        btn_browse.pack(side=RIGHT, padx=2, pady=2)

        self.entry_load = Entry(loadFrame,width= 40)
        self.entry_load.pack(side=RIGHT, padx=0, pady=2)

        label_load = Label(loadFrame, text = "File:")
        label_load.pack(side=RIGHT, padx=0, pady=2)


        loadFrame.pack(side=TOP, padx=2, pady=2,fill=X)



        #Rotate Frame
        rotateFrame = Frame(mainFrame)

        btn_Rotate = Button(rotateFrame,text = "Rotate", width=10, command=self.buttonCall)
        btn_Rotate.pack(side=RIGHT, padx=2, pady=2)


        self.spin_Rotate_Steps = Spinbox(rotateFrame,from_=1,to=10,width=5)
        self.spin_Rotate_Steps.pack(side=RIGHT, padx=2, pady=2)
        label_Rotate_Steps = Label(rotateFrame, text = "Steps:")
        label_Rotate_Steps.pack(side=RIGHT, padx=0, pady=2)

        
        self.spin_Rotate_Degree = Spinbox(rotateFrame,from_=1,to=90,width=5)
        self.spin_Rotate_Degree.pack(side=RIGHT, padx=2, pady=2)
        label_Rotate_Degree = Label(rotateFrame, text = "Degree:")
        label_Rotate_Degree.pack(side=RIGHT, padx=0, pady=2)


        self.entry_B_Z_Rotate = Entry(rotateFrame,width= 3)
        self.entry_B_Z_Rotate.pack(side=RIGHT, padx=0, pady=2)
        self.entry_B_Y_Rotate = Entry(rotateFrame,width= 3)
        self.entry_B_Y_Rotate.pack(side=RIGHT, padx=0, pady=2)
        self.entry_B_X_Rotate = Entry(rotateFrame,width= 3)
        self.entry_B_X_Rotate.pack(side=RIGHT, padx=0, pady=2)
        label_B = Label(rotateFrame, text = "B:")
        label_B.pack(side=RIGHT, padx=0, pady=2)


        self.entry_A_Z_Rotate = Entry(rotateFrame,width= 3)
        self.entry_A_Z_Rotate.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_Y_Rotate = Entry(rotateFrame,width= 3)
        self.entry_A_Y_Rotate.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_X_Rotate = Entry(rotateFrame,width= 3)
        self.entry_A_X_Rotate.pack(side=RIGHT, padx=0, pady=2)
        label_B = Label(rotateFrame, text = "A:")
        label_B.pack(side=RIGHT, padx=0, pady=2)


        self.radio_Rotation_Value = IntVar()
        radio_AB = Radiobutton(rotateFrame, text="AB", variable=self.radio_Rotation_Value, value=4)
        radio_AB.pack(side=RIGHT, padx=2, pady=2)
        radio_Z = Radiobutton(rotateFrame, text="Z", variable=self.radio_Rotation_Value, value=3)
        radio_Z.pack(side=RIGHT, padx=2, pady=2)
        radio_Y = Radiobutton(rotateFrame, text="Y", variable=self.radio_Rotation_Value, value=2)
        radio_Y.pack(side=RIGHT, padx=2, pady=2)
        radio_X = Radiobutton(rotateFrame, text="X", variable=self.radio_Rotation_Value, value=1)
        radio_X.pack(side=RIGHT, padx=2, pady=2)




        rotateFrame.pack(side=TOP,padx=2, pady=2,fill=X)




        #Scale Frame
        scaleFrame = Frame(mainFrame)

        btn_Scale = Button(scaleFrame,text = "Scale", width=10, command=self.buttonCall)
        btn_Scale.pack(side=RIGHT, padx=2, pady=2)


        self.spin_Rotate_Steps = Spinbox(scaleFrame,from_=1,to=10,width=5)
        self.spin_Rotate_Steps.pack(side=RIGHT, padx=2, pady=2)
        label_Rotate_Steps = Label(scaleFrame, text = "Steps:")
        label_Rotate_Steps.pack(side=RIGHT, padx=0, pady=2)


        self.entry_A_Z_Scale = Entry(scaleFrame,width= 3)
        self.entry_A_Z_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_Y_Scale = Entry(scaleFrame,width= 3)
        self.entry_A_Y_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_X_Scale = Entry(scaleFrame,width= 3)
        self.entry_A_X_Scale.pack(side=RIGHT, padx=0, pady=2)
        label_B = Label(scaleFrame, text = "A:")
        label_B.pack(side=RIGHT, padx=0, pady=2)

        self.entry_S_Z_Scale = Entry(scaleFrame,width= 3)
        self.entry_S_Z_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_S_Y_Scale = Entry(scaleFrame,width= 3)
        self.entry_S_Y_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_S_X_Scale = Entry(scaleFrame,width= 3)
        self.entry_S_X_Scale.pack(side=RIGHT, padx=0, pady=2)
        label_S = Label(scaleFrame, text = "S:")
        label_S.pack(side=RIGHT, padx=0, pady=2)


        self.spin_All_Scale = Spinbox(scaleFrame,from_=0.01,to=5,format="%.2f",increment=0.01,width=5)
        self.spin_All_Scale.pack(side=RIGHT, padx=2, pady=2)
        spin_All_Scale = Label(scaleFrame, text = "ALL:")
        spin_All_Scale.pack(side=RIGHT, padx=0, pady=2)



        self.radio_Scale_Value = IntVar()
        radio_AB = Radiobutton(scaleFrame, text="S-A", variable=self.radio_Scale_Value, value=2)
        radio_AB.pack(side=RIGHT, padx=2, pady=2)
        radio_Z = Radiobutton(scaleFrame, text="ALL", variable=self.radio_Scale_Value, value=1)
        radio_Z.pack(side=RIGHT, padx=2, pady=2)
        
        
        
        
        scaleFrame.pack(side=TOP,padx=2, pady=2,fill=X)


        mainFrame.pack()


        


    def buttonCall(self):
        print("button pressed")




    def cmd_browse(self):
        browsedFile = filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")])
        self.entry_load.delete(0, END)
        self.entry_load.insert(0, browsedFile)


    def cmd_load(self):
        self.parentView.loadFile(self.entry_load.get())
