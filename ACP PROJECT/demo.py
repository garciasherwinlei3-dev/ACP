import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import dashboard

USERNAME = "admin"
PASSWORD = "1234"

def login():
    user = username_entry.get()
    pwd = password_entry.get()

    if user == USERNAME and pwd == PASSWORD:
        messagebox.showinfo("Login Successful", "Welcome!")
        root.withdraw()
        dashboard.open_dashboard()
    else:
        messagebox.showerror("Invalid!", "Incorrect username or password.")

def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        toggle_btn.config(text="Show")
    else:
        password_entry.config(show="")
        toggle_btn.config(text="Hide")
        
root = tk.Tk()
root.title("LOGIN")
root.geometry("844x390") 
root.resizable(False, False)


background = ImageTk.PhotoImage(Image.open("ready.jpg"))
bg_label = tk.Label(root, image=background)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()

title_label = tk.Label(root, text= "MAY", font = ("Times New Roman", 25 , "bold"),bg="#c8442d",fg="white")
title_label.pack(pady=5)


tk.Label(root, text = "Username:", font=("Times New Roman", 12),bg="#c8442d",fg="white").pack()
username_entry = tk.Entry(root, font = ("Times New Roman", 12),bg="#D3D3D3",fg="black")
username_entry.pack(pady = 5)

tk.Label(root, text = "Password:", font = ("Times New Roman", 12),bg="#c8442d",fg="white").pack()
password_entry = tk.Entry(root, font = ("Times New Roman", 12), show="*",bg="#D3D3D3",fg="black")
password_entry.pack(pady = 5)

toggle_btn = tk.Button(root, text = "Show", command = toggle_password)
toggle_btn.pack(pady = 3)

login_btn = tk.Button(root, text = "Login", font= ("Times New Roman", 12), width=12, command = login)
login_btn.pack(pady= 10)

root.mainloop()
