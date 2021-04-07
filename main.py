from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as MessageBox
import mysql.connector as mysql
import matplotlib.pyplot as plt
import numpy as np
import datetime


####### pizza kezelés függvények #######


def pizza_formula(command, message):
    if e_pizza_name.get() == "" or e_size.get() == "" or e_price.get() == "":
        MessageBox.showinfo('INFO', "Minden mezőt kötelező kitölteni!")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute(command)
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', message)
            show_pizza(pizza_list)

        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_pizza_name.delete(0, 'end')
            e_size.delete(0, 'end')
            e_price.delete(0, 'end')
            con.close()


def insert_pizza():
    pizza_formula('insert into pizza values("{}", "{}", "{}")'.format(e_pizza_name.get(), e_size.get(), e_price.get()),
                  'Sikeres beszúrás')


def delete_pizza():
    pizza_formula(
        'delete from pizza where Név= "{}" and Méret = "{}" and Ár = "{}"'.format(e_pizza_name.get(), e_size.get(),
                                                                                  e_price.get()),
        'Törlés végrehajtva')


def price_update():
    pizza_formula(
        'update pizza set Ár="{}" where Név= "{}" and Méret = "{}"'.format(e_price.get(), e_pizza_name.get(),
                                                                           e_size.get()),
        'Ár frissítve')


def show_pizza(list):
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor()
    cursor.execute('select név from pizza group by név')
    rows = cursor.fetchall()
    list.delete(0, list.size())
    for row in rows:
        insertData = '{}'.format(row[0])
        list.insert(list.size() + 1, insertData)
    con.close()


####### pizza összetétel függvények #######

def select_and_search():
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor(buffered=True)

    if component_list.curselection():
        e_component.delete(0, 'end')
        state = component_list.get(tk.ANCHOR)
        e_component.insert(0, state)

    component_list.delete(0, component_list.size())

    cursor.execute('select * from feltét where név = "{}"'.format(e_component.get()))
    if cursor.rowcount != 0:
        rows = cursor.fetchall()
        for row in rows:
            insertData = '{}'.format(row[1])
            component_list.insert(component_list.size() + 1, insertData)

    cursor.execute('select * from feltét where feltét = "{}"'.format(e_component.get()))
    if cursor.rowcount != 0:
        rows = cursor.fetchall()
        for row in rows:
            insertData = '{}'.format(row[0])
            component_list.insert(component_list.size() + 1, insertData)

    con.close()


def back_pizza():
    e_component.delete(0, 'end')
    show_pizza(component_list)


####### felhasználó kezelő függvények #######


def user_formula(command, message):
    if e_user_name.get() == "" or e_email.get() == "" or e_name.get() == "" \
            or e_postcode == "" or e_street == "" or e_house == "":
        MessageBox.showinfo('INFO', "Minden mezőt ki kell tölteni!")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute(command)
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', message)
            show_user(user_list)

        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_user_name.delete(0, 'end')
            e_email.delete(0, 'end')
            e_name.delete(0, 'end')
            e_postcode.delete(0, 'end')
            e_street.delete(0, 'end')
            e_house.delete(0, 'end')
            con.close()


def insert_user():
    user_formula('insert into ügyfél(felhasználónév, email, név, irányítószám, utca, házszám) values("{}", "{}", '
                 '"{}", "{}", "{}", "{}")'.format(e_user_name.get(), e_email.get(), e_name.get(), e_postcode.get(),
                                                  e_street.get(), e_house.get()),
                 "Sikeres beszúrás")


def update_user():
    user_formula('update ügyfél set név = "{}", '
                 'irányítószám = "{}", utca = "{}", házszám = "{}" '
                 'where felhasználónév= "{}" and email = "{}"'.format(e_name.get(), e_postcode.get(), e_street.get(),
                                                                      e_house.get(),
                                                                      e_user_name.get(), e_email.get()),
                 "Felhasználó frissítve")


