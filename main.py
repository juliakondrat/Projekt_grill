from tkinter import *
from tkinter import messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# === LISTY DANYCH ===
grill_spots = []
users = []
reservations = []

# === ROOT I MAPA ===
root = Tk()
root.geometry("1200x900")
root.title("System Rezerwacji Terminów i Miejsc do Grillowania")

map_widget = tkintermapview.TkinterMapView(root, width=1200, height=300)
map_widget.pack(pady=10)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)

# === KLASY ===
def get_city_description(city):
    try:
        url = f"https://pl.wikipedia.org/wiki/{city}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.select("div.mw-parser-output > p")
        for para in paragraphs:
            if para.text.strip():
                return para.text.strip()
        return "Brak opisu."
    except Exception as e:
        print(f"Nie udało się pobrać opisu: {e}")
        return "Nie udało się pobrać opisu."

def get_city_image_url(city):
    try:
        url = f"https://pl.wikipedia.org/wiki/{city}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        infobox = soup.find("table", class_="infobox")
        if infobox:
            img = infobox.find("img")
            if img:
                return "https:" + img['src']
    except Exception as e:
        print(f"Nie udało się pobrać zdjęcia: {e}")
    return None

class GrillSpot:
    def __init__(self, name, city, description):
        self.name = name
        self.city = city
        self.description = description
        self.coordinates = self.get_coordinates()
        self.description_text = get_city_description(self.city)
        self.image_url = get_city_image_url(self.city)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f"{self.name} - {self.city}")

    def get_coordinates(self):
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {'q': self.city, 'format': 'json'}
            headers = {'User-Agent': 'GrillApp/1.0 (kontakt@example.com)'}
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            if data:
                return [float(data[0]['lat']), float(data[0]['lon'])]
        except Exception as e:
            print(f"Błąd pobierania lokalizacji: {e}")
        return [52.23, 21.01]

class User:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email

class Reservation:
    def __init__(self, date):
        self.date = date

# === FUNKCJE ===
def update_spot_list():
    listbox_spots.delete(0, END)
    for i, s in enumerate(grill_spots):
        listbox_spots.insert(i, f"{s.name} ({s.city})")

def update_user_list():
    listbox_users.delete(0, END)
    for i, u in enumerate(users):
        listbox_users.insert(i, f"{u.name} {u.surname}")

def update_reservation_list():
    listbox_reservations.delete(0, END)
    for i, r in enumerate(reservations):
        listbox_reservations.insert(i, f"Data: {r.date}")

def clear_placeholder(event):
    if entry_res_date.get() == "YYYY-MM-DD":
        entry_res_date.delete(0, END)

