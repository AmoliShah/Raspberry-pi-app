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

class PaintApp(Frame):
    def __init__(self,parent,posx,posy,*kwargs):
        Frame.__init__(self, parent)   
        self.parent = parent    
        self.initUI()
        self.eraserMode = False
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 2000
        self.sizey = 300
        self.color = 'black'
        self.b1 = "up"
        self.xold = None
        self.yold = None 
        self.line_width = 10
        self.save = False
        self.eraseColor = 'white'
        
        self.drawing_area = tk.Canvas(self.parent,width=self.sizex,height=self.sizey,bg = 'white')
        for a in range(0,2000,35):
            self.drawing_area.create_line(0 ,0 +a,2000,0 + a,fill = 'black')
        self.drawing_area.create_line(100 ,0,100,300,fill = 'red')
        
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.drawing_area.config(scrollregion=self.drawing_area.bbox("all"))

        #pen button
        self.pen =  tk.Button(self.parent,text="pen",width=10,bg='green',command=self.use_pen,cursor='pencil')
        self.pen.grid(row=0, column=0)
        
        #eraser button
        self.clearPoint=tk.Button(self.parent,text="eraser ",width=10,bg='blue',command=self.del_,cursor='icon')
        self.clearPoint.grid(row=1,column=0)

        self.image=Image.new("RGB",(400,400),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = parent

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
    
    def new(self):

        self.exit()
        root=tk.Tk()
        root.wm_geometry("%dx%d+%d+%d" % (300, 300, 10, 10))
        root.config(bg='white')
        PaintApp(root,10,10)
        root.mainloop()

    def exit(self):

        if (self.save==False):
            self.asksaveasfilename()
        
        root.destroy()

    def add(self):
        print "exit"    
    
    def asksaveasfilename(self):
        filename = tkFileDialog.asksaveasfilename(**self.file_opt)

        if filename:
           
           self.image.save(filename)
           self.save = True
            
    def use_pen(self):

         self.eraserMode = False
         self.color = 'black'

    def openImage(self):
        
        fname = tkFileDialog.askopenfilename(filetypes = (("Template files", "*.png"), ("All files", "*")))
        img = ImageTk.PhotoImage(Image.open(fname))
        #img = Image.resize((250, 250), Image.ANTIALIAS)
        imagesprite = self.drawing_area.create_image(20,20,image=img)
        tk.Frame(self.parent) 
        #Displaying ImageTk
        imglabel =  Label(self.parent,image=img).grid(row=2,column=1)

    def clear(self):

        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(300,300),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)
        for a in range(0,2000,35):
            self.drawing_area.create_line(0 ,0 +a,2000,0 + a,fill = 'black')
            self.drawing_area.create_line(100 ,0,100,300,fill = 'red')

    def b1down(self,event):
        self.b1 = "down"

    def b1up(self,event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
        
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                
                if(self.eraserMode == True):
                    
                    self.parent.config(cursor = 'icon')
                    event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill='white')     		                  
                    self.draw.line(((self.xold,self.yold),(event.x,event.y)),(255,255,255),width=3)
                    for a in range(0,2000,35):
                        self.drawing_area.create_line(0 ,0 +a,2000,0 + a,fill = 'black')
                        self.drawing_area.create_line(100 ,0,100,300,fill = 'red')
                    
       			     
                if(self.eraserMode == False):      

                    self.parent.config(cursor = 'pencil')
                    event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=3,fill=self.color)
                    self.draw.line(((self.xold,self.yold),(event.x,event.y)),(self.color),width=3)     
        self.xold = event.x
        self.yold = event.y
                    
    def del_(self):
        self.eraserMode = True
                
    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

if __name__ == "__main__":
    root=tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (300, 300, 10, 10))
    root.config(bg='white')
    PaintApp(root,10,10)
    root.mainloop()
