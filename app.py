import Tkinter as tk
#from Tkinter import*
from Tkinter import Tk, Frame, Menu
from PIL import ImageTk,Image, ImageDraw
#import Image,ImageDraw
from tkColorChooser import askcolor
import  Tkconstants, tkFileDialog
import subprocess
import os
import tkFileDialog
import tkFont
import sys
import operator, itertools
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class PaintApp(Frame):
    def __init__(self,parent,posx,posy,*kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.eraserMode = False
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 1500
        self.sizey = 700
        self.color = 'black'
        self.color1 = 'yellow'
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.line_width = 10
        self.save = False
        self.eraseColor = 'white'
        self.flag = False
        self.image=Image.new("RGBA",(self.sizex,self.sizey),(255,255,255))
        
        self.draw=ImageDraw.Draw(self.image)
        self.drawing_area = tk.Canvas(self.parent,width=self.sizex,height=self.sizey,bg = 'white')
        self.drawPage()

        self.drawing_area.place(x=self.posx,y=self.posy)

        #self.drawing_area.config(scrollregion=self.drawing_area.bbox("all"))


        #pen button
        self.pen =  tk.Button(self.parent,text="Pen",width=10,bg='green',command=self.use_pen,cursor='pencil')
        self.pen.grid(row=0, column=0)

        #eraser button
        self.clearPoint=tk.Button(self.parent,text="Eraser ",width=10,bg='blue',command=self.del_,cursor='icon')
        self.clearPoint.grid(row=1,column=0)

        #Highlight button
        self.highlight=tk.Button(self.parent,text="Highlight ",width=10,bg='red',command=self.highLight,cursor='pencil')
        self.highlight.grid(row=2,column=0)

        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = parent

    def highLight(self):
        self.flag = True
        if self.flag == True:
            self.drawing_area.bind("<Motion>", self.highLight1)
            self.drawing_area.bind("<ButtonPress-1>", self.b1down)
            self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        
        self.flag = False


        
    def drawPage(self):
        for a in range(0,3000,35):
            self.drawing_area.create_line(0 ,0 +a,2000,0 + a,fill = 'black')
            self.draw.line([(0,0+a),(2000,0+a)],fill='black')
        self.drawing_area.create_line(100 ,0,100,700,fill = 'red')
        self.draw.line([(100,0),(100,700)],fill='red')


    def initUI(self):
        self.parent.title("KINTU")
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="New ", command=self.new)
        fileMenu.add_command(label="Open", command=self.add)
        fileMenu.add_command(label="Save ", command=self.asksaveasfilename)
        fileMenu.add_command(label="Clear All", command=self.clear)
        fileMenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menubar)
        editMenu.add_command(label="Insert Image", command=self.openImage)
        menubar.add_cascade(label="Edit", menu=editMenu)

        toolsMenu = Menu(menubar)
        toolsMenu.add_command(label="color", command=self.choose_color)
        menubar.add_cascade(label="Tool", menu=toolsMenu)

    def new(self):
        self.exit()
        root=tk.Tk()
        root.wm_geometry("%dx%d+%d+%d" % (self.sizex, self.sizey, 10, 10))
        root.config(bg='white')
        PaintApp(root,10,10)
        root.mainloop()

    def exit(self):
        if (self.save==False):
            self.asksaveasfilename()

        root.destroy()


    def add(self):

        fname = tkFileDialog.askopenfilename(filetypes = (("Template files", "*.jpg"), ("All files", "*")))
        img = ImageTk.PhotoImage(Image.open(fname))
        im = Image.open(fname).convert("RGBA")
        x,y = im.size;
        self.clear()
        self.drawPage();
        self.drawing_area.create_image(int(x/2),int(y/2),image=img)
        self.image.paste(im,im)
        imglabel = Label(self.parent,image=img).grid(row=4,column=10)

    def asksaveasfilename(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)

        if filename:

           self.image.save(filename)
           self.save = True
           file = open(filename,encoding = "ISO-8859-1")
           file1 = drive.CreateFile({'title':'Hello.txt'})
           for line in file:
               file1.SetContentString(line)
            file1.Upload()

    def use_pen(self):
        self.eraserMode = False
        self.color = 'black'
        if self.flag == False:
            self.drawing_area.bind("<Motion>", self.motion)
            self.drawing_area.bind("<ButtonPress-1>", self.b1down)
            self.drawing_area.bind("<ButtonRelease-1>", self.b1up)



    def openImage(self):

        fname = tkFileDialog.askopenfilename(filetypes = (("Template files", "*.png"), ("All files", "*")))
        img = ImageTk.PhotoImage(Image.open(fname))
        im = Image.open(fname).convert("RGBA")
        x,y = im.size;
        #img = Image.resize((250, 250), Image.ANTIALIAS)
        a1 = self.drawing_area.create_image(int(x/2),int(y/2),image=img)

        self.image.paste(im,im)

        #Displaying ImageTk
        imglabel = Label(self.parent,image=img).grid(row=4,column=10)


    def clear(self):

        self.drawing_area.delete("all")
        self.image=Image.new("RGBA",(self.sizex,self.sizey),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        self.drawPage()

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
        #print("Motion")
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:

                if(self.eraserMode == True):

                    self.parent.config(cursor = 'icon')
                    event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill='white')
                    self.draw.line(((self.xold,self.yold),(event.x,event.y)),(255,255,255),width=3)
                    self.drawPage()


                if(self.eraserMode == False):

                    self.parent.config(cursor = 'pencil')
                    #print(self.color)
                    event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill=self.color)
                    self.draw.line(((self.xold,self.yold),(event.x,event.y)),(self.color),width=3)
                    #event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill=self.color)

        self.xold = event.x
        self.yold = event.y
        

    def highLight1(self,event):
    
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                if(self.eraserMode == False):

                    self.parent.config(cursor = 'pencil')
                    #print(self.color)
                    event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=10,fill=self.color1,stipple='gray50')
                    self.draw.line(((self.xold,self.yold),(event.x,event.y)),(self.color1),width=3)
                    #event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill=self.color)

        self.xold = event.x
        self.yold = event.y
    
    

    def del_(self):
        self.eraserMode = True

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

if __name__ == "__main__":
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    root=tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (300, 300, 10, 10))
    root.config(bg='white')
    PaintApp(root,10,10)
    root.mainloop()
