from tkinter import *
import tkintermapview

# **ZMIANA nazwy listy z `users` na `grill_spots`**
grill_spots: list = []

# **ZMIANA nazwy klasy z `User` na `GrillSpot`**
class GrillSpot:
    def __init__(self, name, city, description, reserved):
        self.name = name
        self.city = city
        self.description = description
        self.reserved = reserved
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=f"{self.name} ({'Zajęte' if self.reserved else 'Wolne'})"
        )

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.'))
        ]


def add_grill_spot() -> None:
    name = entry_name.get()
    city = entry_city.get()
    description = entry_description.get()
    reserved = var_reserved.get()

    grill_spot = GrillSpot(name, city, description, reserved)
    grill_spots.append(grill_spot)

    print(grill_spots)

    entry_name.delete(0, END)
    entry_city.delete(0, END)
    entry_description.delete(0, END)
    var_reserved.set(False)
    entry_name.focus()
    show_grill_spots()


def show_grill_spots():
    listbox_spots.delete(0, END)
    for idx, spot in enumerate(grill_spots):
        listbox_spots.insert(idx, f"{idx+1}. {spot.name} ({'Zajęte' if spot.reserved else 'Wolne'})")


def remove_grill_spot():
    i = listbox_spots.index(ACTIVE)
    grill_spots[i].marker.delete()
    grill_spots.pop(i)
    show_grill_spots()


def edit_grill_spot():
    i = listbox_spots.index(ACTIVE)
    entry_name.insert(0, grill_spots[i].name)
    entry_city.insert(0, grill_spots[i].city)
    entry_description.insert(0, grill_spots[i].description)
    var_reserved.set(grill_spots[i].reserved)

    button_add.configure(text="Zapisz", command=lambda: update_grill_spot(i))


def update_grill_spot(i):
    name = entry_name.get()
    city = entry_city.get()
    description = entry_description.get()
    reserved = var_reserved.get()

    grill_spots[i].name = name
    grill_spots[i].city = city
    grill_spots[i].description = description
    grill_spots[i].reserved = reserved

    grill_spots[i].coordinates = grill_spots[i].get_coordinates()
    grill_spots[i].marker.delete()
    grill_spots[i].marker = map_widget.set_marker(
        grill_spots[i].coordinates[0], grill_spots[i].coordinates[1],
        text=f"{grill_spots[i].name} ({'Zajęte' if grill_spots[i].reserved else 'Wolne'})"
    )

    show_grill_spots()
    button_add.configure(text='Dodaj', command=add_grill_spot)

    entry_name.delete(0, END)
    entry_city.delete(0, END)
    entry_description.delete(0, END)
    var_reserved.set(False)
    entry_name.focus()


def show_grill_spot_detail():
    i = listbox_spots.index(ACTIVE)
    label_detail_name_value.config(text=grill_spots[i].name)
    label_detail_city_value.config(text=grill_spots[i].city)
    label_detail_description_value.config(text=grill_spots[i].description)
    label_detail_reserved_value.config(text="Zajęte" if grill_spots[i].reserved else "Wolne")

    map_widget.set_zoom(15)
    map_widget.set_position(grill_spots[i].coordinates[0], grill_spots[i].coordinates[1])


root = Tk()
root.geometry("1200x700")
root.title('System Rezerwacji Miejsc do Grillowania')

# **ZMIANA nazw ramek GUI**
frame_list = Frame(root)
frame_form = Frame(root)
frame_details = Frame(root)
frame_map = Frame(root)

frame_list.grid(row=0, column=0)
frame_form.grid(row=0, column=1)
frame_details.grid(row=1, column=0, columnspan=2)
frame_map.grid(row=2, column=0, columnspan=2)

# **Sekcja LISTA MIEJSC**
Label(frame_list, text='Lista miejsc do grillowania:').grid(row=0, column=0)

listbox_spots = Listbox(frame_list, width=50, height=10)
listbox_spots.grid(row=1, column=0, columnspan=3)

Button(frame_list, text='Szczegóły', command=show_grill_spot_detail).grid(row=2, column=0)
Button(frame_list, text='Usuń', command=remove_grill_spot).grid(row=2, column=1)
Button(frame_list, text='Edytuj', command=edit_grill_spot).grid(row=2, column=2)

# **Sekcja FORMULARZ**
Label(frame_form, text='Formularz nowego miejsca:').grid(row=0, column=0, sticky=W)
Label(frame_form, text='Nazwa miejsca:').grid(row=1, column=0, sticky=W)
Label(frame_form, text='Miasto:').grid(row=2, column=0, sticky=W)
Label(frame_form, text='Opis:').grid(row=3, column=0, sticky=W)
Label(frame_form, text='Zarezerwowane:').grid(row=4, column=0, sticky=W)

entry_name = Entry(frame_form)
entry_name.grid(row=1, column=1)

entry_city = Entry(frame_form)
entry_city.grid(row=2, column=1)

entry_description = Entry(frame_form)
entry_description.grid(row=3, column=1)

var_reserved = BooleanVar()
checkbox_reserved = Checkbutton(frame_form, variable=var_reserved)
checkbox_reserved.grid(row=4, column=1)

button_add = Button(frame_form, text='Dodaj', command=add_grill_spot)
button_add.grid(row=5, column=0, columnspan=2)

# **Sekcja SZCZEGÓŁY**
Label(frame_details, text='Szczegóły miejsca:').grid(row=0, column=0)

Label(frame_details, text='Nazwa:').grid(row=1, column=0)
label_detail_name_value = Label(frame_details, text='...')
label_detail_name_value.grid(row=1, column=1)

Label(frame_details, text='Miasto:').grid(row=1, column=2)
label_detail_city_value = Label(frame_details, text='...')
label_detail_city_value.grid(row=1, column=3)

Label(frame_details, text='Opis:').grid(row=1, column=4)
label_detail_description_value = Label(frame_details, text='...')
label_detail_description_value.grid(row=1, column=5)

Label(frame_details, text='Status:').grid(row=1, column=6)
label_detail_reserved_value = Label(frame_details, text='...')
label_detail_reserved_value.grid(row=1, column=7)

# **MAPA**
map_widget = tkintermapview.TkinterMapView(frame_map, width=1200, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()
