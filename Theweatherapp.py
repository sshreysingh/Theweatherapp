
import requests
import tkinter as tk
from tkinter import ttk  # Import ttk for themed widgets
from tkinter import messagebox

def get_weather_emoji(description):
    emojis = {
        'clear sky': '☀️',
        'few clouds': '🌤️',
        'scattered clouds': '🌥️',
        'broken clouds': '☁️',
        'shower rain': '🌧️',
        'rain': '🌧️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️'
    }
    return emojis.get(description.lower(), '')

def fetch_weather(event=None):
    api_key = 'dc53d09fb2436ca2727ad4b51273c800'
    city = city_entry.get()
    units = 'metric'  # Default units for temperature

    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}'

    try:
        current_response = requests.get(current_url)
        current_response.raise_for_status()
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()

        current_data = current_response.json()
        temp = current_data['main']['temp']
        desc = current_data['weather'][0]['description']
        pressure = current_data['main']['pressure']
        humidity = current_data['main']['humidity']
        wind = current_data['wind']['speed']

        forecast_data = forecast_response.json()['list']
        forecast_text = f'{get_weather_emoji(desc)} Current Temperature: {temp:.2f} °C\n🌤️ Description: {desc} \n💨 Wind speed: {wind} \n💧 Humidity: {humidity} \n🌊 Pressure: {pressure}\n\n'

        for forecast in forecast_data[:4]:  # Display weather forecast for the next 4 time slots (12-hour forecast)
            date = forecast['dt_txt']
            temp = forecast['main']['temp']
            desc = forecast['weather'][0]['description']
            forecast_text += f'{date}\n🌡️ Temp: {temp:.2f}°C, {desc}\n'

        result_label.config(text=forecast_text, anchor="center")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")

# Create main window
root = tk.Tk()
root.geometry("600x600")
root.title('Weather App')

# Create and pack widgets with updated design and emojis using ttk themed widgets
style = ttk.Style(root)
style.theme_use("clam")  # Use the "clam" theme for consistent styling across platforms
style.configure('TLabel', font=("Arial", 20), background="#f0f0f0", foreground="#333")  # Configure label style
style.configure('TEntry', font=("Arial", 20), background="#ddd", foreground="#333", width=35)  # Configure entry style with increased width
style.configure('TButton', font=("Arial", 20), background="#4CAF50", foreground="white")  # Configure button style with larger font size
style.configure('TFrame', background="#f0f0f0", borderwidth=5, relief="ridge")  # Configure frame style with a ridge border

main_frame = ttk.Frame(root, style="TFrame")
main_frame.pack(fill="both", expand=True, padx=30, pady=30)

title_label = ttk.Label(main_frame, text='⛅ Weather App ⛅', font=("Arial", 24, "bold"))
title_label.pack(pady=(0, 20))

city_label = ttk.Label(main_frame, text='Enter city name:')
city_label.pack()

city_entry = ttk.Entry(main_frame)
city_entry.pack(pady=10)
city_entry.focus()
city_entry.bind("<Return>", fetch_weather)

fetch_button = ttk.Button(main_frame, text='Fetch Weather 🌦️', command=fetch_weather)
fetch_button.pack(pady=10)

result_label = ttk.Label(main_frame, text='', font=("Arial", 16), anchor="center")
result_label.pack(fill="both", expand=True)

# Run the Tkinter event loop
root.mainloop()