def delete_user():
    user_formula('delete from ügyfél where felhasználónév= "{}" and email = "{}" and név = "{}" and '
                 'irányítószám = "{}" and utca = "{}" and házszám = "{}"'.format(e_user_name.get(), e_email.get(),
                                                                                 e_name.get(),
                                                                                 e_postcode.get(), e_street.get(),
                                                                                 e_house.get()),
                 'Törlés végrehajtva')


def user_data():
    if not user_list.curselection():
        MessageBox.showinfo('INFO', "Válasszon ki egy felhasználót")
    else:
        e_user_name.delete(0, 'end')
        e_email.delete(0, 'end')
        e_name.delete(0, 'end')
        e_postcode.delete(0, 'end')
        e_street.delete(0, 'end')
        e_house.delete(0, 'end')

        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        cursor.execute('select * from ügyfél where felhasználónév = "{}"'.format(user_list.get(tk.ANCHOR)))
        row = cursor.fetchone()

        e_user_name.insert(0, row[0])
        e_email.insert(0, row[1])
        e_name.insert(0, row[2])
        e_postcode.insert(0, row[3])
        e_street.insert(0, row[4])
        e_house.insert(0, row[5])
        cursor.close()


def show_user(list):
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor()
    cursor.execute('select Felhasználónév from ügyfél')
    rows = cursor.fetchall()
    list.delete(0, list.size())
    for row in rows:
        insertData = '{}'.format(row[0])
        list.insert(list.size() + 1, insertData)
    con.close()


####### egy utcában laknak függvények #######


def home():
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor()

    if user_home_list.curselection():
        e_user_home.delete(0, 'end')
        state = user_home_list.get(tk.ANCHOR)
        e_user_home.insert(0, state)

    cursor.execute('select * from ügyfél where felhasználónév != "{}" and'
                   ' utca = (select utca from ügyfél where felhasználónév = "{}")'.format(e_user_home.get(),
                                                                                          e_user_home.get()))
    rows = cursor.fetchall()
    user_home_list.delete(0, 'end')
    for row in rows:
        insertData = '{}'.format(row[0])
        user_home_list.insert(user_home_list.size() + 1, insertData)
    con.close()


def back_user():
    e_user_home.delete(0, 'end')
    show_user(user_home_list)


####### rendelés kezelése függvények #######

def show_order():
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor()
    cursor.execute('select * from rendel order by rendelid')
    rows = cursor.fetchall()
    order_list.delete(0, order_list.size())
    for row in rows:
        insertData = '{}.{}-{} {}cm'.format(row[0], row[1], row[2], row[3])
        order_list.insert(order_list.size() + 1, insertData)
    con.close()


def insert_order():
    if e_orderid.get() == "" or e_order_pizza_name.get() == "" or e_order_pizza_name.get() == "" \
            or e_order_pizza_size.get() == "" or e_order_time.get() == "":
        MessageBox.showinfo('INFO', "Minden mezőt ki kell tölteni!")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute('insert into rendel(rendelid, felhasználónév, név, méret, mikor) values("{}", "{}", "{}", '
                           '"{}", "{}")'.format(e_orderid.get(), e_order_user_name.get(), e_order_pizza_name.get(),
                                                e_order_pizza_size.get(), e_order_time.get()))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', "Sikeres beszúrás")
            show_order()
        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_orderid.delete(0, 'end')
            e_order_user_name.delete(0, 'end')
            e_order_pizza_name.delete(0, 'end')
            e_order_pizza_size.delete(0, 'end')
            e_order_time.delete(0, 'end')
            con.close()


