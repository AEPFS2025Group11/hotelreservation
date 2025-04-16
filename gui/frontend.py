import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import requests


def fetch_cities():
    try:
        response = requests.get("http://127.0.0.1:5049/api/hotels/addresses")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Fehler", f"Es gab ein Problem beim Abrufen der verfügbaren Ortschaften: {e}")
        return []


def show_cities(event):
    selected_city = city_combobox.get()
    for address in available_cities:
        if address['street'] == selected_city:
            address_details_text.config(state=tk.NORMAL)
            address_details_text.delete(1.0, tk.END)
            address_details_text.insert(tk.END, f"Straße: {address['street']}\n")
            address_details_text.insert(tk.END, f"Stadt: {address['city']}\n")
            address_details_text.insert(tk.END, f"PLZ: {address['zip_code']}\n")
            address_details_text.insert(tk.END, f"Adresse ID: {address['address_id']}")
            address_details_text.config(state=tk.DISABLED)
            break


root = tk.Tk()
root.title("Hotelreservationssystem")
root.geometry("400x300")

label = tk.Label(root, text="Wählen Sie eine Stadt aus:")
label.pack(pady=10)

available_cities = fetch_cities()

if not available_cities:
    messagebox.showerror("Fehler", "Keine Städte gefunden oder Fehler bei der API-Verbindung.")
else:
    city_combobox = ttk.Combobox(root, values=[address['city'] for address in available_cities])
    city_combobox.pack(pady=10)
    city_combobox.bind("<<ComboboxSelected>>", show_cities)

    address_details_text = tk.Text(root, height=8, width=40, wrap=tk.WORD, state=tk.DISABLED)
    address_details_text.pack(pady=10)

root.mainloop()
