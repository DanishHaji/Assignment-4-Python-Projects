import requests
import tkinter as tk
from tkinter import messagebox
from config import API_KEY

def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    if not API_KEY:
        messagebox.showerror("Error", "API key is missing. Please check your configuration.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        print(f"Requesting URL: {url}") 
        response = requests.get(url)
        print(f"Response: {response.status_code} - {response.text}")  
        response.raise_for_status()
        data = response.json()

        weather = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        result_label.config(
            text=f"🌤 Weather: {weather}\n🌡 Temperature: {temp}°C\n💧 Humidity: {humidity}%\n💨 Wind Speed: {wind_speed} m/s"
        )

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")
    except KeyError:
        messagebox.showerror("Error", "Invalid city name or unexpected response. Try again.")

root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

tk.Label(root, text="Enter City Name:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=20)

tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()
