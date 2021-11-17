import webbrowser
from tkinter import *
from bs4 import BeautifulSoup
import requests
import os
from sqlalchemy.orm import sessionmaker
from produktas import engine, Produktas  # tablenamas o darbuotojas = darbuotojas.py failas

Session = sessionmaker(bind=engine)
session = Session()

win = Tk()

win.geometry = "920x550"
win.minsize(920, 550)
win.maxsize(920, 550)
win.title("BARBORA NOTEBOOK 2021")
icon = PhotoImage(file="barb.png")
win.iconphoto(True, icon)
bg = PhotoImage(file="bg.png")

my_canvas = Canvas(win, width=920, height=550)
my_canvas.pack(fill="both", expand=True)  # su (args)
my_canvas.create_image(0, 0, image=bg, anchor='nw')

SAVE_FOLDER = "Nuotraukos"
linku_listas = []
prekiu_listas = []


def callback(url):
    try:
        webbrowser.open_new(url)
    except requests.exceptions.MissingSchema:
        print("Tuscias URL Inputas")


def add_item():
    try:
        my_list_box.delete('0', END)
        m_likas = entry1.get()
        print(m_likas)
        linkas = requests.get(m_likas).text
        soup = BeautifulSoup(linkas, 'html.parser')
        visas_pavadinimas = soup.find('h1', class_="b-product-info--title").text.strip()
        trumpas_pavadinimas = visas_pavadinimas.split(" ")[0]

        prekiu_listas.append(trumpas_pavadinimas)

        # blokas = soup.find('div', class_="b-product-prices-block")

        kaina = soup.find("span", class_="b-product-price-current-number").text.strip()
        print(kaina)

        result = True

        while result:
            try:
                akcija = soup.find("del", class_="b-product-crossed-out-price").text.strip()
                print(akcija)
                print("yra akcija")
                break

            except AttributeError:
                result = False
                print("nera akcijos")

        foto_linkas = soup.div.img['src']
        linku_listas.append(foto_linkas)

        print("start downloading ...")

        if not os.path.exists(SAVE_FOLDER):
            os.mkdir(SAVE_FOLDER)

        for photo_linkas in linku_listas:
            response = requests.get(photo_linkas)

            image_name = SAVE_FOLDER + "/" + visas_pavadinimas + '.png'
            with open(image_name, 'wb') as file:
                file.write(response.content)

        my_list_box.config(fg="#002a76")

        print("done")

        produktas = Produktas(visas_pavadinimas, kaina, result)
        session.add(produktas)
        session.commit()

        produktu_listas = []
        produktai = session.query(Produktas).all()  # Table name
        for produktas in produktai:
            produktu_listas.append(produktas)

        for item in produktu_listas:
            my_list_box.insert(END, item)

        print("done downloading images")

        # entry1.delete('0', END)
    except requests.exceptions.MissingSchema:
        print("Tuscias URL Inputas || netinkamas URL")


def uzkrauti_prekes():
    my_list_box.delete('0', END)

    produktu_listas = []
    produktai = session.query(Produktas).all()  # Table name
    for produktas in produktai:
        produktu_listas.append(produktas)

    for item in produktu_listas:  # tiesiai is database imame data ir listo pavidalu printinam
        my_list_box.insert(END, item)

    my_list_box.config(fg="#002a76")


def istrinti_preke():
    while True:
        try:
            pirmas = my_list_box.get(ANCHOR).split()  # Split !!! Anchor kur paspausta
            idi = pirmas[0]

            print(pirmas)
            print(idi)

            trinamas_id = int(idi)
            trinamas_produktas = session.query(Produktas).get(trinamas_id)
            session.delete(trinamas_produktas)
            session.commit()

            my_list_box.delete(ANCHOR)
            break

        except IndexError:
            my_list_box.delete('0', END)
            my_list_box.insert(END, "Klaida ! Nepazimetas produktas")  # \n ??
            my_list_box.config(fg="Red")
            break

##  barbora.lt linkas
browser = PhotoImage(file="barl.png")
br_button = Button(win, image=browser, relief=FLAT, bg='#ebebeb', cursor="hand2")  # command=callback() <-- nereikia
br_button.bind("<Button-1>", lambda a: callback("https://barbora.lt/"))
br_button_window = my_canvas.create_window(15, 10, anchor="nw", window=br_button)

##  Top
butt1 = Button(win, text="ADD", width=9, fg="#001c5b", activeforeground="Grey", font=("Calibri Bold", 10), bd=3,
               command=add_item)
butt1_window = my_canvas.create_window(910, 90, anchor="ne", window=butt1)

entry1 = Entry(win, font=("Calibri Bold", 12), text="Link", width=100, fg="#002a76", bg="#e1e1e1",
               insertbackground='#002a76')
entry1_window = my_canvas.create_window(20, 91, anchor="nw", window=entry1)

##  Bottom
butt2 = Button(win, text="LOAD", width=9, fg="#001c5b", activeforeground="Grey", font=("Calibri Bold", 10), bd=3,
               command=uzkrauti_prekes)
butt2_window = my_canvas.create_window(910, 181, anchor="ne", window=butt2)

butt3 = Button(win, text="DEL", width=9, fg="red", activeforeground="Grey", font=("Calibri Bold", 10), bd=3,
               command=istrinti_preke)
butt3_window = my_canvas.create_window(910, 211, anchor="ne", window=butt3)

my_list_box = Listbox(win, width=100, height=17, selectmode=SINGLE, fg="#002a76", bg="#e1e1e1",
                      font=("Calibri Bold", 12))

my_list_box1_window = my_canvas.create_window(823, 180, anchor="ne", window=my_list_box)
################################################################################################################

# path = r'C:\Users\al_man\PycharmProjects\Barbora\'
# foto_area = PhotoImage(file='ban.png')
# my_canvas.create_image(5, 235, image=foto_area, anchor='nw')

##############################################################################################################
win.mainloop()
# print(os.getcwd())
