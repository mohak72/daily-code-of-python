import tkinter as tk
from tkinter import ttk, messagebox
from weather_service import WeatherService
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO
import time

class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Initialize weather service and variables
        self.weather_service = WeatherService()
        self.units = "metric"
        self.auto_refresh = False
        self.auto_refresh_time = 300  # 5 minutes
        self.current_city = ""
        
        # Create and setup GUI elements
        self.setup_gui()
        
    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure("Weather.TFrame", padding=10)
        style.configure("Weather.TLabel", font=("Arial", 12))
        style.configure("WeatherData.TLabel", font=("Arial", 14))
        style.configure("Forecast.TFrame", padding=5)
        
        # Main container
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Search and options frame
        options_frame = ttk.Frame(container, style="Weather.TFrame")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # City entry
        search_frame = ttk.Frame(options_frame)
        search_frame.pack(fill=tk.X)
        
        self.city_var = tk.StringVar()
        ttk.Label(search_frame, text="City:", style="Weather.TLabel").pack(side=tk.LEFT)
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var)
        self.city_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Search button
        self.search_button = ttk.Button(search_frame, text="Search", command=self.get_weather)
        self.search_button.pack(side=tk.LEFT)
        
        # Options frame
        controls_frame = ttk.Frame(options_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Temperature unit toggle
        self.unit_var = tk.StringVar(value="metric")
        ttk.Radiobutton(controls_frame, text="Celsius", variable=self.unit_var, 
                       value="metric", command=self.on_unit_change).pack(side=tk.LEFT)
        ttk.Radiobutton(controls_frame, text="Fahrenheit", variable=self.unit_var,
                       value="imperial", command=self.on_unit_change).pack(side=tk.LEFT)
        
        # Auto-refresh toggle
        self.auto_refresh_var = tk.BooleanVar()
        ttk.Checkbutton(controls_frame, text="Auto-refresh (5min)", 
                       variable=self.auto_refresh_var,
                       command=self.toggle_auto_refresh).pack(side=tk.LEFT, padx=20)
        
        # Current weather frame
        self.weather_frame = ttk.Frame(container, style="Weather.TFrame")
        self.weather_frame.pack(fill=tk.X, padx=20)
        
        # Weather icon label
        self.icon_label = ttk.Label(self.weather_frame)
        self.icon_label.pack(pady=5)
        
        # Weather information labels
        self.location_label = ttk.Label(self.weather_frame, text="", style="WeatherData.TLabel")
        self.location_label.pack(pady=5)
        
        self.temp_label = ttk.Label(self.weather_frame, text="", style="WeatherData.TLabel")
        self.temp_label.pack(pady=5)
        
        self.feels_like_label = ttk.Label(self.weather_frame, text="", style="WeatherData.TLabel")
        self.feels_like_label.pack(pady=5)
        
        self.condition_label = ttk.Label(self.weather_frame, text="", style="WeatherData.TLabel")
        self.condition_label.pack(pady=5)
        
        self.humidity_label = ttk.Label(self.weather_frame, text="", style="WeatherData.TLabel")
        self.humidity_label.pack(pady=5)
        
        self.wind_label = ttk.Label(self.weather_frame, text="", style="WeatherData.TLabel")
        self.wind_label.pack(pady=5)
        
        # Forecast frame
        forecast_label = ttk.Label(container, text="5-Day Forecast", 
                                 style="WeatherData.TLabel")
        forecast_label.pack(pady=10)
        
        self.forecast_frame = ttk.Frame(container, style="Weather.TFrame")
        self.forecast_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create forecast day frames
        self.forecast_days = []
        for _ in range(5):
            day_frame = ttk.Frame(self.forecast_frame, style="Forecast.TFrame")
            day_frame.pack(fill=tk.X, pady=2)
            
            icon_label = ttk.Label(day_frame)
            icon_label.pack(side=tk.LEFT, padx=5)
            
            info_label = ttk.Label(day_frame, style="Weather.TLabel")
            info_label.pack(side=tk.LEFT, padx=5)
            
            self.forecast_days.append({
                "frame": day_frame,
                "icon": icon_label,
                "info": info_label
            })
        
        # Bind Enter key to search
        self.city_entry.bind("<Return>", lambda e: self.get_weather())
        
    def get_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
            
        self.current_city = city
        self.update_weather()
    
    def update_weather(self):
        def fetch_data():
            try:
                # Disable controls while fetching
                self.toggle_controls(False)
                
                # Get current weather and forecast
                weather_data = self.weather_service.get_weather(self.current_city, self.unit_var.get())
                forecast_data = self.weather_service.get_forecast(self.current_city, self.unit_var.get())
                
                # Update current weather display
                self.update_weather_display(weather_data)
                
                # Update forecast display
                self.update_forecast_display(forecast_data)
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                self.toggle_controls(True)
        
        # Run weather fetch in separate thread
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def update_weather_display(self, weather_data):
        # Update weather icon
        self.update_weather_icon(self.icon_label, weather_data["icon_url"])
        
        # Update weather information
        self.location_label.config(text=f"Location: {weather_data['city']}, {weather_data['country']}")
        self.temp_label.config(text=f"Temperature: {weather_data['temperature']}{weather_data['temp_unit']}")
        self.feels_like_label.config(text=f"Feels like: {weather_data['feels_like']}{weather_data['temp_unit']}")
        self.condition_label.config(text=f"Condition: {weather_data['description']}")
        self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        self.wind_label.config(text=f"Wind Speed: {weather_data['wind_speed']} {weather_data['speed_unit']}")
    
    def update_forecast_display(self, forecast_data):
        for day_frame, forecast in zip(self.forecast_days, forecast_data):
            self.update_weather_icon(day_frame["icon"], forecast["icon_url"])
            day_frame["info"].config(
                text=f"{forecast['day']}: {forecast['temperature']}{forecast['temp_unit']} - {forecast['description']}"
            )
    
    def update_weather_icon(self, label, icon_url):
        def fetch_icon():
            try:
                response = requests.get(icon_url)
                image = Image.open(BytesIO(response.content))
                photo = ImageTk.PhotoImage(image)
                label.configure(image=photo)
                label.image = photo
            except Exception:
                label.configure(image="")
                label.image = None
        
        threading.Thread(target=fetch_icon, daemon=True).start()
    
    def toggle_controls(self, enabled):
        state = "!disabled" if enabled else "disabled"
        self.search_button.state([state])
        self.city_entry.state([state])
    
    def on_unit_change(self):
        if self.current_city:
            self.update_weather()
    
    def toggle_auto_refresh(self):
        self.auto_refresh = self.auto_refresh_var.get()
        if self.auto_refresh and self.current_city:
            self.schedule_refresh()
    
    def schedule_refresh(self):
        if self.auto_refresh and self.current_city:
            self.update_weather()
            self.root.after(self.auto_refresh_time * 1000, self.schedule_refresh)

def main():
    root = tk.Tk()
    app = WeatherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
