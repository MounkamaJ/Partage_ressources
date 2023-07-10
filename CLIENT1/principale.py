from tkinter import *
import tkinter as tk
from tkinter import ttk
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo

#global parameters, updating dynamically
all_content = []
all_images = []
img_idx = [0]
displayed_img = []

#initiallize a Tkinter root object
root = Tk()
root.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10
root.title("ClassMate")


#header area - logo & browse button
header = Frame(root, width=800, height=175, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

#BEGIN MENUES AND MENU WIDGETS

# menu on row 3
menu = Frame(root, width=800, height=50, bg="#c8c8c8")
menu.grid(columnspan=3, rowspan=1, row=3)

button1 = Button(root, text="Partage", font=("shanti", 10), height=1, width=15, command=lambda:create_gui())
button2 = Button(root, text="Recherche", font=("shanti", 10), height=1, width=15)
button3 = Button(root, text="Historique", font=("shanti", 10), height=1, width=15)

button1.grid(row=3, column=0)
button2.grid(row=3, column=1)
button3.grid(row=3, column=2)


#main content area - text and image extraction
main_content = Frame(root, width=800, height=250, bg="#3d6466")
main_content.grid(columnspan=3, rowspan=2, row=4)


#BEGIN INITIAL APP COMPONENTS
display_logo('logo.png', 0, 0)


#browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway",12), bg="#3d6466", fg="white", height=1, width=15)
browse_text.set("Se déconnecter")
browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

root.mainloop()