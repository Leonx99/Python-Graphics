from tkinter import *
from Controller import *




class MyButtonGroup:
    def __init__(self, rootWidget,parentView):


        self.parentView = parentView
        #add frame and attach buttons
        
        mainFrame = Frame(rootWidget)



        #Loading Frame
        loadFrame = Frame(mainFrame)

        label_load = Label(loadFrame, text = "File:")
        self.entry_load = Entry(loadFrame,width= 40)
        btn_browse = Button(loadFrame, text = "Browse", width=10, command=self.cmd_browse)
        btn_load = Button(loadFrame,text = "Load", width=10, command=self.cmd_load)
        btn_load.pack(side=RIGHT, padx=2, pady=2)


        btn_browse.pack(side=RIGHT, padx=2, pady=2)
        self.entry_load.pack(side=RIGHT, padx=0, pady=2)
        label_load.pack(side=RIGHT, padx=0, pady=2)
        loadFrame.pack(side=TOP, padx=2, pady=2,fill=X)



        #Rotate Frame
        rotateFrame = Frame(mainFrame)


        self.radio_Rotation_Value = IntVar()


        radio_X = Radiobutton(rotateFrame, text="X", variable=self.radio_Rotation_Value, value=1)
        radio_Y = Radiobutton(rotateFrame, text="Y", variable=self.radio_Rotation_Value, value=2)
        radio_Z = Radiobutton(rotateFrame, text="Z", variable=self.radio_Rotation_Value, value=3)
        label_Rotate_Degree = Label(rotateFrame, text = "Degree:")
        self.spin_Rotate_Degree = Spinbox(rotateFrame,from_=1,to=90,width=5)
        label_Rotate_Steps = Label(rotateFrame, text = "Steps:")
        self.spin_Rotate_Steps = Spinbox(rotateFrame,from_=1,to=10,width=5)
        btn_Rotate = Button(rotateFrame,text = "Rotate", width=10, command=self.cmd_Rotate)
        btn_Rotate.pack(side=RIGHT, padx=2, pady=2)



        self.spin_Rotate_Steps.pack(side=RIGHT, padx=2, pady=2)

        label_Rotate_Steps.pack(side=RIGHT, padx=0, pady=2)

        

        self.spin_Rotate_Degree.pack(side=RIGHT, padx=2, pady=2)

        label_Rotate_Degree.pack(side=RIGHT, padx=0, pady=2)



        radio_Z.pack(side=RIGHT, padx=2, pady=2)

        radio_Y.pack(side=RIGHT, padx=2, pady=2)

        radio_X.pack(side=RIGHT, padx=2, pady=2)




        rotateFrame.pack(side=TOP,padx=2, pady=2,fill=X)




        #Scale Frame
        scaleFrame = Frame(mainFrame)
        self.radio_Scale_Value = IntVar()




        radio_Z = Radiobutton(scaleFrame, text="ALL", variable=self.radio_Scale_Value, value=1)
        radio_AB = Radiobutton(scaleFrame, text="S-A", variable=self.radio_Scale_Value, value=2)
        spin_All_Scale = Label(scaleFrame, text = "ALL:")
        self.spin_All_Scale = Spinbox(scaleFrame,from_=0.01,to=5,format="%.2f",increment=0.01,width=5)
        label_S = Label(scaleFrame, text = "S:")
        self.entry_S_X_Scale = Entry(scaleFrame,width= 3)
        self.entry_S_Y_Scale = Entry(scaleFrame,width= 3)
        self.entry_S_Z_Scale = Entry(scaleFrame,width= 3)
        label_B = Label(scaleFrame, text = "A:")
        self.entry_A_X_Scale = Entry(scaleFrame,width= 3)
        self.entry_A_Y_Scale = Entry(scaleFrame,width= 3)
        self.entry_A_Z_Scale = Entry(scaleFrame,width= 3)
        label_Scale_Steps = Label(scaleFrame, text = "Steps:")
        self.spin_Scale_Steps = Spinbox(scaleFrame,from_=1,to=10,width=5)
        btn_Scale = Button(scaleFrame,text = "Scale", width=10, command=self.cmd_Scale)




        btn_Scale.pack(side=RIGHT, padx=2, pady=2)
        self.spin_Scale_Steps.pack(side=RIGHT, padx=2, pady=2)
        label_Scale_Steps.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_Z_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_Y_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_A_X_Scale.pack(side=RIGHT, padx=0, pady=2)
        label_B.pack(side=RIGHT, padx=0, pady=2)
        self.entry_S_Z_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_S_Y_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_S_X_Scale.pack(side=RIGHT, padx=0, pady=2)
        label_S.pack(side=RIGHT, padx=0, pady=2)
        self.spin_All_Scale.pack(side=RIGHT, padx=2, pady=2)
        spin_All_Scale.pack(side=RIGHT, padx=0, pady=2)
        radio_AB.pack(side=RIGHT, padx=2, pady=2)
        radio_Z.pack(side=RIGHT, padx=2, pady=2)
        scaleFrame.pack(side=TOP,padx=2, pady=2,fill=X)




        #translation Frame
        translationFrame = Frame(mainFrame)

        label_translation = Label(translationFrame, text = "Translation [dx,dy,dz]:")
        self.entry_d_X_Scale = Entry(translationFrame,width= 3)
        self.entry_d_Y_Scale = Entry(translationFrame,width= 3)
        self.entry_d_Z_Scale = Entry(translationFrame,width= 3)
        label_Scale_Steps = Label(translationFrame, text = "Steps:")
        self.spin_Translation_Steps = Spinbox(translationFrame,from_=1,to=10,width=5)
        btn_Translation = Button(translationFrame,text = "Translate", width=10, command=self.cmd_Translate)


        btn_Translation.pack(side=RIGHT, padx=2, pady=2)
        self.spin_Translation_Steps.pack(side=RIGHT, padx=2, pady=2)
        label_Scale_Steps.pack(side=RIGHT, padx=0, pady=2)
        self.entry_d_Z_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_d_Y_Scale.pack(side=RIGHT, padx=0, pady=2)
        self.entry_d_X_Scale.pack(side=RIGHT, padx=0, pady=2)
        label_translation.pack(side=RIGHT, padx=0, pady=2)
        translationFrame.pack(side=TOP,padx=2, pady=2,fill=X)



        #fly frame
        flyFrame = Frame(mainFrame)



        label_vrp1 = Label(flyFrame, text = "VRP1 [x,y,z]:")
        self.entry_X_VRP1 = Entry(flyFrame,width= 3)
        self.entry_Y_VRP1 = Entry(flyFrame,width= 3)
        self.entry_Z_VRP1 = Entry(flyFrame,width= 3)
        label_vrp2 = Label(flyFrame, text = "VRP2 [x,y,z]:")
        self.entry_X_VRP2 = Entry(flyFrame,width= 3)
        self.entry_Y_VRP2 = Entry(flyFrame,width= 3)
        self.entry_Z_VRP2 = Entry(flyFrame,width= 3)
        self.spin_Fly_Steps = Spinbox(flyFrame,from_=1,to=10,width=5)
        btn_Fly = Button(flyFrame,text = "Fly", width=10, command=self.buttonCall)


        btn_Fly.pack(side=RIGHT, padx=2, pady=2)
        self.spin_Fly_Steps.pack(side=RIGHT, padx=2, pady=2)
        self.entry_Z_VRP2.pack(side=RIGHT, padx=2, pady=2)
        self.entry_Y_VRP2.pack(side=RIGHT, padx=2, pady=2)
        self.entry_X_VRP2.pack(side=RIGHT, padx=2, pady=2)
        label_vrp2.pack(side=RIGHT, padx=2, pady=2)
        self.entry_Z_VRP1.pack(side=RIGHT, padx=2, pady=2)
        self.entry_Y_VRP1.pack(side=RIGHT, padx=2, pady=2)
        self.entry_X_VRP1.pack(side=RIGHT, padx=2, pady=2)
        label_vrp1.pack(side=RIGHT, padx=2, pady=2)



        flyFrame.pack(side=TOP,padx=2, pady=2,fill=X)

        mainFrame.pack()


        


    def buttonCall(self):
        print("button pressed")




    def cmd_browse(self):
        browsedFile = filedialog.askopenfilename(filetypes=[("allfiles", "*"), ("pythonfiles", "*.txt")])
        self.entry_load.delete(0, END)
        self.entry_load.insert(0, browsedFile)


    def cmd_load(self):
        self.parentView.loadFile(self.entry_load.get())

    def cmd_Rotate(self):
        self.parentView.rotate_call(self.radio_Rotation_Value.get(),self.spin_Rotate_Steps.get(),self.spin_Rotate_Degree.get())

    def cmd_Scale(self):
        try:steps = int(self.spin_Scale_Steps.get())   
        except ValueError: steps = None     
        try:a_Scale = [float(self.entry_A_X_Scale.get()),float(self.entry_A_Y_Scale.get()),float(self.entry_A_Z_Scale.get())]
        except ValueError:a_Scale = None
        try: s_Scale = [float(self.entry_S_X_Scale.get()),float(self.entry_S_Y_Scale.get()),float(self.entry_S_Z_Scale.get())]
        except ValueError:s_Scale = None
        try: all_Scale = float(self.spin_All_Scale.get())
        except ValueError:all_Scale = None
        try: scale_Type = int(self.radio_Scale_Value.get())
        except ValueError:scale_Type = None
        self.parentView.scale_call(steps,a_Scale,s_Scale,all_Scale,scale_Type)

    def cmd_Translate(self):
        x = float(self.entry_d_X_Scale.get())
        y = float(self.entry_d_Y_Scale.get())
        z = float(self.entry_d_Z_Scale.get())
        steps = int(self.spin_Translation_Steps.get())
        self.parentView.translation_call(x,y,z,steps)
