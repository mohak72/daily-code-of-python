from weather_service import WeatherService

def display_weather(weather_data):
    """Display weather information in a formatted way."""
    print("\n=== Weather Report ===")
    print(f"Location: {weather_data['city']}, {weather_data['country']}")
    print(f"Temperature: {weather_data['temperature']}C")
    print(f"Feels like: {weather_data['feels_like']}C")
    print(f"Condition: {weather_data['description']}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")
    print("===================")

def main():
    weather_service = WeatherService()
    
    while True:
        print("\nWeather Information CLI")
        print("1. Get weather by city")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == "2":
            print("Goodbye!")
            break
        elif choice == "1":
            city = input("Enter city name: ")
            try:
                weather_data = weather_service.get_weather(city)
                display_weather(weather_data)
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