def update_order():
    if e_orderid.get() == "" or e_order_pizza_name.get() == "" or e_order_pizza_name.get() == "" \
            or e_order_pizza_size.get() == "" or e_order_time.get() == "":
        MessageBox.showinfo('INFO', "Minden mezőt ki kell tölteni!")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute('update rendel set felhasználónév = "{}", név = "{}", méret = "{}", mikor = "{}" '
                           'where rendelid="{}"'.format(e_order_user_name.get(), e_order_pizza_name.get(),
                                                        e_order_pizza_size.get(), e_order_time.get(), e_orderid.get()))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', "Rendelés frissítve")
            show_order()
        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_orderid.delete(0, 'end')
            e_order_user_name.delete(0, 'end')
            e_order_pizza_name.delete(0, 'end')
            e_order_pizza_size.delete(0, 'end')
            e_order_time.delete(0, 'end')
            con.close()


def delete_order():
    if e_orderid.get() == "":
        MessageBox.showinfo('INFO', "Adja meg a törölni kívánt rendelés ID-t")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute('delete from rendel where rendelid = "{}"'.format(e_orderid.get()))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', "Törlés végrehajtva")
            show_order()

        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_orderid.delete(0, 'end')
            e_order_user_name.delete(0, 'end')
            e_order_pizza_name.delete(0, 'end')
            e_order_pizza_size.delete(0, 'end')
            e_order_time.delete(0, 'end')
            con.close()


def order_data():
    if not order_list.curselection():
        MessageBox.showinfo('INFO', "Válasszon ki egy rendelést")
    else:
        e_orderid.delete(0, 'end')
        e_order_user_name.delete(0, 'end')
        e_order_pizza_name.delete(0, 'end')
        e_order_pizza_size.delete(0, 'end')
        e_order_time.delete(0, 'end')

        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        listitem = "{}".format(order_list.get(tk.ANCHOR))
        parts = listitem.split(".")
        cursor.execute('select * from rendel where rendelid = "{}"'.format(parts[0]))
        row = cursor.fetchone()

        e_orderid.insert(0, row[0])
        e_order_user_name.insert(0, row[1])
        e_order_pizza_name.insert(0, row[2])
        e_order_pizza_size.insert(0, row[3])
        e_order_time.insert(0, row[4])
        cursor.close()


####### statisztika függvények #######

def income():
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor(buffered=True)

    cursor.execute('select * from bevétel where nap > 22 and nap < 30')
    rows = cursor.fetchall()
    sum_ar = []
    nap = []
    for row in rows:
        sum_ar.append(int(row[0]))
        nap.append(row[1])

    ypos = np.arange(len(nap))
    days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']

    fig = plt.figure(figsize=(7, 5))
    fig.canvas.set_window_title("Heti bevétel diagram")

    plt.xticks(ypos, days)
    plt.ylabel("bevétel értéke(Ft)")
    plt.title("Az előző heti bevétel")

    plt.bar(ypos, sum_ar, color=['maroon', 'darkred', 'firebrick', 'indianred', 'lightcoral', 'lightpink', 'mistyrose'])

    plt.show()
    con.close()


def daily_comp():
    daily_comp_list.delete(0, daily_comp_list.size())

    if e_day.get() == "":
        MessageBox.showinfo('INFO', "Adj meg egy napot")
    else:
        try:
            datetime.datetime.strptime(e_day.get(), '%Y.%m.%d.')
        except ValueError:
            MessageBox.showinfo('INFO', "Hibás formátum! Helyesen: YYYY.MM.DD")
            return

        date = "{}".format(e_day.get()).split(".")

        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor(buffered=True)
        cursor.execute('select feltét, count(*) from feltét, rendel where feltét.név = rendel.név and '
                       'year(rendel.mikor) = "{}" and month(rendel.mikor) = "{}" and day(rendel.mikor) = "{}" '
                       'group by feltét order by feltét'.format(date[0], date[1], date[2]))
        rows = cursor.fetchall()
        for row in rows:
            insertData = '{}db   {}'.format(row[1], row[0])
            daily_comp_list.insert(daily_comp_list.size() + 1, insertData)
        con.close()

        cursor.close()


def daily_back():
    e_day.delete(0, 'end')
    daily_comp_list.delete(0, daily_comp_list.size())


####### szakácsok kezelése függvények #######

