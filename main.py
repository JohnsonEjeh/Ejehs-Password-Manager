from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def passwords():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_number = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_letters + password_number

    shuffle(password_list)

    password = "".join(password_list)
    entry_3.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    # new_line = f"{entry_1.get()}/ {entry_2.get()} / {entry_3.get()}\n"
    new_data = {
        entry_1.get(): {
            "email": entry_2.get(),
            "password": entry_3.get()
        }
    }
    if entry_2.get() == "" or entry_3.get() == "" or entry_1.get() == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")

    else:
        is_ok = messagebox.askokcancel(title=entry_1.get(), message=f"These are the details entered: \nEmail:"
                                                                    f" {entry_2} "f"\nPassword: {entry_2.get()} \n Is "
                                                                    f"it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data_r = json.load(file)
                    data_r.update(new_data)
            except json.decoder.JSONDecodeError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open("data.json", "w") as file:
                    json.dump(data_r, file, indent=4)
            finally:
                entry_1.delete(0, END)
                entry_3.delete(0, END)


def find_password():
    website = entry_1.get()
    try:
        with open("data.json") as file:
            read_file = json.load(file)
            w = read_file[website]

    except FileNotFoundError:
        messagebox.showinfo(text="Error", message="No Data File Found.")
    else:
        if entry_1.get() in read_file:
            messagebox.showinfo(title=entry_1.get(),
                                message=f"Email: {w['email']}\nPassword: {w['password']}")
        elif website == "":
            messagebox.showinfo(title="Error", message="Please type something to search")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=0)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

entry_1 = Entry(width=22)
entry_1.grid(row=1, column=1)
entry_1.focus()
entry_2 = Entry(width=42)
entry_2.insert(0, "Example@eg.com")
entry_2.grid(row=2, column=1, columnspan=2)
entry_3 = Entry(width=22)
entry_3.grid(row=3, column=1)

generate_password_button = Button(text="Generate PassWord", command=passwords, width=16)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", width=16, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
