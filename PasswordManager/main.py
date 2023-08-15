from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
YELLOW = "#f7f5dd"


# -------------------GENERATE PASSWORD---------------#


def password():
    password_l = []

    for l in range(0, 6):
        password_l += random.choice(letters)

    for s in range(0, 6):
        password_l += random.choice(symbols)

    for n in range(0, 6):
        password_l += random.choice(numbers)

    random.shuffle(password_l)

    password = ""
    for i in password_l:
        password += i
    password_entry.delete(0, 'end')
    password_entry.insert(END, string=f"{password}")
    pyperclip.copy(password)


# -------------------ADD DATA----------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password_add = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password_add,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password_add) == 0:
        messagebox.showwarning(title="Empty", message="Please don't leave any field empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            email_entry.insert(0, string="@gmail.com")


# -------------------SEARCH DATA ----------------------------- #


def search():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            data_found = data[f'{website}']
    except (KeyError, FileNotFoundError):
        messagebox.showerror(title="Error", message=f"Sorry no password saved {website}.")

    else:
        messagebox.showinfo(title=f"{website.capitalize()}", message=f"{website}\n Email: {data_found['email']}\n "
                                                                     f"Password: {data_found['password']}")
        email_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        email_entry.insert(0, f"{data_found['email']}")
        password_entry.insert(0, f"{data_found['password']}")


# -------------------UI----------------------------- #
main_window = Tk()
main_window.title("PasswordManager")
main_window.config(padx=50, pady=50, bg=YELLOW)
main_window.iconbitmap("systemlockscreen_104197.ico")

canvas = Canvas(width=256, height=256, highlightthickness=0, bg=YELLOW)
lock = PhotoImage(file="padlock.png")
canvas.create_image(128, 128, image=lock)
canvas.grid(column=1, row=1)

title_label = Label(text="PasswordManager", fg="#DD1616", bg=YELLOW, font=("Ariel", 22, "bold"), )
title_label.grid(column=1, row=0)

website_label = Label(text="Website:", bg="#DD1616",fg="white", width=13)
website_label.grid(column=0, row=2)

email_label = Label(text="Email/Username:", bg="#DD1616",fg="white", width=13)
email_label.grid(column=0, row=3)

password_label = Label(text="Password:", bg="#DD1616",fg="white", width=13)
password_label.grid(column=0, row=4)

website_entry = Entry(width=43)
website_entry.focus()
website_entry.grid(column=1, row=2)

email_entry = Entry(width=60)
email_entry.insert(0, string="@gmail.com")
email_entry.grid(column=1, row=3, columnspan=2)

password_entry = Entry(width=43)
password_entry.grid(column=1, row=4)

search_image = PhotoImage(file="search_button.png")
search_button = Button(image=search_image, bg="white", highlightthickness=0, command=search)
search_button.grid(column=2, row=2)

generate_image = PhotoImage(file="generate_pass.png")
password_button = Button(image=generate_image, highlightthickness=0, bg="white", command=password)
password_button.grid(column=2, row=4)

add_button = Button(width=36, text="Add", bg="#DD1616", command=save, fg="white")
add_button.grid(column=1, row=5)

main_window.mainloop()