def show_cook():
    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor()
    cursor.execute('select * from szakacs order by szakácsid')
    rows = cursor.fetchall()
    cook_list.delete(0, cook_list.size())
    for row in rows:
        insertData = '{}'.format(row[1])
        cook_list.insert(cook_list.size() + 1, insertData)
    con.close()


def insert_cook():
    if e_cookid.get() == "" or e_cook_name.get() == "" or e_cook_pos.get() == "" \
            or e_cook_spec.get() == "":
        MessageBox.showinfo('INFO', "Minden mezőt ki kell tölteni!")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute('insert into szakacs(szakácsid, név, pozíció, specialitás) values("{}", "{}", "{}", '
                           '"{}")'.format(e_cookid.get(), e_cook_name.get(), e_cook_pos.get(),
                                          e_cook_spec.get()))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', "Sikeres beszúrás")
            show_cook()
        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_cookid.delete(0, 'end')
            e_cook_name.delete(0, 'end')
            e_cook_pos.delete(0, 'end')
            e_cook_spec.delete(0, 'end')
            con.close()


def update_cook():
    if e_cookid.get() == "" or e_cook_name.get() == "" or e_cook_pos.get() == "" \
            or e_cook_spec.get() == "":
        MessageBox.showinfo('INFO', "Minden mezőt ki kell tölteni!")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute('update szakacs set név = "{}", pozíció = "{}", specialitás = "{}" '
                           'where szakácsid="{}"'.format(e_cook_name.get(), e_cook_pos.get(), e_cook_spec.get(),
                                                         e_cookid.get()))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', "Adatok frissítve")
            show_cook()
        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_cookid.delete(0, 'end')
            e_cook_name.delete(0, 'end')
            e_cook_pos.delete(0, 'end')
            e_cook_spec.delete(0, 'end')
            con.close()


def delete_cook():
    if e_cookid.get() == "":
        MessageBox.showinfo('INFO', "Adja meg a törölni kívánt szakács ID-t")
    else:
        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        try:
            cursor.execute('delete from szakacs where szakácsid = "{}"'.format(e_cookid.get()))
            con.commit()
            if cursor.rowcount == 0:
                raise Exception()
            MessageBox.showinfo('INFO', "Törlés végrehajtva")
            show_cook()

        except:
            MessageBox.showerror('ERROR', "Hiba!")

        finally:
            e_cookid.delete(0, 'end')
            e_cook_name.delete(0, 'end')
            e_cook_pos.delete(0, 'end')
            e_cook_spec.delete(0, 'end')
            con.close()


def cook_data():
    if not cook_list.curselection():
        MessageBox.showinfo('INFO', "Válasszon ki egy szakácsot")
    else:
        e_cookid.delete(0, 'end')
        e_cook_name.delete(0, 'end')
        e_cook_pos.delete(0, 'end')
        e_cook_spec.delete(0, 'end')

        con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        cursor = con.cursor()
        cursor.execute('select * from szakacs where név = "{}"'.format(cook_list.get(tk.ANCHOR)))
        row = cursor.fetchone()

        e_cookid.insert(0, row[0])
        e_cook_name.insert(0, row[1])
        e_cook_pos.insert(0, row[2])
        e_cook_spec.insert(0, row[3])
        cursor.close()


def employee_of_the_month():
    e_cookid.delete(0, 'end')
    e_cook_name.delete(0, 'end')
    e_cook_pos.delete(0, 'end')
    e_cook_spec.delete(0, 'end')

    con = mysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
    cursor = con.cursor(buffered=True)

    cursor.execute('select szakacs.név, count(rendelid) from szakacs, rendel where szakacs.specialitás = rendel.név '
                   'and year(rendel.mikor) = 2020 and month(rendel.mikor) = 11 group by név order by count(rendelid) '
                   'desc')
    row = cursor.fetchone()

    MessageBox.showinfo('A hónap dolgozója', "Az előző hónap dolgozója {}, aki {} alkalommal készítette el a "
                                             "specialitását.".format(row[0], row[1]))
    con.close()


