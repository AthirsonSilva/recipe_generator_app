""" A simple tkinter and sqlite3 app """

import sqlite3
from tkinter import Frame, Label, Button, Tk
from PIL import ImageTk
from numpy import random


def clear_widgets(window_frame):
    """ destroys other frames to suppress window collision

    Args:
        window_frame (Frame): the window frames
    """

    for widget in window_frame.winfo_children():
        widget.destroy()

def fetch_db():
    """ fetchs the sqlite3 database data
    """

    conn = sqlite3.connect('data/recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table';")
    all_tables = cursor.fetchall()

    idx = random.randint(0, len(all_tables) - 1)
    table_name = all_tables[idx][1]
    cursor.execute(f"SELECT * FROM {table_name};")
    table_records = cursor.fetchall()

    conn.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    """pre_processing the data from the database

    Args:
        table_name (str): the name of the table
        table_records (str): all the database's tables
    """

    title = table_name[:-6]
    title = "".join([char if char.islower() else f" {char}" for char in title])

    ingredients = []

    # ingredients
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)

    return title, ingredients

def load_first_frame():
    """ first_frame widgets
    """

    clear_widgets(second_frame)

    first_frame.tkraise()
    first_frame.propagate(False)
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = Label(first_frame, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack()

    Label(
        first_frame,
        text='Ready for your random recipe?',
        bg=BG_COLOR,
        fg='white',
        font=('TkMenuFont', 14)
    ).pack()

    Button(
        first_frame,
        text='SHUFFLE',
        font=('TkHeadingFont', 20),
        bg='#28393a',
        fg='white',
        cursor='hand2',
        activebackground='#badee2',
        activeforeground='black',
        command=load_second_frame
    ).pack(pady=35)


def load_second_frame():
    """  Says hello
    """

    clear_widgets(first_frame)
    second_frame.tkraise()

    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = Label(second_frame, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    Label(
        second_frame,
        text='Ready for your random recipe?',
        bg=BG_COLOR,
        fg='white',
        font=('TkHeadingFont', 20)
    ).pack(pady=25)

    for i in ingredients:
        Label(
            second_frame,
            text=i,
            bg=BG_COLOR,
            fg='white',
            font=('TkMenuFont', 12)
        ).pack(fill='both')

    Button(
        second_frame,
        text='BACK',
        font=('TkHeadingFont', 20),
        bg='#28393a',
        fg='white',
        cursor='hand2',
        activebackground='#badee2',
        activeforeground='black',
        command=load_first_frame
    ).pack(pady=35)


BG_COLOR = '#3d6466'

# initiallize app
root = Tk()
root.title("Recipe picker")
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)

first_frame = Frame(root, width=600, height=600, bg=BG_COLOR)
second_frame = Frame(root, bg=BG_COLOR)

for frame in (first_frame, second_frame):
    frame.grid(row=0, column=0, sticky='newsw')


load_first_frame()

# run app
root.mainloop()
