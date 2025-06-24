from tkinter import *
import tkintermapview
import requests

# === LISTY DANYCH ===
grill_spots = []
users = []
reservations = []

# === KLASY ===
class GrillSpot:
    def __init__(self, name, city, description):
        self.name = name
        self.city = city
        self.description = description
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=f"{self.name}"
        )

    def get_coordinates(self) -> list:
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {'q': self.city, 'format': 'json'}
            headers = {'User-Agent': 'GrillApp/1.0 (kontakt@example.com)'}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return [lat, lon]
            else:
                raise ValueError("Nie znaleziono lokalizacji")

        except Exception as e:
            print(f"[Błąd pobierania współrzędnych OSM] {self.city}: {e}")
            return [52.23, 21.01]  # fallback: Warszawa

class User:
    def __init__(self, name, surname, email):
        self.name = name
        self.surname = surname
        self.email = email

class Reservation:
    def __init__(self, user: User, spot: GrillSpot, date: str):
        self.user = user
        self.spot = spot
        self.date = date

# === FUNKCJE ===
def add_grill_spot():
    name = entry_spot_name.get()
    city = entry_spot_city.get()
    desc = entry_spot_description.get()
    if not name or not city:
        return
    spot = GrillSpot(name, city, desc)
    grill_spots.append(spot)
    update_spot_list()
    entry_spot_name.delete(0, END)
    entry_spot_city.delete(0, END)
    entry_spot_description.delete(0, END)

def add_user():
    name = entry_user_name.get()
    surname = entry_user_surname.get()
    email = entry_user_email.get()
    if not name or not email:
        return
    user = User(name, surname, email)
    users.append(user)
    update_user_list()
    entry_user_name.delete(0, END)
    entry_user_surname.delete(0, END)
    entry_user_email.delete(0, END)

def make_reservation():
    user_index = listbox_users.curselection()
    spot_index = listbox_spots.curselection()
    date = entry_res_date.get()
    if not (user_index and spot_index and date):
        return
    user = users[user_index[0]]
    spot = grill_spots[spot_index[0]]
    reservations.append(Reservation(user, spot, date))
    update_reservation_list()
    entry_res_date.delete(0, END)

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
        listbox_reservations.insert(i, f"{r.user.name} -> {r.spot.name} ({r.date})")

# === GUI ===
root = Tk()
root.geometry("1200x800")
root.title("System Rezerwacji Miejsc do Grillowania")

# === Główna ramka formularzy ===
form_frame = Frame(root)
form_frame.pack(pady=10)

# === Sekcja: Miejsca ===
frame_spot_form = Frame(form_frame)
frame_spot_form.grid(row=0, column=0, padx=10, sticky="n")
Label(frame_spot_form, text="Dodaj miejsce").pack()
entry_spot_name = Entry(frame_spot_form)
entry_spot_name.pack()
entry_spot_name.insert(0, "Nazwa")

entry_spot_city = Entry(frame_spot_form)
entry_spot_city.pack()
entry_spot_city.insert(0, "Miasto")

entry_spot_description = Entry(frame_spot_form)
entry_spot_description.pack()
entry_spot_description.insert(0, "Opis")

Button(frame_spot_form, text="Dodaj miejsce", command=add_grill_spot).pack(pady=5)

frame_spot_list = Frame(form_frame)
frame_spot_list.grid(row=0, column=1, padx=10, sticky="n")
Label(frame_spot_list, text="Lista miejsc").pack()
listbox_spots = Listbox(frame_spot_list, height=8, width=30)
listbox_spots.pack()

# === Sekcja: Użytkownicy ===
frame_user_form = Frame(form_frame)
frame_user_form.grid(row=0, column=2, padx=10, sticky="n")
Label(frame_user_form, text="Dodaj użytkownika").pack()
entry_user_name = Entry(frame_user_form)
entry_user_name.pack()
entry_user_name.insert(0, "Imię")

entry_user_surname = Entry(frame_user_form)
entry_user_surname.pack()
entry_user_surname.insert(0, "Nazwisko")

entry_user_email = Entry(frame_user_form)
entry_user_email.pack()
entry_user_email.insert(0, "E-mail")

Button(frame_user_form, text="Dodaj użytkownika", command=add_user).pack(pady=5)

frame_user_list = Frame(form_frame)
frame_user_list.grid(row=0, column=3, padx=10, sticky="n")
Label(frame_user_list, text="Lista użytkowników").pack()
listbox_users = Listbox(frame_user_list, height=8, width=30)
listbox_users.pack()

# === Sekcja: Rezerwacje ===
frame_res_form = Frame(form_frame)
frame_res_form.grid(row=0, column=4, padx=10, sticky="n")
Label(frame_res_form, text="Dodaj rezerwację").pack()
entry_res_date = Entry(frame_res_form)
entry_res_date.pack()
entry_res_date.insert(0, "YYYY-MM-DD")

frame_res_list = Frame(form_frame)
frame_res_list.grid(row=0, column=5, padx=10, sticky="n")
Label(frame_res_list, text="Lista rezerwacji").pack()
listbox_reservations = Listbox(frame_res_list, height=8, width=40)
listbox_reservations.pack()

Button(frame_res_list, text="Zarezerwuj", command=make_reservation).pack(pady=5)

# === Mapa ===
map_widget = tkintermapview.TkinterMapView(root, width=1200, height=400)
map_widget.pack(pady=10)
map_widget.set_position(52.23, 21.01)
map_widget.set_zoom(6)

root.mainloop()
