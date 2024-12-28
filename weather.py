import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
import requests
import time
from PIL import Image, ImageTk
import io

# Constants
API_KEY = "06c921750b9a82d8f5d1294e1586276f"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Major Cities List for Dropdown
CITIES = ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Mumbai', 'Berlin', 'Cape Town']

def fetch_weather_data(city):
    params = {'q': city, 'appid': API_KEY}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")
        return None

def kelvin_to_celsius(kelvin):
    return int(kelvin - 273.15)

def format_time(timestamp):
    return time.strftime('%I:%M:%S %p', time.gmtime(timestamp - 21600))

def get_weather_info(city):
    data = fetch_weather_data(city)
    if not data:
        return None, None, None

    condition = data['weather'][0]['main']
    icon = data['weather'][0]['icon']
    temp = kelvin_to_celsius(data['main']['temp'])
    min_temp = kelvin_to_celsius(data['main']['temp_min'])
    max_temp = kelvin_to_celsius(data['main']['temp_max'])
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    sunrise = format_time(data['sys']['sunrise'])
    sunset = format_time(data['sys']['sunset'])

    weather_info = f"{condition}\n{temp}°C"
    weather_data = {
        "Min Temp": f"{min_temp}°C",
        "Max Temp": f"{max_temp}°C",
        "Pressure": f"{pressure} hPa",
        "Humidity": f"{humidity}%",
        "Wind Speed": f"{wind} m/s",
        "Sunrise": sunrise,
        "Sunset": sunset
    }

    return weather_info, weather_data, icon

def display_weather():
    city = city_combobox.get()
    if not city.strip():
        messagebox.showwarning("Input Error", "Please enter or select a city.")
        return

    weather_info, weather_data, icon = get_weather_info(city)
    if weather_info and weather_data:
        label1.config(text=weather_info)
        for widget in details_frame.winfo_children():
            widget.destroy()

        for key, value in weather_data.items():
            tile = tk.Frame(details_frame, bg="#d9edf7", bd=1, relief="solid", padx=10, pady=10)
            tile.pack(side="top", fill="x", pady=5)
            tk.Label(tile, text=f"{key}: {value}", font=f, bg="#d9edf7").pack()

        update_weather_icon(icon)

def update_weather_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    try:
        img_data = requests.get(icon_url).content
        image = Image.open(io.BytesIO(img_data))
        image = image.resize((100, 100), Image.Resampling.LANCZOS)
        weather_icon = ImageTk.PhotoImage(image)
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon
    except Exception as e:
        print(f"Error loading icon: {e}")
        icon_label.config(text="Icon not available")

# Set up the main window
canvas = tk.Tk()
canvas.geometry("800x600")
canvas.title("Weather App")
canvas.configure(bg="#f5f5f5")

# Font styles
f = ("Poppins", 15, "bold")
t = ("Poppins", 25, "bold")

# City selection dropdown
city_label = tk.Label(canvas, text="Select a city or enter a city name:", font=f, bg="#f5f5f5")
city_label.pack(pady=10)

city_combobox = ttk.Combobox(canvas, values=CITIES, font=f, width=20)
city_combobox.pack(pady=10)
city_combobox.set('New York')

# Fetch button
fetch_button = tk.Button(canvas, text="Get Weather", font=f, command=display_weather, bg="#0275d8", fg="white")
fetch_button.pack(pady=10)

# Label for the weather icon
icon_label = tk.Label(canvas, bg="#f5f5f5")
icon_label.pack(pady=20)

# Display weather info in tiles
label1 = tk.Label(canvas, font=t, bg="#f5f5f5")
label1.pack(pady=10)

details_frame = tk.Frame(canvas, bg="#f5f5f5")
details_frame.pack(pady=10, fill="both", expand=True)

# Start the Tkinter event loop
canvas.mainloop()
