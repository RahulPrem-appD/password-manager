import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(index=0, string=password)
    messagebox.showinfo(title="Password Generated",
                        message="The password which you've created\n has copied to your clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) != 0 and len(email) != 0 and len(password) != 0 and email != "@gmail.com":
        is_ok = messagebox.askokcancel(title="Is everything Okay?",
                                       message=f"Theses are the details you've entered:\n"
                                               f"Website: {website}\nEmail: {email}\nPassword: {password}")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
                # updating old data with new data
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                email_entry.insert(index=0, string="@gmail.com")
                password_entry.delete(0, END)
    else:
        messagebox.showerror(title="Oops!!", message="Please don't leave any fields empty!")


# ---------------------------- SEARCH FUNCTION ------------------------------- #
def find_password():
    try:
        with open("data.json", "r") as data_file:
            # Reading old data
            data = json.load(data_file)
        messagebox.showinfo(title=f"{website_entry.get().title()} account details", message=f"Website:{website_entry.get()} "
                                              f"\nEmail/Username:{data[website_entry.get().title()]['email']}"
                                              f"\nPassword:{data[website_entry.get().title()]['password']}")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    except KeyError:
        messagebox.showerror(title="Error", message="NO details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(bg="white", padx=50, pady=50)
# ______________LOGO_______________ #
canvas = Canvas(height=200, width=200, highlightthickness=0, bg="white", )
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
# ______________LABELS_______________ #
website_title = Label(text="Website:", bg="white", font=('Arial', 11), padx=10, pady=10)
website_title.grid(row=1, column=0)
email_title = Label(text="Email/Username:", bg="white", font=('Arial', 11), padx=10, pady=10)
email_title.grid(row=2, column=0)
password_title = Label(text="Password:", bg="white", font=('Arial', 11), padx=10, pady=10)
password_title.grid(row=3, column=0)
# ______________ENTRIES_______________ #
website_entry = Entry(width=21, bg="white", font="Arial 11 normal")
website_entry.grid(row=1, column=1, ipady=3)
website_entry.focus()
email_entry = Entry(width=40, bg="white", font="Arial 11 normal")
email_entry.grid(row=2, column=1, columnspan=2, ipady=3, )
email_entry.insert(index=0, string="@gmail.com")
password_entry = Entry(width=21, bg="white", font="Arial 11 normal")
password_entry.grid(row=3, column=1, ipady=5)
# ______________BUTTONS_______________ #
generate_button = Button(width=15, text="Generate Password", bg="white", font="Arial 11 normal", border=1,
                         highlightthickness=0, command=generate)
generate_button.grid(row=3, column=2, padx=5, pady=5, ipady=3)
add_button = Button(width=36, text="Add", bg="white", font="Arial 11 normal", border=1,
                    highlightthickness=0, command=save)
add_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10, ipady=3)
search_button = Button(width=10, text="Search", bg="white", font="Arial 11 normal", border=1,
                       highlightthickness=0, command=find_password)
search_button.grid(row=1, column=2, padx=5, pady=5, ipady=3)

window.mainloop()