if __name__ == '__main__':
    dbhost = 'localhost'
    dbuser = 'pizzeria'
    dbpass = 'asd'
    dbname = 'pizzeria'

    root = tk.Tk()

    root.geometry("1600x600")
    root.title("Pizzéria adatbázis")
    root.iconbitmap('img/icon.ico')

    line = ttk.Separator(root).place(x=10, y=300, width=380)
    line2 = ttk.Separator(root).place(x=410, y=300, width=380)
    line3 = ttk.Separator(root).place(x=810, y=300, width=380)
    line4 = ttk.Separator(root).place(x=1210, y=300, width=380)
    line5 = ttk.Separator(root, orient=tk.VERTICAL).place(x=400, y=10, height=280)
    line6 = ttk.Separator(root, orient=tk.VERTICAL).place(x=800, y=10, height=280)
    line7 = ttk.Separator(root, orient=tk.VERTICAL).place(x=400, y=310, height=280)
    line8 = ttk.Separator(root, orient=tk.VERTICAL).place(x=800, y=310, height=280)
    line9 = ttk.Separator(root, orient=tk.VERTICAL).place(x=1200, y=10, height=280)
    line10 = ttk.Separator(root, orient=tk.VERTICAL).place(x=1200, y=310, height=280)

    quit_button = tk.Button(root, text="Kilépés", font=('italic', 10), bg="white", command=root.quit)
    quit_button.place(x=1100, y=550)

    ####### pizzák kezelése blokk #######

    pizza_title = tk.Label(root, text="Pizzák kezelése", font=('bold', 13))
    pizza_title.place(x=120, y=10)

    pizza_name = tk.Label(root, text="Név", font=('bold', 10))
    pizza_name.place(x=30, y=60)

    size = tk.Label(root, text="Méret", font=('bold', 10))
    size.place(x=30, y=100)

    price = tk.Label(root, text="Ár", font=('bold', 10))
    price.place(x=30, y=140)

    e_pizza_name = tk.Entry()
    e_pizza_name.place(x=110, y=60)

    e_size = tk.Entry()
    e_size.place(x=110, y=100)

    e_price = tk.Entry()
    e_price.place(x=110, y=140)

    insert_pizza_button = tk.Button(root, text="Beszúrás", font=('italic', 10), bg="white", command=insert_pizza)
    insert_pizza_button.place(x=30, y=200)

    update_pizza_button = tk.Button(root, text="Ár Frissít", font=('italic', 10), bg="white", command=price_update)
    update_pizza_button.place(x=110, y=200)

    delete_pizza_button = tk.Button(root, text="Töröl", font=('italic', 10), bg="white", command=delete_pizza)
    delete_pizza_button.place(x=190, y=200)

    pizza_list = tk.Listbox(root)
    pizza_list.place(x=260, y=50)
    show_pizza(pizza_list)

    ####### pizzák összetétele blokk #######

    component_title = tk.Label(root, text="Pizza összetétele", font=('bold', 13))
    component_title.place(x=120, y=320)

    e_component = tk.Entry()
    e_component.place(x=90, y=360)

    search_button = tk.Button(root, text="Keresés", font=('italic', 10), bg="white", command=select_and_search)
    search_button.place(x=240, y=355)

    back_pizza_button = tk.Button(root, text="Vissza", font=('italic', 10), bg="white", command=back_pizza)
    back_pizza_button.place(x=310, y=355)

    component_list = tk.Listbox(root)
    component_list.place(x=120, y=400)
    show_pizza(component_list)

    ####### ügyfelek kezelése blokk #######

    user_title = tk.Label(root, text="Felhasználók kezelése", font=('bold', 13))
    user_title.place(x=520, y=10)

    user_name = tk.Label(root, text="Felhasználónév", font=('bold', 10))
    user_name.place(x=420, y=50)

    email = tk.Label(root, text="Email", font=('bold', 10))
    email.place(x=420, y=80)

    name = tk.Label(root, text="Név", font=('bold', 10))
    name.place(x=420, y=110)

    postcode = tk.Label(root, text="Irányítószám", font=('bold', 10))
    postcode.place(x=420, y=140)

    street = tk.Label(root, text="Utca", font=('bold', 10))
    street.place(x=420, y=170)

    house = tk.Label(root, text="Házszám", font=('bold', 10))
    house.place(x=420, y=200)

    e_user_name = tk.Entry()
    e_user_name.place(x=520, y=50)

    e_email = tk.Entry()
    e_email.place(x=520, y=80)

    e_name = tk.Entry()
    e_name.place(x=520, y=110)

    e_postcode = tk.Entry()
    e_postcode.place(x=520, y=140)

    e_street = tk.Entry()
    e_street.place(x=520, y=170)

    e_house = tk.Entry()
    e_house.place(x=520, y=200)

    insert_user_button = tk.Button(root, text="Beszúrás", font=('italic', 10), bg="white", command=insert_user)
    insert_user_button.place(x=430, y=250)

    update_user_button = tk.Button(root, text="Felhasználó frissít", font=('italic', 10), bg="white",
                                   command=update_user)
    update_user_button.place(x=510, y=250)

    delete_user_button = tk.Button(root, text="Töröl", font=('italic', 10), bg="white", command=delete_user)
    delete_user_button.place(x=640, y=250)

    user_data_button = tk.Button(root, text="Mutat", font=('italic', 10), bg="white", command=user_data)
    user_data_button.place(x=695, y=250)

    user_list = tk.Listbox(root)
    user_list.place(x=660, y=50)
    show_user(user_list)

    ####### egy utcában lakó ügyfelek #######

    e_user_home = tk.Entry()
    e_user_home.place(x=540, y=330)

    home_button = tk.Button(root, text="Ki lakik még az utcában?", font=('italic', 10), bg="white", command=home)
    home_button.place(x=460, y=365)

    back_user_button = tk.Button(root, text="Vissza", font=('italic', 10), bg="white", command=back_user)
    back_user_button.place(x=640, y=365)

    user_home_list = tk.Listbox(root)
    user_home_list.place(x=540, y=410)
    show_user(user_home_list)

    ####### rendelések kezelése blokk #######

    order_title = tk.Label(root, text="Rendelések kezelése", font=('bold', 13))
    order_title.place(x=920, y=10)

    orderid = tk.Label(root, text="ID", font=('bold', 10))
    orderid.place(x=825, y=50)

    order_user_name = tk.Label(root, text="Felhasználónév", font=('bold', 10))
    order_user_name.place(x=825, y=85)

    order_pizza_name = tk.Label(root, text="Pizza név", font=('bold', 10))
    order_pizza_name.place(x=825, y=120)

    order_pizza_size = tk.Label(root, text="Méret", font=('bold', 10))
    order_pizza_size.place(x=825, y=155)

    order_time = tk.Label(root, text="Idő", font=('bold', 10))
    order_time.place(x=825, y=190)

    e_orderid = tk.Entry()
    e_orderid.place(x=925, y=50)

    e_order_user_name = tk.Entry()
    e_order_user_name.place(x=925, y=85)

    e_order_pizza_name = tk.Entry()
    e_order_pizza_name.place(x=925, y=120)

    e_order_pizza_size = tk.Entry()
    e_order_pizza_size.place(x=925, y=155)

    e_order_time = tk.Entry()
    e_order_time.place(x=925, y=190)

    insert_user_button = tk.Button(root, text="Beszúrás", font=('italic', 10), bg="white", command=insert_order)
    insert_user_button.place(x=820, y=250)

    update_user_button = tk.Button(root, text="Rendelés frissít", font=('italic', 10), bg="white",
                                   command=update_order)
    update_user_button.place(x=900, y=250)

    delete_user_button = tk.Button(root, text="Töröl", font=('italic', 10), bg="white", command=delete_order)
    delete_user_button.place(x=1020, y=250)

    order_data_button = tk.Button(root, text="Mutat", font=('italic', 10), bg="white", command=order_data)
    order_data_button.place(x=1075, y=250)

    order_list = tk.Listbox(root)
    order_list.place(x=1060, y=50)
    show_order()

    ####### statisztika #######

    stat_title = tk.Label(root, text="Statisztikák", font=('bold', 13))
    stat_title.place(x=950, y=310)

    # adott nap felhasznált összetevők

    day_title = tk.Label(root, text="Nap", font=('bold', 10))
    day_title.place(x=840, y=400)

    e_day = tk.Entry()
    e_day.place(x=900, y=400)

    daily_comp_button = tk.Button(root, text="Keresés", font=('italic', 10), bg="white", command=daily_comp)
    daily_comp_button.place(x=900, y=440)

    daily_back_button = tk.Button(root, text="Vissza", font=('italic', 10), bg="white", command=daily_back)
    daily_back_button.place(x=970, y=440)

    comp_list_title = tk.Label(root, text="Felhasznált összetevők", font=('bold', 10))
    comp_list_title.place(x=1050, y=325)

    daily_comp_list = tk.Listbox(root)
    daily_comp_list.place(x=1060, y=350)

    # heti bevétel

    income_title = tk.Label(root, text="Heti bevétel", font=('bold', 10))
    income_title.place(x=840, y=540)

    income_button = tk.Button(root, text="Mutat", font=('italic', 10), bg="white", command=income)
    income_button.place(x=950, y=536)

    ####### szakácsok kezelése blokk #######

    cook_title = tk.Label(root, text="Szakácsok kezelése", font=('bold', 13))
    cook_title.place(x=1300, y=10)

    cookid = tk.Label(root, text="SzakácsID", font=('bold', 10))
    cookid.place(x=1207, y=60)

    cook_name = tk.Label(root, text="Név", font=('bold', 10))
    cook_name.place(x=1207, y=100)

    cook_pos = tk.Label(root, text="Pozíció", font=('bold', 10))
    cook_pos.place(x=1207, y=140)

    cook_spec = tk.Label(root, text="Specialitás", font=('bold', 10))
    cook_spec.place(x=1207, y=180)

    insert_cook_button = tk.Button(root, text="Beszúrás", font=('italic', 10), bg="white", command=insert_cook)
    insert_cook_button.place(x=1220, y=225)

    update_cook_button = tk.Button(root, text="Adatokat frissít", font=('italic', 10), bg="white",
                                   command=update_cook)
    update_cook_button.place(x=1300, y=225)

    delete_cook_button = tk.Button(root, text="Töröl", font=('italic', 10), bg="white", command=delete_cook)
    delete_cook_button.place(x=1420, y=225)

    cook_data_button = tk.Button(root, text="Mutat", font=('italic', 10), bg="white", command=cook_data)
    cook_data_button.place(x=1475, y=225)

    emp_of_the_month_button = tk.Button(root, text="A hónap dolgozója", font=('italic', 10), bg="white", command=employee_of_the_month)
    emp_of_the_month_button.place(x=1315, y=260)

    e_cookid = tk.Entry()
    e_cookid.place(x=1275, y=60)

    e_cook_name = tk.Entry()
    e_cook_name.place(x=1275, y=100)

    e_cook_pos = tk.Entry()
    e_cook_pos.place(x=1275, y=140)

    e_cook_spec = tk.Entry()
    e_cook_spec.place(x=1275, y=180)

    cook_list = tk.Listbox(root)
    cook_list.place(x=1405, y=50)
    show_cook()

    made_title = tk.Label(root, text="Készítette: Süli Tamara (ILQAHJ)", font=('bold', 10))
    made_title.place(x=1320, y=550)

    root.mainloop()