def show_city_description(event):
    selection = listbox_spots.curselection()
    if not selection:
        return
    index = selection[0]
    spot = grill_spots[index]
    label_city_description.config(text=f"Opis miasta:\n{spot.description_text}")

    if spot.image_url:
        try:
            image_response = requests.get(spot.image_url)
            image_data = image_response.content
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((200, 150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            label_city_image.config(image=photo)
            label_city_image.image = photo
        except Exception as e:
            print(f"Nie udało się załadować obrazka: {e}")
            label_city_image.config(image='')
    else:
        label_city_image.config(image='')

# === UŻYTKOWNICY ===
def add_user():
    name = entry_user_name.get()
    surname = entry_user_surname.get()
    email = entry_user_email.get()
    if not name or not email:
        return
    users.append(User(name, surname, email))
    update_user_list()
    entry_user_name.delete(0, END)
    entry_user_surname.delete(0, END)
    entry_user_email.delete(0, END)

def edit_user():
    selection = listbox_users.curselection()
    if not selection:
        return
    index = selection[0]
    user = users[index]
    entry_user_name.delete(0, END)
    entry_user_name.insert(0, user.name)
    entry_user_surname.delete(0, END)
    entry_user_surname.insert(0, user.surname)
    entry_user_email.delete(0, END)
    entry_user_email.insert(0, user.email)
    button_add_user.config(text="Zapisz użytkownika", command=lambda: save_edited_user(index))

def save_edited_user(index):
    name = entry_user_name.get()
    surname = entry_user_surname.get()
    email = entry_user_email.get()
    users[index] = User(name, surname, email)
    update_user_list()
    entry_user_name.delete(0, END)
    entry_user_surname.delete(0, END)
    entry_user_email.delete(0, END)
    button_add_user.config(text="Dodaj użytkownika", command=add_user)

# === MIEJSCA ===
def add_grill_spot():
    name = entry_spot_name.get()
    city = entry_spot_city.get()
    desc = entry_spot_description.get()
    if not name or not city:
        return
    grill_spots.append(GrillSpot(name, city, desc))
    update_spot_list()
    entry_spot_name.delete(0, END)
    entry_spot_city.delete(0, END)
    entry_spot_description.delete(0, END)

def edit_grill_spot():
    selection = listbox_spots.curselection()
    if not selection:
        return
    index = selection[0]
    spot = grill_spots[index]
    entry_spot_name.delete(0, END)
    entry_spot_name.insert(0, spot.name)
    entry_spot_city.delete(0, END)
    entry_spot_city.insert(0, spot.city)
    entry_spot_description.delete(0, END)
    entry_spot_description.insert(0, spot.description)
    button_add_spot.config(text="Zapisz miejsce", command=lambda: save_edited_grill_spot(index))

def save_edited_grill_spot(index):
    name = entry_spot_name.get()
    city = entry_spot_city.get()
    desc = entry_spot_description.get()
    grill_spots[index] = GrillSpot(name, city, desc)
    update_spot_list()
    entry_spot_name.delete(0, END)
    entry_spot_city.delete(0, END)
    entry_spot_description.delete(0, END)
    button_add_spot.config(text="Dodaj miejsce", command=add_grill_spot)

# === REZERWACJE  ===
def make_reservation():
    date = entry_res_date.get().strip()
    if not date:
        messagebox.showwarning("Brak danych", "Wpisz datę!")
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Niepoprawna data", "Format RRRR-MM-DD!")
        return
    reservations.append(Reservation(date))
    update_reservation_list()
    entry_res_date.delete(0, END)

def edit_reservation():
    selection = listbox_reservations.curselection()
    if not selection:
        return
    index = selection[0]
    res = reservations[index]
    entry_res_date.delete(0, END)
    entry_res_date.insert(0, res.date)
    button_reserve.config(text="Zapisz rezerwację", command=lambda: save_edited_reservation(index))

def save_edited_reservation(index):
    date = entry_res_date.get().strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Błąd", "Format daty to RRRR-MM-DD!")
        return
    reservations[index] = Reservation(date)
    update_reservation_list()
    entry_res_date.delete(0, END)
    button_reserve.config(text="Zarezerwuj", command=make_reservation)

def delete_reservation():
    selection = listbox_reservations.curselection()
    if not selection:
        return
    del reservations[selection[0]]
    update_reservation_list()

# === GUI ===
form_frame = Frame(root)
form_frame.pack(pady=10)

# --- UŻYTKOWNICY ---
user_frame = LabelFrame(form_frame, text="Użytkownicy")
user_frame.grid(row=0, column=0, padx=10)

entry_user_name = Entry(user_frame)
entry_user_name.pack()
entry_user_name.insert(0, "Imię")

entry_user_surname = Entry(user_frame)
entry_user_surname.pack()
entry_user_surname.insert(0, "Nazwisko")

entry_user_email = Entry(user_frame)
entry_user_email.pack()
entry_user_email.insert(0, "E-mail")

button_add_user = Button(user_frame, text="Dodaj użytkownika", command=add_user)
button_add_user.pack()
Button(user_frame, text="Edytuj użytkownika", command=edit_user).pack()

listbox_users = Listbox(user_frame, height=8, width=30)
listbox_users.pack()

# --- MIEJSCA ---
spot_frame = LabelFrame(form_frame, text="Miejsca do grillowania")
spot_frame.grid(row=0, column=1, padx=10)

entry_spot_name = Entry(spot_frame)
entry_spot_name.pack()
entry_spot_name.insert(0, "Nazwa miejsca")

entry_spot_city = Entry(spot_frame)
entry_spot_city.pack()
entry_spot_city.insert(0, "Miasto")

entry_spot_description = Entry(spot_frame)
entry_spot_description.pack()
entry_spot_description.insert(0, "Opis")

button_add_spot = Button(spot_frame, text="Dodaj miejsce", command=add_grill_spot)
button_add_spot.pack()
Button(spot_frame, text="Edytuj miejsce", command=edit_grill_spot).pack()

listbox_spots = Listbox(spot_frame, height=8, width=30)
listbox_spots.pack()
listbox_spots.bind("<<ListboxSelect>>", show_city_description)

label_city_description = Label(spot_frame, text="Opis miasta: ", wraplength=250, justify=LEFT)
label_city_description.pack(pady=5)

label_city_image = Label(spot_frame)
label_city_image.pack(pady=5)

# --- REZERWACJE ---
res_frame = LabelFrame(form_frame, text="Rezerwacje")
res_frame.grid(row=0, column=2, padx=10)

entry_res_date = Entry(res_frame)
entry_res_date.pack()
entry_res_date.insert(0, "YYYY-MM-DD")
entry_res_date.bind("<FocusIn>", clear_placeholder)

button_reserve = Button(res_frame, text="Zarezerwuj", command=make_reservation)
button_reserve.pack()
Button(res_frame, text="Edytuj", command=edit_reservation).pack()
Button(res_frame, text="Usuń", command=delete_reservation).pack()

listbox_reservations = Listbox(res_frame, height=8, width=30)
listbox_reservations.pack()

# === Start ===
root.mainloop()
