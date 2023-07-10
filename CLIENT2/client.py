import os
import sys
from tkinter import *
import tkinter as tk
from tkinter import Tk
import customtkinter as ctk
from tkinter import Tk, messagebox, Canvas, Entry, Text, Button, PhotoImage, filedialog, simpledialog
from PIL import ImageTk, Image
import datetime
import socket
import struct
import subprocess
import requetesClient
from numpy import random
import requetesClient

repertoire_courant = os.path.dirname(os.path.abspath(__file__))
def mode_serveur():
    chemin_relatif = os.path.join(repertoire_courant, "modeServeur.py")
    subprocess.Popen([sys.executable, chemin_relatif])


def authenticate(username, password):
    valid_username = "john"
    valid_password = "password"
    if username == valid_username and password == valid_password:
        return True
    else:
        return False


def send_request(choice):
    data = struct.pack('!i', choice)
    client_socket.sendall(data)


def share_file():
    initial_directory = os.path.expanduser("~")
    selected_file = filedialog.askopenfilename(title = "Sélectionnez le fichier à partager", initialdir=initial_directory)
    if selected_file:
        filename = os.path.basename(selected_file)
        send_request(1)
        requetesClient.partage(client_socket, filename)
        messagebox.showinfo("Partager", "Le partage a été éffectué avec succès")


def search_file():
    keyword = simpledialog.askstring("Rechercher", "Entrez le mot-clé de recherche")
    if keyword:
        with open('LOGS/log.txt', 'a') as logs_file:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logs_file.write(f"{current_time} - Fichier {keyword} recherché: \n")
    
        send_request(2)
        requetesClient.recherche(client_socket, keyword)


def historique():
    try:
        with open('LOGS/log.txt', 'r') as file:
            content = file.read()
            messagebox.showinfo("Historique", content)
    except FileNotFoundError:
        messagebox.showinfo("Erreur", "Le fichier Historique n'existe pas.")


def show_main_window():
    #global parameters, updating dynamically
    all_content = []
    all_images = []
    img_idx = [0]
    displayed_img = []

    def quitter():
        root.destroy()
        show_home_window()

    #initiallize a Tkinter root object
    root = Tk()
    root.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10
    root.title("ClassMate")


    #header area - logo & browse button
    header = Frame(root, width=800, height=175, bg="white")
    header.grid(columnspan=3, rowspan=2, row=0)

    
    # menu on row 3
    menu = Frame(root, width=800, height=50, bg="#c8c8c8")
    menu.grid(columnspan=3, rowspan=1, row=3)

    button1 = Button(root, text="Partage", font=("shanti", 10), height=1, width=15, command=share_file)
    button2 = Button(root, text="Recherche", font=("shanti", 10), height=1, width=15, command=search_file)
    button3 = Button(root, text="Historique", font=("shanti", 10), height=1, width=15, command=historique)

    button1.grid(row=3, column=0)
    button2.grid(row=3, column=1)
    button3.grid(row=3, column=2)


    #main content area - text and image extraction
    main_content = Frame(root, width=800, height=250, bg="#3d6466")
    main_content.grid(columnspan=3, rowspan=2, row=4)

    #BEGIN INITIAL APP COMPONENTS
    requetesClient.display_logo('logo.png', 0, 0)


    #browse button
    browse_text = StringVar()
    browse_btn = Button(root, textvariable=browse_text, command=lambda:quitter(), font=("Raleway",12), bg="#3d6466", fg="white", height=1, width=15)
    browse_text.set("Se déconnecter")
    browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

    root.mainloop()


def show_login_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    login = ctk.CTk()
    login.title("ClassMate")
    x = login.winfo_screenwidth() // 2
    y = int(login.winfo_screenheight() * 0.1)
    login.geometry('500x500+' + str(x) + '+' + str(y))

    # Function to handle login submission
    def submit_login():
        username = champ1.get()
        password = champ2.get()

        if authenticate(username, password):
            login.destroy()
            show_main_window()
        else:
            messagebox.showerror("Echec de connexion", "Identifiants invalides")
    

    def go_back():
        login.destroy()
        show_home_window()

    frame = ctk.CTkFrame(master=login)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    frame.tkraise()
    frame.pack_propagate(False)

    label = ctk.CTkLabel(master=frame, text="Se connecter")
    label.pack(pady=12, padx=10)

    champ1 = ctk.CTkEntry(master=frame, placeholder_text="Identifiant")
    champ1.pack(pady=12)

    champ2 = ctk.CTkEntry(master=frame, placeholder_text="Mot de passe", show="*")
    champ2.pack(pady=12)

    button = ctk.CTkButton(master=frame, text="Connexion", command=submit_login)
    button.pack(pady=12, padx=10)

    checkbox = ctk.CTkCheckBox(master=frame, text="Se souvenir de moi")
    checkbox.pack(pady=12, padx=10)

    button = ctk.CTkButton(master=frame, text="Retour", command=go_back)
    button.pack(pady=12, padx=10)

    login.mainloop()


def show_home_window():
    root = Tk()
    root.title("ClassMate")
    root.eval("tk::PlaceWindow . center")
    bg_colour = "#3d6466"

    root.geometry('+%d+%d'%(350,10))

    frame1 = tk.Frame(root, width=500, height=600, bg=bg_colour)
    frame1.grid(row=0, column=0, sticky="nesw")

    frame1.tkraise()
    frame1.pack_propagate(False)

    def login_window():
        root.destroy()
        show_login_window()

    def quitter():
        client_socket.close()
        root.quit()

    logo_img = ImageTk.PhotoImage(file="./logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(
        frame1,
        text="Prêt à partager?, Connectez vous!",
        bg=bg_colour,
        fg="white",
        font=("TkMenuFont", 14)
    ).pack(pady=20)
    

    button1= tk.Button(
        frame1,
        text="Se Connecter",
        font=("TkHeadingFont", 12),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: login_window()
    ).pack(pady=70)


    root.mainloop()


if __name__ == '__main__':
    mode_serveur()

    # Connexion au serveur distant
    server_host = '127.0.0.1'
    server_port = 8000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    show_home_window()

    client_socket.close()
